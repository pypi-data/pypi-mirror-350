from ..base.config import *


class ColorResnetPreConfig:
    NUMBER_OF_INPUT_CHANNELS: int = 3
    NUMBER_OF_OUTPUT_CHANNELS: int = 30
    UPSCALE_RATIO: int = 1
    PATCH_SIZE = 256
    MAX_BATCH_SIZE = 1
    MIN_BATCH_SIZE = 1
    OPT_BATCH_SIZE = 1

    TRT_SHAPE_INPUT = (NUMBER_OF_INPUT_CHANNELS, PATCH_SIZE, PATCH_SIZE)
    TRT_SHAPE_OUTPUT = (NUMBER_OF_OUTPUT_CHANNELS,)


class ColorResnetPostConfig:
    NUMBER_OF_FRAMES = 1
    NUMBER_OF_INPUT_CHANNELS: int = 3 * NUMBER_OF_FRAMES
    NUMBER_OF_MODEL_OUTPUT_CHANNELS: int = 30
    NUMBER_OF_OUTPUT_CHANNELS: int = 3
    UPSCALE_RATIO: int = 1
    PATCH_SIZE = 512
    MAX_BATCH_SIZE = 1
    MIN_BATCH_SIZE = 1
    OPT_BATCH_SIZE = 1
    INPUT_OVERLAB_LENGTH = 16 * 2

    PATCHER_CONFIG = PatcherIOConfig(
        patch_size=PATCH_SIZE,
        upscale_ratio=UPSCALE_RATIO,
        number_of_input_channels=NUMBER_OF_INPUT_CHANNELS,
        number_of_output_channels=NUMBER_OF_OUTPUT_CHANNELS,
        input_overlab_length=INPUT_OVERLAB_LENGTH,
    )
    TRT_CONFIG = TRTIOConfig(
        patch_size=PATCH_SIZE,
        upscale_ratio=UPSCALE_RATIO,
        number_of_input_channels=NUMBER_OF_INPUT_CHANNELS,
        number_of_output_channels=NUMBER_OF_OUTPUT_CHANNELS,
    )
    TRT_SHAPE_MODEL_OUTPUT = (NUMBER_OF_MODEL_OUTPUT_CHANNELS,)
