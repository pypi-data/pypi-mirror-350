import os
from distutils.util import strtobool

from oip_tracking_client.monitors.amd_monitor import AMDGPUMonitor


def amd_gpu_exists() -> bool:
    try:
        gpus = AMDGPUMonitor.get_gpus()
        return True if gpus else False
    except Exception:
        return False


def verify_ssl() -> bool:
    return bool(strtobool(os.environ.get("OI_REQUESTS_VERIFY_SSL", "True")))
