from contextlib import contextmanager
import mlflow
from urllib.parse import urlparse
from typing import Optional
import os
from PIL.Image import Image
import numpy as np
from matplotlib.figure import Figure
from mlflow.tracking.fluent import run_id_to_system_metrics_monitor
from plotly.graph_objects import Figure as FigureP
import io
import json
import hashlib
import tempfile
from typing import Union, Dict, List, Optional, Any
from oip_tracking_client.lib import (
    get_data_from_entity,
    check_env_variables,
    create_entity,
)
from oip_tracking_client.monitors.amd_monitor import AMDGPUMonitor
from oip_tracking_client.utilies import amd_gpu_exists
from oip_tracking_client.wavfile import write as wavfile_write
from oip_tracking_client.rest import http_request, augmented_raise_for_status
from oip_tracking_client.api import MLOpsAPI, MLOpsAPIEntity
from oip_tracking_client.lib import get_default_logger

logger = get_default_logger()


def log_artifact_extra(extra: Optional[Dict[str, Any]], artifact_path: str) -> None:
    """
    :param extra: Dict: extra information to log with the artifact
    :param artifact_path: the artifact path
    """

    # If extra is none, nothing to do
    if not extra:
        return

    # Check if necessary env variables are set
    check_env_variables()
    # Get the active run and check if it not none
    run = mlflow.active_run()
    if not run:
        msg = 'NO ACTIVE RUN, PLEASE START THE RUN...'
        logger.info(msg)
        raise RuntimeError(msg)

    # Add mlflow/experiment_id/run_id/artifacts to artifact path
    run_id = run.info.run_id
    experiment_id = run.info.experiment_id
    artifact_path = os.path.join(
        experiment_id, run_id, "artifacts", artifact_path)

    # Add artifact_path to extra that will be used as request body
    extra["artifact_path"] = artifact_path

    # Create token and headers
    endpoint: str = MLOpsAPI.get_update_artifact_endpoint(run_id=run_id)
    headers: Dict[str, str] = {
        "Authorization": f"Bearer {os.environ['MLFLOW_TRACKING_TOKEN']}"
    }
    logger.debug(
        f"Logging metadata for artifact at {artifact_path}: {extra}")
    # Make the request to the tracking server
    resp = http_request("POST", endpoint, headers=headers, json=extra)
    augmented_raise_for_status(resp)


class LogModelMethodWrapper:
    def __init__(self, method):
        self.method = method

    def __call__(self, *args, **kwargs):

        modified_args = list(args)

        if len(args) == 2:
            # If called with two positional arguments
            modified_args[1] = "model"
        elif "artifact_path" in kwargs:
            # If called with named arguments
            kwargs["artifact_path"] = "model"

        return self.method(*modified_args, **kwargs)


class ModuleWrapper:
    def __init__(self, module):
        self.module = module

    def __getattr__(self, attr):
        module_attr = getattr(self.module, attr)

        if attr == "log_model":
            return LogModelMethodWrapper(module_attr)

        return module_attr


class TrackingClientMeta(type):
    def __getattr__(cls, attr):

        mlflow_attr = getattr(mlflow, attr)

        # If the attribute is a module, wrap it using ModuleWrapper
        if type(mlflow_attr).__name__ == "module":
            return ModuleWrapper(mlflow_attr)

        return mlflow_attr


class TrackingClient(metaclass=TrackingClientMeta):
    @staticmethod
    @contextmanager
    def start_run():
        logger.info("Starting tracking run.")
        with mlflow.start_run(log_system_metrics=True) as run:
            monitor_system = run_id_to_system_metrics_monitor[run.info.run_id]

            if amd_gpu_exists():
                logger.info("AMD Gpu detected.")
                monitor_system.monitors.append(AMDGPUMonitor())

            parsed_host_url = urlparse(os.environ["OIP_API_HOST"])
            platform_url = f"{parsed_host_url.scheme}://{parsed_host_url.hostname}"
            if parsed_host_url.port:
                platform_url += f":{parsed_host_url.port}"
            workspace_id = os.environ["WORKSPACE_ID"]
            exp_id = run.info.experiment_id
            run_id = run.info.run_id
            exp_url = f"{platform_url}/ws/{workspace_id}/tracking/experiments/{exp_id}"
            run_url = f"{platform_url}/ws/{workspace_id}/tracking/experiments/{exp_id}/run/{run_id}"

            logger.info(f"View experiment at: {exp_url}")
            logger.info(f"View run at: {run_url}")

            yield run

    @staticmethod
    def connect(
        api_host: Optional[str] = None,
        api_key: Optional[str] = None,
        workspace_name: Optional[str] = None,
        workspace_id: Optional[str] = None,
    ):
        """
        Connect to the remove MLOPS platform
        It will check if the workspace exists and get its id
        Then set the the api host, the workspace id, and the api key
        :param api_host: str: The API Host
        :param api_key: str: The API Key
        :param workspace_name: str: The workspace name
        :param workspace_id: str: The workspace id
        """
        api_host = api_host or os.environ.get("OIP_API_HOST")
        api_key = api_key or os.environ.get("OIP_WORKLOAD_ACCESS_KEY")
        workspace_name = workspace_name or os.environ.get("WORKSPACE_NAME")
        workspace_id = workspace_id or os.environ.get("OIP_WORKSPACE_ID")

        missing_params = []
        if not api_host:
            missing_params.append("API host")
        if not api_key:
            missing_params.append("API key")
        if not workspace_name and not workspace_id:
            missing_params.append(
                "At least one of 'workspace_name' or 'workspace_id' must be provided. (when both are provided, workspace_id takes precedence over workspace_name)"
            )

        if missing_params:
            msg = f"Missing required parameters: {', '.join(missing_params)}"
            logger.info(msg)
            raise ValueError(msg)

        os.environ["OIP_API_HOST"] = api_host
        os.environ["MLFLOW_TRACKING_TOKEN"] = api_key
        os.environ["LEGACY_MODE"] = "False"

        if not workspace_id:
            legacy_params = {
                "filter_cols": "name",
                "filter_ops": "=",
                "filter_vals": workspace_name,
            }

            # Check if workspace exists
            data = get_data_from_entity(
                access_token=api_key,
                api_host=api_host,
                entity=MLOpsAPIEntity.Workspace,
                params={
                    "workspace_name": workspace_name,
                },
                legacy_params=legacy_params,
            )
            if len(data) == 0:
                msg = f"Workspace {workspace_name} does not exist."
                logger.info(msg)
                raise ValueError(msg)

            logger.info(f"Connecting to workspace {data}")
            # Get workspace id
            workspace_id: str = data[0]["id"]

        logger.info(f"Connecting to workspace {workspace_id}")

        # Set tracking URL & access token & workspace & api host
        mlflow.set_tracking_uri(
            MLOpsAPI.get_tracking_url(api_host, workspace_id))
        os.environ["WORKSPACE_ID"] = workspace_id

    @staticmethod
    def set_experiment(experiment_name: str):
        """
        Set experiment by experiment_name
        :param experiment_name: str: experiment name
        """

        # Check env variables
        check_env_variables()

        logger.info(
            f"Setting experiment: {experiment_name} with experiment: {os.environ['WORKSPACE_ID']}")
        # Check if exp exists
        legacy_params = {
            "filter_cols": "name|workspace_id",
            "filter_ops": "=|=",
            "filter_vals": f"{experiment_name}|{os.environ['WORKSPACE_ID']}",
        }

        data = get_data_from_entity(
            access_token=os.environ["MLFLOW_TRACKING_TOKEN"],
            api_host=os.environ["OIP_API_HOST"],
            entity=MLOpsAPIEntity.Experiment,
            params={
                "experiment_name": experiment_name,
            },
            legacy_params=legacy_params,
        )

        if len(data) == 0:
            experiment = create_entity(
                access_token=os.environ["MLFLOW_TRACKING_TOKEN"],
                api_host=os.environ["OIP_API_HOST"],
                entity="experiment",
                workspace_id=os.environ["WORKSPACE_ID"],
                body={
                    "name": experiment_name,
                },
            )
        else:
            experiment = data[0]

        logger.info(f"Experiment found: {experiment.get('name')}")
        # Get workspace id
        exp_id: str = experiment.get("experiment_id") or experiment.get("id")

        # Set mlflow experiment_id
        mlflow.set_experiment(experiment_id=exp_id)

    @staticmethod
    def set_run_name(run_name: str, run_id: Optional[str] = None):
        """
        Set run name
        :param run_name: str: The Run Name
        :param run_id: Optional[str]: The Run Id
        """
        if not run_id:
            active_run: Optional[mlflow.ActiveRun] = mlflow.active_run()
            if not active_run:
                msg = "There is no active run and run id is not specified"
                logger.info(msg)
                raise ValueError(msg)
            run_id: str = active_run.info.run_id

        logger.info(
            f"Setting run name to '{run_name}' for run ID {run_id}")
        # Create token and headers
        endpoint = MLOpsAPI.get_update_run_endpoint()
        headers: Dict[str, str] = {
            "Authorization": f"Bearer {os.environ['MLFLOW_TRACKING_TOKEN']}"
        }

        # Make the request to the tracking server
        resp = http_request(
            "POST",
            endpoint,
            headers=headers,
            json={"id": run_id, "run_name": run_name},
            allow_redirects=False,
        )
        augmented_raise_for_status(resp)

    @staticmethod
    def close():
        """
        Delete the env variable: MLFLOW_TRACKING_TOKEN
        """
        mlflow.end_run()
        if "MLFLOW_TRACKING_TOKEN" in os.environ:
            del os.environ["MLFLOW_TRACKING_TOKEN"]

    @staticmethod
    def log_image_at_step(
        image: Union[np.ndarray, Image],
        file_name: str,
        step: int,
        extra: Optional[Dict[str, Any]] = None,
    ) -> None:
        artifact_file: str = f"image/step_{str(int(step))}/{file_name}"
        mlflow.log_image(image, artifact_file)
        log_artifact_extra(extra, artifact_file)

    @staticmethod
    def log_figure_at_step(
        figure: Union[Figure, FigureP],
        file_name: str,
        step: int,
        extra: Optional[Dict[str, Any]] = None,
    ) -> None:
        artifact_path: str = f"figure/step_{str(int(step))}/{file_name}"
        mlflow.log_figure(figure, artifact_path)
        log_artifact_extra(extra, artifact_path)

    @staticmethod
    def log_json_at_step(
        dictionary: Union[Dict, List],
        file_name: str,
        step: int,
        extra: Optional[Dict[str, Any]] = None,
    ) -> None:
        artifact_path: str = f"json/step_{str(int(step))}/{file_name}"
        mlflow.log_dict(dictionary, artifact_path)
        log_artifact_extra(extra, artifact_path)

    @staticmethod
    def log_text_at_step(
        text: str,
        file_name: str,
        step: int,
        extra: Optional[Dict[str, Any]] = None,
    ) -> None:
        artifact_path: str = f"text/step_{str(int(step))}/{file_name}"
        mlflow.log_text(text, artifact_path)
        log_artifact_extra(extra, artifact_path)

    @staticmethod
    def log_llm_predictions_at_step(
        inputs: List[Dict[str, str]],
        outputs: List[str],
        prompts: List[str],
        step: int,
    ) -> None:
        dictionary: Dict[str, Any] = {
            "inputs": inputs,
            "outputs": outputs,
            "prompts": prompts,
        }
        serialized_data: bytes = json.dumps(
            dictionary, sort_keys=True).encode("utf-8")
        md5_hash: str = hashlib.md5(serialized_data).hexdigest()
        file_name: str = f"{md5_hash}.json"
        artifact_path: str = f"llm_predictions/step_{str(int(step))}/{file_name}"
        mlflow.log_dict(dictionary, artifact_path)

    @staticmethod
    def log_audio_at_step(
        data: Union[np.ndarray],
        file_name: str,
        step: int,
        rate: int = None,
        extra: Optional[Dict[str, Any]] = None,
    ) -> None:

        audio_formats = ("mp3", "wav", "flac")

        audio_format = file_name.split(".")[-1]
        if isinstance(data, np.ndarray):
            # Currently, only WAV audio formats are supported for numpy
            if audio_format != "wav":
                raise ValueError(
                    f"Only WAV audio formats are supported for numpy")

            if not rate:
                rate = 22500
                print(
                    f'Parameter "rate" is not provided! Using default: {rate}')
            bs = wavfile_write.write(rate, data)
            data = bs

        # act as a regular file with enforced audio format definition by user side
        if not audio_format:
            raise ValueError("Audio format must be provided.")
        elif audio_format not in audio_formats:
            raise ValueError(
                f"Invalid audio format is provided. Must be one of {audio_formats}"
            )

        if isinstance(data, str):
            if not os.path.exists(data) or not os.path.isfile(data):
                raise ValueError("Invalid audio file path")
            with open(data, "rb") as FS:
                data = FS.read()
        elif isinstance(data, io.BytesIO):
            data = data.read()

        if not isinstance(data, bytes):
            raise TypeError("Content is not a byte-stream object")

        artifact_path: str = f"audio/step_{str(int(step))}/{file_name}"
        with tempfile.NamedTemporaryFile(suffix=f".{audio_format}") as tmp:
            tmp.write(data)
            local_path = tmp.name
            mlflow.log_artifact(local_path, artifact_path)

        log_artifact_extra(extra, artifact_path)

    @staticmethod
    def infer_signature(model_input, model_output):
        return mlflow.models.signature.infer_signature(model_input, model_output)
