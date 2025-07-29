from typing import Literal
import numpy as np


def crop_vector(
    vector: np.ndarray,
    overlap_length: int,
) -> np.ndarray:
    return vector[overlap_length:-overlap_length, overlap_length:-overlap_length].copy()


class PatcherW:

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
        assert all(
            [e > 0 for e in input_patch_shape]
        ), "assert all([e > 0 for e in input_patch_shape])"
        assert (
            len(input_patch_shape) == 3
        ), "assert len(input_patch_shape) == 3"  # only allow image-like vector
        self._input_vector_shape = input_vector_shape
        self._input_patch_shape = input_patch_shape
        self._input_overlap_length = input_overlap_length

        self._patch_pos_list = self._get_patch_pos_list()
        self._weight_mask = self._make_hanning_weight_mask(output_patch_shape)

    def _get_patch_pos_list(self):
        input_vector_width = self._input_vector_shape[1]
        input_vector_height = self._input_vector_shape[0]
        input_patch_width = self._input_patch_shape[1]
        input_patch_height = self._input_patch_shape[0]
        input_overlap_length = self._input_overlap_length
        patchs: list[tuple[slice, slice]] = []
        for y0 in range(
            0, input_vector_height, input_patch_height - input_overlap_length
        ):
            y1 = min(y0 + input_patch_height, input_vector_height)
            for x0 in range(
                0, input_vector_width, input_patch_width - input_overlap_length
            ):
                x1 = min(x0 + input_patch_width, input_vector_width)
                patchs.append((slice(y0, y1), slice(x0, x1)))
        return patchs

    def _make_gaussian_weight_mask(
        self,
        shape: tuple[int, int, int],
        min_val=0.0,
        max_val=1.0,
        sigma_scale=0.25,
    ):
        """
        h, w: 패치 높이/너비
        sigma_scale: 중심에서 분포하는 정도 (0.25이면 가우시안 표준편차가 크기 대비 1/4)
        """

        h, w, c = shape
        y = np.linspace(-1, 1, h)
        x = np.linspace(-1, 1, w)
        yy, xx = np.meshgrid(y, x, indexing="ij")
        d2 = xx**2 + yy**2
        sigma2 = sigma_scale**2
        weights = np.exp(-d2 / (2 * sigma2))
        np.subtract(weights, weights.min(), out=weights)
        np.divide(weights, weights.max(), out=weights)
        weights = weights * (max_val - min_val) + min_val
        return weights.astype(np.float32)[:, :, None]

    def _make_hanning_weight_mask(
        self,
        shape: tuple[int, int, int],
        min_val=0.0,
        max_val=1.0,
    ):
        """
        Hanning window 기반의 weight mask를 생성합니다.

        Parameters:
            shape (tuple[int, int, int]): (h, w, c) - 패치의 높이, 너비, 채널 수
            min_val (float): weight의 최소값 (스케일 조정용)
            max_val (float): weight의 최대값 (스케일 조정용)

        Returns:
            np.ndarray: shape = (h, w, c), float32 타입의 Hanning weight mask
        """
        h, w, c = shape

        hann_y = np.hanning(h)
        hann_x = np.hanning(w)
        hann_2d = np.outer(hann_y, hann_x).astype(np.float32)
        # import cv2
        # cv2.imwrite(
        #     ".pytest_cache/hanning_wight_mask.png", (hann_2d * 255).astype(np.uint8)
        # )

        # 정규화 및 스케일 조정
        # hann_2d -= hann_2d.min()
        # hann_2d /= hann_2d.max()
        # hann_2d = hann_2d * (max_val - min_val) + min_val

        # (h, w, 1)로 reshape
        weight = hann_2d[:, :, None]

        return weight.astype(np.float32)

    def slice(self, input_vector: np.ndarray) -> list[np.ndarray]:
        patchs = []
        for ys, xs in self._get_patch_pos_list():
            patchs.append(input_vector[ys, xs])
        return patchs

    def merge(
        self,
        patches: list[np.ndarray] | np.ndarray,
        output_vector: np.ndarray,
        scale: int = 1,
    ):
        # w_vector = np.ones((*output_vector.shape[:-1], 1), np.float32) * (1e-8)
        w_vector = np.zeros((*output_vector.shape[:-1], 1), np.float32)
        for (ys, xs), patch in zip(self._patch_pos_list, patches, strict=True):
            ys_out = slice(ys.start * scale, ys.stop * scale)
            xs_out = slice(xs.start * scale, xs.stop * scale)
            target_vector = output_vector[ys_out, xs_out]
            target_patch = patch[: target_vector.shape[0], : target_vector.shape[1]]
            target_weight_mask = self._weight_mask[
                : target_patch.shape[0], : target_patch.shape[1]
            ]
            np.multiply(target_patch, target_weight_mask, out=target_patch)
            np.add(target_vector, target_patch, out=target_vector)
            w_vector[ys_out, xs_out] += target_weight_mask
        output_vector /= w_vector
