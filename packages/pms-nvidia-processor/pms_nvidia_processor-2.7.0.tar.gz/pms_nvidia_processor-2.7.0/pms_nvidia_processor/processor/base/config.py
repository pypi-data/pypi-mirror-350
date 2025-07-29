from .dependency import *


@dataclass
class PatcherIOConfig:
    patch_size: int
    upscale_ratio: int
    number_of_input_channels: int
    number_of_output_channels: int
    input_overlab_length: int

    @property
    def output_overlab_length(self) -> int:
        return self.input_overlab_length * self.upscale_ratio

    @property
    def input_shape(self) -> tuple[int, int, int]:
        return (
            self.patch_size,
            self.patch_size,
            self.number_of_input_channels,
        )

    @property
    def output_shape(self) -> tuple[int, int, int]:
        output_patch_size = (
            self.patch_size - self.input_overlab_length * 2
        ) * self.upscale_ratio
        return (
            output_patch_size,
            output_patch_size,
            self.number_of_output_channels,
        )

    def build_patcher_params(
        self,
        input_vector: np.ndarray,
        output_vector: np.ndarray,
    ) -> dict[str, object]:
        input_vector_shape = input_vector.shape
        output_vector_shape = output_vector.shape
        return {
            "input_vector_shape": input_vector_shape,  # type: ignore
            "input_patch_shape": self.input_shape,
            "input_overlap_length": self.input_overlab_length,
            "output_vector_shape": output_vector_shape,  # type: ignore
            "output_patch_shape": self.output_shape,
            "output_overlap_length": self.output_overlab_length,
        }


@dataclass
class TRTIOConfig:
    patch_size: int
    upscale_ratio: int
    number_of_input_channels: int
    number_of_output_channels: int

    @property
    def input_shape(self) -> tuple[int, int, int]:
        return (self.number_of_input_channels, self.patch_size, self.patch_size)

    @property
    def output_shape(self) -> tuple[int, int, int]:
        return (
            self.number_of_output_channels,
            self.patch_size * self.upscale_ratio,
            self.patch_size * self.upscale_ratio,
        )


@dataclass
class PatcherWIOConfig(PatcherIOConfig):

    @property
    def output_shape(self) -> tuple[int, int, int]:
        output_patch_size = self.patch_size * self.upscale_ratio
        return (
            output_patch_size,
            output_patch_size,
            self.number_of_output_channels,
        )
