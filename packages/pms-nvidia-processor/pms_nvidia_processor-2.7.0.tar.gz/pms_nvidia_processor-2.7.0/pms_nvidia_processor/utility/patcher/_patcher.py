from ._patch_collection import PatchPosXYCollection
from typing import Literal
import numpy as np


def pad_vector(
    vector: np.ndarray,
    overlap_length: int,
    mode: Literal[
        "edge",
        "mean",
        "median",
        "reflect",
        "symmetric",
    ] = "edge",
) -> np.ndarray:
    # create padding image
    padded_vector = np.pad(
        vector,
        pad_width=(
            (overlap_length, overlap_length),
            (overlap_length, overlap_length),
            (0, 0),
        ),
        mode=mode,
    )
    return padded_vector


class Patcher:

    def __init__(
        self,
        input_vector_shape: tuple[int, int, int],
        input_patch_shape: tuple[int, int, int],
        input_overlap_length: int,
        output_vector_shape: tuple[int, int, int],
        output_patch_shape: tuple[int, int, int],
        output_overlap_length: int,
    ) -> None:
        assert input_overlap_length > -1, "assert input_overlap_length > -1"
        assert output_overlap_length > -1, "assert output_overlap_length > -1"
        assert all(
            [e > 0 for e in input_patch_shape]
        ), "assert all([e > 0 for e in input_patch_shape])"
        assert all(
            [e > 0 for e in output_patch_shape]
        ), "assert all([e > 0 for e in output_patch_shape])"
        assert (
            len(input_patch_shape) == 3
        ), "assert len(input_patch_shape) == 3"  # only allow image-like vector
        assert (
            len(output_patch_shape) == 3
        ), "assert len(output_patch_shape) == 3"  # only allow image-like vector

        input_pos_collection = PatchPosXYCollection.create(
            vector_shape=input_vector_shape,
            patch_shape=input_patch_shape,
            overlap_length=input_overlap_length,
        )
        output_pos_collection = PatchPosXYCollection.create(
            vector_shape=output_vector_shape,
            patch_shape=output_patch_shape,
            overlap_length=0,
        )
        assert (
            input_pos_collection.shape == output_pos_collection.shape
        ), f"assert input_pos_collection.shape == output_pos_collection.shape | {input_pos_collection.shape} != {output_pos_collection.shape}"
        self._input_pos_collection = input_pos_collection
        self._output_pos_collection = output_pos_collection
        self._input_overlap_length = input_overlap_length
        self._output_overlap_length = output_overlap_length

    def slice(self, input_vector: np.ndarray):  # -> list[ndarray[Any, Any]]:
        return self._input_pos_collection.get_patch(input_vector)

    def merge(self, output_vector: np.ndarray, patches: list[np.ndarray] | np.ndarray):
        self._output_pos_collection.set_patch(
            vector=output_vector,
            patches=patches,
            overlab_length=self._output_overlap_length,
        )

    def merge_w(
        self, output_vector: np.ndarray, patches: list[np.ndarray] | np.ndarray
    ):
        import cv2

        n = 0

        pos_collection = self._output_pos_collection
        vector = output_vector
        weight_vector = np.ones((*output_vector.shape[:-1], 1), np.float32) * (1e-8)
        overlab_length = self._output_overlap_length
        print(f"pos_collection.size: {pos_collection.size}")
        print(f"pos_collection.patch_pos_list: {pos_collection.patch_pos_list}")
        for pos, patch in zip(pos_collection, patches, strict=True):  # inplace copy
            h, w, c = patch.shape
            np.add(
                vector[pos.y.range, pos.x.range],
                patch[
                    overlab_length : overlab_length + pos.y.dp,
                    overlab_length : overlab_length + pos.x.dp,
                ],
                out=vector[pos.y.range, pos.x.range],
            )
            weight_vector[pos.y.range, pos.x.range] += 1.0
            cv2.imwrite(
                f"/home/hskim/pms-nvidia-processor/.pytest_cache/2025-04-29 color test/{n:04d}.jpg",
                np.clip(vector * 255, 0, 255).astype(np.uint8),
            )
            n += 1
        # np.divide(vector, weight_vector, out=vector)
