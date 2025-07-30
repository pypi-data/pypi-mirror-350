import os
import enum
from urllib.parse import urljoin
import requests
from oip_tracking_client.utilies import verify_ssl


def is_legacy_mode_enabled() -> bool:
    return os.environ.get("LEGACY_MODE", "false").lower() in ("true", "1", "yes")


class MLOpsAPIEntity(enum.Enum):
    Workspace = "workspace"
    Experiment = "mlflow_experiment"


class MLOpsAPILegacy:

    @staticmethod
    def get_tracking_url(api_host: str, workspace_id: str) -> str:
        return f"{api_host}/mlflow/workspaces/{workspace_id}"

    @staticmethod
    def get_update_artifact_endpoint() -> str:
        return f"{os.environ['OIP_API_HOST']}/mlflow/mlflow_artifacts"

    @staticmethod
    def get_update_run_endpoint() -> str:
        return f"{os.environ['OIP_API_HOST']}/mlflow/mlflow_runs"

    @staticmethod
    def get_create_entity_endpoint(workspace_id: str, entity: str) -> str:
        api_host = os.environ["OIP_API_HOST"]
        tracking_host = MLOpsAPI.get_tracking_url(api_host, workspace_id)
        return urljoin(tracking_host + "/", f"api/2.0/mlflow/{entity}/create")

    @staticmethod
    def get_retrieve_entity_endpoint(entity: MLOpsAPIEntity) -> str:
        api_host = os.environ["OIP_API_HOST"]
        return urljoin(api_host + "/", f"mlflow/entities/{entity.value}")


class MLOpsAPI:

    @staticmethod
    def get_tracking_url(api_host: str, workspace_id: str) -> str:
        if is_legacy_mode_enabled():
            return MLOpsAPILegacy.get_tracking_url(api_host, workspace_id)

        return f"{api_host}/v1/workspaces/{workspace_id}/mlflow"

    @staticmethod
    def get_update_artifact_endpoint(run_id: str) -> str:
        if is_legacy_mode_enabled():
            return MLOpsAPILegacy.get_update_artifact_endpoint()
        return f"{os.environ['OIP_API_HOST']}/v1/workspaces/{os.environ['WORKSPACE_ID']}/mlflow_runs/{run_id}/mlflow_artifacts"

    @staticmethod
    def get_update_run_endpoint() -> str:
        if is_legacy_mode_enabled():
            return MLOpsAPILegacy.get_update_run_endpoint()
        return f"{os.environ['OIP_API_HOST']}/v1/workspaces/{os.environ['WORKSPACE_ID']}/mlflow_runs"

    @staticmethod
    def get_create_entity_endpoint(workspace_id: str, entity: str) -> str:
        if is_legacy_mode_enabled():
            return MLOpsAPILegacy.get_create_entity_endpoint(workspace_id, entity)

        api_host = os.environ["OIP_API_HOST"]
        tracking_host = MLOpsAPI.get_tracking_url(api_host, workspace_id)
        return urljoin(tracking_host + "/", f"api/2.0/mlflow/{entity}/create")

    @staticmethod
    def get_retrieve_entity_endpoint(entity: MLOpsAPIEntity) -> str:
        if is_legacy_mode_enabled():
            return MLOpsAPILegacy.get_retrieve_entity_endpoint(entity)

        api_host = os.environ["OIP_API_HOST"]
        if entity == MLOpsAPIEntity.Workspace:
            return urljoin(api_host + "/", f"v1/workspaces")
        elif entity == MLOpsAPIEntity.Experiment:
            return urljoin(api_host + "/", f"v1/workspaces/{os.environ['WORKSPACE_ID']}/experiments")

    @staticmethod
    def get(
        url: str,
        params: dict = None,
        headers: dict = None,
        stream: bool = False,
        timeout=None,
    ) -> requests.Response:
        workload_id = os.environ.get("OIP_WORKLOAD_ID")
        if workload_id:
            headers["OIP-Workload-Id"] = workload_id
        try:
            response = requests.get(
                url,
                params=params,
                headers=headers,
                timeout=timeout,
                stream=stream,
                verify=verify_ssl(),
            )
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            raise Exception(f"GET request failed: {e}")

    @staticmethod
    def post(url: str, body: dict = None, headers: dict = None) -> requests.Response:

        workload_id = os.environ.get("OIP_WORKLOAD_ID")
        if workload_id:
            headers["OIP-Workload-Id"] = workload_id

        try:
            response = requests.post(
                url, json=body, headers=headers, verify=verify_ssl()
            )
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            raise Exception(f"POST request failed: {e}")
