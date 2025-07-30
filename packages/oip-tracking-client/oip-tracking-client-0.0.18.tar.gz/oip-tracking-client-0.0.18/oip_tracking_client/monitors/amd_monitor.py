import logging
import sys
import time
from typing import Optional
from mlflow.system_metrics.metrics.base_metrics_monitor import BaseMetricsMonitor

from oip_tracking_client.enums.metrics import Metrics

_logger = logging.getLogger(__name__)


class AMDGPUMonitor(BaseMetricsMonitor):
    """Class for monitoring AMD GPU stats."""

    def __init__(self):
        if "pyamdgpuinfo" not in sys.modules:
            # Only instantiate if `pyamdgpuinfo` is installed.
            raise ImportError(
                "`pyamdgpuinfo` is not installed, to log GPU metrics please run `pip install pyamdgpuinfo` "
                "to install it."
            )

        super().__init__()
        self.gpus = self.detect_and_initialize_gpus()

    def detect_and_initialize_gpus(self) -> Optional[list]:
        """
        Detects all gpus and initialize the utilisation pooling
        """
        gpus = AMDGPUMonitor.get_gpus()

        if len(gpus) == 0:
            _logger.info("NO AMD GPUs found! Getting THE AMD Metrics skipped!")
            return None

        for i, gpu in enumerate(gpus):
            is_pooling_alive = False
            gpu.start_utilisation_polling(ticks_per_second=10, buffer_size_in_ticks=100)
            while not is_pooling_alive:
                try:
                    _logger.info(f"Start utilisation pooling for GPU: {i}")
                    gpu.query_utilisation()
                    is_pooling_alive = True
                    _logger.info(f"utilisation pooling is running for GPU: {i}")
                except Exception as e:
                    time.sleep(1)
                    _logger.info(
                        f"Waiting for starting the utilization pooling: {str(e)}. Trying in 1s"
                    )

        _logger.info("Utilization polling started for all GPUs")
        return gpus

    @staticmethod
    def get_gpus() -> list:
        import pyamdgpuinfo

        devices = pyamdgpuinfo.detect_gpus()
        if not devices:
            return []
        return [pyamdgpuinfo.get_gpu(0)]

    def collect_metrics(self) -> None:
        """Collects the metrics"""
        for i, gpu in enumerate(self.gpus):
            utilization = gpu.query_utilisation()

            clock = gpu.query_max_clocks()
            vram = gpu.query_vram_usage()
            gpu_temperature = gpu.query_temperature()
            gpu_power = self.query_power_safe(gpu)

            self._build_metrics(clock, gpu_power, gpu_temperature, utilization, vram)

            _logger.debug(
                {
                    "device": i,
                    "utilization": utilization,
                    "sclk_max": clock["sclk_max"],
                    "mclk_max": clock["mclk_max"],
                    "vram": vram,
                    "temperature": gpu_temperature,
                    "power": gpu_power,
                }
            )

    @staticmethod
    def query_power_safe(gpu):
        """
        Gets the power of the AMD GPU and return 0 if received and exception
        """
        try:
            return gpu.query_power()
        except Exception as _:
            return 0

    def _build_metrics(self, clock, gpu_power, gpu_temperature, utilization, vram):
        self._metrics[Metrics.MCLK_MAX.value] = clock["mclk_max"] / 1e6
        self._metrics[Metrics.POWER.value] = gpu_power
        self._metrics[Metrics.SCLK_MAX.value] = clock["sclk_max"] / 1e6
        self._metrics[Metrics.TEMPERATURE.value] = gpu_temperature
        self._metrics[Metrics.VRAM_USAGE.value] = vram / (1024**3)
        self._metrics[Metrics.SHADER_EXPORT_UTILIZATION.value] = (
            utilization["shader_export"] * 100
        )
        self._metrics[Metrics.SHADER_INTERPOLATOR_UTILIZATION.value] = (
            utilization["shader_interpolator"] * 100
        )
        self._metrics[Metrics.TEXTURE_ADDRESSER_UTILIZATION.value] = (
            utilization["texture_addresser"] * 100
        )
        self._metrics[Metrics.SCAN_CONVERTER_UTILIZATION.value] = (
            utilization["scan_converter"] * 100
        )
        self._metrics[Metrics.PRIMITIVE_ASSEMBLY_UTILIZATION.value] = (
            utilization["primitive_assembly"] * 100
        )
        self._metrics[Metrics.COLOUR_BLOCK_UTILIZATION.value] = (
            utilization["colour_block"] * 100
        )
        self._metrics[Metrics.DEPTH_BLOCK_UTILIZATION.value] = (
            utilization["depth_block"] * 100
        )
        self._metrics[Metrics.GRAPHICS_PIPE_UTILIZATION.value] = (
            utilization["graphics_pipe"] * 100
        )

    def aggregate_metrics(self):
        return {k: round(v, 1) for k, v in self._metrics.items()}
