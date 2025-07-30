import os
import requests
from requests.adapters import HTTPAdapter
from requests.exceptions import HTTPError
from functools import lru_cache
from urllib3.util import Retry
from oip_tracking_client.lib import get_default_logger
from oip_tracking_client.utilies import verify_ssl

logger = get_default_logger()

INTERNAL_ERROR = 500
INVALID_STATE = 500
TEMPORARILY_UNAVAILABLE = 503
REQUEST_LIMIT_EXCEEDED = 429
ENDPOINT_NOT_FOUND = 404
RESOURCE_DOES_NOT_EXIST = 404
PERMISSION_DENIED = 403
CUSTOMER_UNAUTHORIZED = 401
BAD_REQUEST = 400
RESOURCE_ALREADY_EXISTS = 409
INVALID_PARAMETER_VALUE = 400
UNPROCESSABLE_ENTITY = 422
CONTENT_TOO_LARGE = 413
UNSUPPORTED_MEDIA_TYPE = 415
REQUEST_TIMEOUT = 408
BAD_GATEWAY = 502
GATEWAY_TIMEOUT = 504


_TRANSIENT_FAILURE_RESPONSE_CODES = frozenset(
    [
        REQUEST_TIMEOUT,  # Request Timeout
        REQUEST_LIMIT_EXCEEDED,  # Too Many Requests
        BAD_GATEWAY,  # Bad Gateway
        TEMPORARILY_UNAVAILABLE,  # Service Unavailable
        GATEWAY_TIMEOUT,  # Gateway Timeout
    ]
)
# INTERNAL_ERROR,  # Internal Server Error


@lru_cache(maxsize=64)
def _get_request_session(max_retries, backoff_factor, retry_codes):
    """
    Returns a cached Requests.Session object for making HTTP request.

    :param max_retries: Maximum total number of retries.
    :param backoff_factor: a time factor for exponential backoff. e.g. value 5 means the HTTP
      request will be retried with interval 5, 10, 20... seconds. A value of 0 turns off the
      exponential backoff.
    :param retry_codes: a list of HTTP response error codes that qualifies for retry.
    :return: requests.Session object.
    """
    assert 0 <= max_retries < 10
    assert 0 <= backoff_factor < 120

    retry_kwargs = {
        "total": max_retries,
        "connect": max_retries,
        "read": max_retries,
        "redirect": max_retries,
        "status": max_retries,
        "status_forcelist": retry_codes,
        "backoff_factor": backoff_factor,
        "allowed_methods": None,
    }

    retry = Retry(**retry_kwargs)
    adapter = HTTPAdapter(max_retries=retry)
    session = requests.Session()
    session.verify = verify_ssl()
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


def _get_http_response_with_retries(
    method, url, max_retries, backoff_factor, retry_codes, **kwargs
):
    """
    Performs an HTTP request using Python's `requests` module with an automatic retry policy.

    :param method: a string indicating the method to use, e.g. "GET", "POST", "PUT".
    :param url: the target URL address for the HTTP request.
    :param max_retries: Maximum total number of retries.
    :param backoff_factor: a time factor for exponential backoff. e.g. value 5 means the HTTP
      request will be retried with interval 5, 10, 20... seconds. A value of 0 turns off the
      exponential backoff.
    :param retry_codes: a list of HTTP response error codes that qualifies for retry.
    :param kwargs: Additional keyword arguments to pass to `requests.Session.request()`

    :return: requests.Response object.
    """
    headers = kwargs.get("headers", {})
    oip_workload_id = os.environ.get("OIP_WORKLOAD_ID")
    if oip_workload_id:
        headers["OIP-Workload-Id"] = oip_workload_id
    kwargs["headers"] = headers

    session = _get_request_session(max_retries, backoff_factor, retry_codes)
    return session.request(method, url, **kwargs)


def http_request(
    method,
    url,
    max_retries=None,
    backoff_factor=None,
    retry_codes=None,
    timeout=None,
    **kwargs,
):
    """
    Makes an HTTP request with the specified method to the specified hostname/endpoint. Transient
    errors such as Rate-limited (429), service unavailable (503) and internal error (500) are
    retried with an exponential back off with backoff_factor * (1, 2, 4, ... seconds).
    The function parses the API response (assumed to be JSON) into a Python object and returns it.

    :param method: a string indicating the method to use, e.g. "GET", "POST", "PUT".
    :param url: the target URL address for the HTTP request.
    :param max_retries: maximum number of retries before throwing an exception.
    :param backoff_factor: a time factor for exponential backoff. e.g. value 5 means the HTTP
      request will be retried with interval 5, 10, 20... seconds. A value of 0 turns off the
      exponential backoff.
    :param retry_codes: a list of HTTP response error codes that qualifies for retry.
    :param timeout: wait for timeout seconds for response from remote server for connect and
      read request.
    :param kwargs: Additional keyword arguments to pass to `requests.Session.request()`

    :return: requests.Response object.
    """

    timeout = timeout or 120
    retry_codes = retry_codes or _TRANSIENT_FAILURE_RESPONSE_CODES
    backoff_factor = backoff_factor or 2
    max_retries = max_retries or 2

    try:
        return _get_http_response_with_retries(
            method,
            url,
            max_retries=max_retries,
            backoff_factor=backoff_factor,
            retry_codes=retry_codes,
            timeout=timeout,
            **kwargs,
        )
    except requests.exceptions.Timeout as to:
        raise Exception(
            str(f"API request to {url} failed with timeout exception {to}.")
        )
    except Exception as e:
        raise Exception(
            str(f"API request to {url} failed with exception {str(e)}"), INTERNAL_ERROR
        )


def augmented_raise_for_status(response):
    """Wrap the standard `requests.response.raise_for_status()` method and return reason"""
    try:
        response.raise_for_status()
    except HTTPError as e:
        if response.text:
            logger.info(f"Error making request to: {response.request.url}")
            raise HTTPError(f"{e}. Response text: {response.text}")
        else:
            raise e
