from .config import *
from ..base.dependency import *
from ..base.processor import *
from ...utility import patcher, normalizer


class DRURBPNDeinterF3GLossContext:

    def __init__(
        self,
        input_vector: np.ndarray,
        input_patcher: patcher.Patcher,
    ) -> None:
        config = DRURBPNDEINTERF3GLOSSConfig

        self.input_vector = input_vector
        self.input_pathcer = input_patcher
        self.padded_input_image = patcher.pad_vector(
            vector=self.input_vector,
            overlap_length=config.PATCHER_CONFIG.input_overlab_length,
            mode="edge",
        )
        self.input_patches: list[np.ndarray] = self.input_pathcer.slice(
            self.padded_input_image
        )
        self.output_patches: np.ndarray = np.zeros(
            (len(self.input_patches), config.PATCH_SIZE, config.PATCH_SIZE, 3),
            np.float32,
        )
        self.output_vector: np.ndarray = np.zeros(
            (
                input_vector.shape[0] * config.UPSCALE_RATIO,
                input_vector.shape[1] * config.UPSCALE_RATIO,
                config.NUMBER_OF_OUTPUT_CHANNELS,
            ),
            np.float32,
        )
