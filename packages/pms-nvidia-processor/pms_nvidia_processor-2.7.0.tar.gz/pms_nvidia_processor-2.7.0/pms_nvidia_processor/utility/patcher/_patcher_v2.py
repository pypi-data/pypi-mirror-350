from dataclasses import dataclass
import numpy as np
from pms_nvidia_processor.utility.normalizer._multi_normalizer import Slicer
import cv2


@dataclass
class PatcherConfig:
    target_shape: tuple[int, int, int]
    patch_length: int
    overlab_length: int


class Slicer1D:
    def __init__(self, target_length: int, slice_length: int) -> None:
        assert (
            target_length >= slice_length
        ), f"ERROR, The target_length({target_length}) must greater than slice_length({slice_length})"
        self.slices: list[slice] = [
            slice(i * slice_length, (i + 1) * slice_length)
            for i in range(target_length // slice_length)
        ]
        if self.slices[-1].stop < target_length:
            self.slices.append(slice(target_length - slice_length, target_length))

    def __len__(self) -> int:
        return len(self.slices)

    def __getitem__(self, index: int) -> slice:
        return self.slices[index]

    def __iter__(self):
        for slice in self.slices:
            yield slice


class PatchContext:

    def __init__(
        self,
        vector: np.ndarray,
        slicer_x: Slicer1D,
        slicer_y: Slicer1D,
    ):
        self.vector = vector
        self.slicer_x = slicer_x
        self.slicer_y = slicer_y

    def __len__(self):
        return len(self.slicer_x) * len(self.slicer_y)

    def __getitem__(self, index: int) -> np.ndarray:
        idx_x = index % len(self.slicer_x)
        idx_y = index // len(self.slicer_x)
        return self.vector[self.slicer_y[idx_y], self.slicer_x[idx_x], :]

    def __iter__(self):
        for s_y in self.slicer_y:
            for s_x in self.slicer_x:
                yield self.vector[s_y, s_x, :]


class PatchingEngine:

    def __init__(
        self,
        vector_shape: tuple[int, int, int],
        patch_length: int,
    ) -> None:
        self.vector_shape = vector_shape
        self.patch_length = patch_length
        self.slicer_y = Slicer1D(vector_shape[0], patch_length)
        self.slicer_x = Slicer1D(vector_shape[1], patch_length)

    def create_context(self, vector: np.ndarray) -> PatchContext:
        assert (
            vector.shape == self.vector_shape
        ), f"ERROR, Shapes are not matced. vector.shape({vector.shape}) != self.vector_shape({self.vector_shape})"
        return PatchContext(vector, self.slicer_x, self.slicer_y)


class PatchingInferenceService:

    def __init__(
        self,
        input_vector_shape: tuple[int, int, int],
        input_patch_length: int,
        input_overlab_length: int,
        output_vector_shape: tuple[int, int, int],
        output_patch_length: int,
        output_overlab_length: int,
    ):
        self.input_patch_engine = PatchingEngine(
            input_vector_shape,
            input_patch_length - input_overlab_length,
        )
        self.output_patch_engine = PatchingEngine(
            output_vector_shape,
            output_patch_length - output_overlab_length,
        )
        self.input_overlab_length = input_overlab_length
        self.output_overlab_length = output_overlab_length

    def create_padded_input_patches_generator(
        self,
        input_vector: np.ndarray,
        mode: Literal[
            "edge",
            "mean",
            "median",
            "reflect",
            "symmetric",
        ],
    ):
        for p in self.input_patch_engine.create_context(input_vector):
            yield np.pad(
                p,
                pad_width=(
                    (self.input_overlab_length, self.input_overlab_length),
                    (self.input_overlab_length, self.input_overlab_length),
                    (0, 0),
                ),
                mode=mode,
            )

    def create_output_patches_generator(self, output_vector: np.ndarray):
        for p in self.output_patch_engine.create_context(output_vector):
            yield p


if __name__ == "__main__":
    scale = 1
    input_shape = (1000, 1000, 3)
    input_patch_length = 512
    input_overlab_length = 32
    output_shape = (
        input_shape[0] * scale,
        input_shape[1] * scale,
        input_shape[2] * scale,
    )
    output_patch_length = 512
    output_overlab_length = 32
    patcher = PatchingEngine(vector_shape=input_shape, patch_length=input_patch_length)
    input_vector = np.zeros(input_shape, np.uint8)
    context = patcher.create_context(input_vector)
    for idx, patch in enumerate(context):
        color = (
            255,
            int(255.0 * (float(idx) / len(context))),
            int(255.0 * (1.0 - float(idx) / len(context))),
        )
        cv2.rectangle(
            patch,
            (0, 0),
            (input_patch_length - 1, input_patch_length - 1),
            color,
            1,
            lineType=cv2.LINE_4,
        )

    cv2.imwrite(
        "/home/hskim/pms-nvidia-processor/.pytest_cache/patch.png", input_vector
    )
