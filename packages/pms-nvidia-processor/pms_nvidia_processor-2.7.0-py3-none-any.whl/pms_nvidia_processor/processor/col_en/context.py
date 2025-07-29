from .config import *
from ..base.dependency import *
from ..base.processor import *
from ...utility import patcher, normalizer


class ColEnContext:

    def __init__(
        self,
        input_vector: np.ndarray,
        input_patcher: patcher.PatcherW,
    ) -> None:
        config = ColEnConfig()

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
            (
                len(self.input_patches),
                config.PATCH_SIZE * config.UPSCALE_RATIO,
                config.PATCH_SIZE * config.UPSCALE_RATIO,
                3,
            ),
            np.float32,
        )
        self.output_vector: np.ndarray = np.zeros(
            (*self.padded_input_image.shape[:-1], 3),
            np.float32,
        )
