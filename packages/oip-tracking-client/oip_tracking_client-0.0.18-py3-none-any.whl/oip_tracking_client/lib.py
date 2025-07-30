import requests
import logging
import os
import time
from typing import Dict, Optional, Union, List
from oip_tracking_client.api import MLOpsAPI, MLOpsAPIEntity
from oip_tracking_client.utilies import verify_ssl


class Config:
    MAX_RETRIES = 4


def get_default_logger():
    """Get a logging object using the default log level set in cfg.
    https://docs.python.org/3/library/logging.html
    """
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        stderr_handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s %(levelname)s %(message)s", datefmt="%Y/%m/%d %H:%M:%S"
        )
        stderr_handler.setFormatter(formatter)
        logger.addHandler(stderr_handler)
    return logger


def get_data_from_entity(
    access_token: str,
    api_host: str,
    entity: MLOpsAPIEntity,
    params: Dict,
    legacy_params: Dict
) -> Optional[List[Dict]]:
    """
    Retrieve data from the API based on the provided parameters.

    :param access_token: str: The access token for authentication.
    :param api_host: str: The host URL of the API.
    :param entity: str: The name of the entity for which to retrieve the data.
    :param params: FrozenSet: Additional parameters for the API request.
    :return: list: The retrieved data.
    """
    url = MLOpsAPI.get_retrieve_entity_endpoint(entity)
    headers = {"authorization": "APIKey " + access_token}
    logger = get_default_logger()
    try:
        if os.environ["LEGACY_MODE"] == "True":
            params = legacy_params
        logger.debug(url)
        resp = MLOpsAPI.get(
            url=url,
            params=params,
            headers=headers,
            stream=False,
            timeout=None,
        )
    except:
        os.environ["LEGACY_MODE"] = "True"
        url = MLOpsAPI.get_retrieve_entity_endpoint(entity)
        headers = {"authorization": "APIKey " + access_token}
        logger.debug(url)
        resp = get_data(url, headers, dict(legacy_params))

    if resp.status_code == 200:
        json_data = resp.json()
        if "items" in json_data:
            return json_data["items"]
        if "data" in json_data:
            return json_data["data"]

    return None


def get_data(
    url: str,
    headers: Dict[str, str],
    params: Dict[str, str],
    logger=None,
    stream=False,
):
    """
    .. py:method:: General 'make api request' function.
    Assigns headers and builds in retries and logging
    :param url: str: api host, example: https://www.example.com/api?x=1
    :param headers: Dict[str, str]: headers
    :param params: Dict[str, str]: params
    :param logger: Logger: logger
    :param stream: bool:
    """
    """General 'make api request' function.
    Assigns headers and builds in retries and logging.
    """
    base_log_record: Dict[str, Union[str, Dict[str, str]]] = dict(
        route=url, params=params
    )
    retry_count: int = 0

    if not logger:
        logger = get_default_logger()
        logger.debug(url)
        logger.debug(params)
    while retry_count <= Config.MAX_RETRIES:
        start_time = time.time()
        try:
            response = MLOpsAPI.get(
                url=url,
                params=params,
                headers=headers,
                stream=stream,
                timeout=None,
            )

        except Exception as e:
            response = e

        elapsed_time = time.time() - start_time
        status_code = response.status_code if hasattr(
            response, "status_code") else None
        log_record: Dict[str, Union[int, float, str, Dict[str, str]]] = dict(
            base_log_record
        )
        log_record["elapsed_time_in_ms"] = 1000 * elapsed_time
        log_record["retry_count"] = retry_count
        log_record["status_code"] = status_code
        if status_code == 200:  # Success
            logger.debug("OK", extra=log_record)
            return response
        if status_code in [204, 206]:  # Success with a caveat - warning
            log_msg = {204: "No Content", 206: "Partial Content"}[status_code]
            logger.warning(log_msg, extra=log_record)
            return response
        log_record["tag"] = "failed_gro_api_request"
        if retry_count < Config.MAX_RETRIES:
            logger.warning(
                response.text if hasattr(response, "text") else response,
                extra=log_record,
            )
        if status_code in [400, 401, 402, 404, 301]:
            break  # Do not retry
        logger.warning("{}".format(response), extra=log_record)
        if retry_count > 0:
            # Retry immediately on first failure.
            # Exponential backoff before retrying repeatedly failing requests.
            time.sleep(2**retry_count)
        retry_count += 1
    raise APIError(response, retry_count, url, params)


def create_entity(
    access_token: str,
    api_host: str,
    entity: str,
    workspace_id: str,
    body: Dict,
) -> Dict:
    url = MLOpsAPI.get_create_entity_endpoint(workspace_id, entity)
    headers = {"authorization": "APIKey " + access_token}

    logger = get_default_logger()
    logger.debug(url)
    logger.debug(body)

    response = MLOpsAPI.post(
        url=url,
        body=body,
        headers=headers,
    )

    logger.debug(response)

    if not response.ok:
        raise APIError(response, 1, url, body)

    return response.json()


class APIError(Exception):
    def __init__(self, response, retry_count, url, params):
        self.response = response
        self.retry_count = retry_count
        self.url = url
        self.params = params
        self.status_code = (
            response.status_code if hasattr(response, "status_code") else None
        )
        try:
            json_content = self.response.json()
            # 'error' should be something like 'Not Found' or 'Bad Request'
            self.message = json_content.get("error", "")
            # Some error responses give additional info.
            # For example, a 400 Bad Request might say "metricId is required"
            if "message" in json_content:
                self.message += ": {}".format(json_content["message"])
        except Exception:
            # If the error message can't be parsed, fall back to a generic "giving up" message.
            self.message = "Giving up on {} after {} {}: {}".format(
                self.url,
                self.retry_count,
                "retry" if self.retry_count == 1 else "retries",
                response,
            )


def check_env_variables():
    """
    Check if necessary env variables are set
    """
    if (
        "OIP_API_HOST" not in os.environ
        or "WORKSPACE_ID" not in os.environ
        or "MLFLOW_TRACKING_TOKEN" not in os.environ
    ):
        raise RuntimeError(
            "Not Connected. Use TrackingClient.connect before starting the run."
        )
