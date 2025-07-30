from enum import Enum


class Metrics(Enum):
    TEXTURE_ADDRESSER_UTILIZATION = "amd_gpu_texture_addresser_utilization"
    SHADER_EXPORT_UTILIZATION = "amd_gpu_shader_export_utilization"
    SHADER_INTERPOLATOR_UTILIZATION = "amd_gpu_shader_interpolator_utilization"
    SCAN_CONVERTER_UTILIZATION = "amd_gpu_scan_converter_utilization"
    PRIMITIVE_ASSEMBLY_UTILIZATION = "amd_gpu_primitive_assembly_utilization"
    DEPTH_BLOCK_UTILIZATION = "amd_gpu_depth_block_utilization"
    COLOUR_BLOCK_UTILIZATION = "amd_gpu_colour_block_utilization"
    GRAPHICS_PIPE_UTILIZATION = "amd_gpu_graphics_pipe_utilization"
    SCLK_MAX = "amd_gpu_sclk_max"
    MCLK_MAX = "amd_gpu_mclk_max"
    VRAM_USAGE = "amd_gpu_vram_usage"
    TEMPERATURE = "amd_gpu_temperature"
    POWER = "amd_gpu_power"
