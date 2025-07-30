import os
from mlflow.tracking.request_header.abstract_request_header_provider import (
    RequestHeaderProvider,
)


class OipRequestHeaderProvider(RequestHeaderProvider):
    def in_context(self):
        return os.environ.get("OIP_WORKLOAD_ID") is not None

    def request_headers(self):
        headers = {}
        headers["OIP-Workload-Id"] = os.environ.get("OIP_WORKLOAD_ID")

        return headers
