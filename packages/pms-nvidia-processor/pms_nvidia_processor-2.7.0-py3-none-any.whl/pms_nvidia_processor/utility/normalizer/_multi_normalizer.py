import numpy as np
from concurrent.futures import ThreadPoolExecutor
from ._single_normalizer import SingleNormalizer
from ._normalization_param import NormalizationParam


class Slicer:
    def __init__(self, vector: np.ndarray, axis: int):
        self.axis = axis
        self.vector = vector
        slices: list = []
        for i in range(vector.shape[axis]):
            slc = [slice(None)] * vector.ndim  # 기본 슬라이싱 규칙 생성
            slc[axis] = i  # type: ignore n번째 차원에 인덱스를 고정
            slices.append(tuple(slc))
        self.slices = slices

    def __getitem__(self, index: int) -> np.ndarray:
        return self.vector[self.slices[index]]

    def __len__(self) -> int:
        return len(self.slices)

    def __iter__(self):
        for idx in range(len(self)):
            yield self[idx]


class MultiNormalizer:

    def __init__(
        self,
        params: list[NormalizationParam],
    ) -> None:
        self.single_normalizers: list[SingleNormalizer] = [
            SingleNormalizer(_param) for _param in params
        ]

    def normalize(self, vector: np.ndarray, axis: int):
        assert (
            vector.dtype == np.float32
        ), "ERROR, the vector's dtype must be np.float32"
        assert (
            vector.shape[axis] == self.number_of_normalization
        ), f"ERROR, the vector's shape[{axis}] must be {self.number_of_normalization}(number of normalization)"
        slicer = Slicer(vector, axis)
        # 병렬 처리
        with ThreadPoolExecutor() as executor:
            executor.map(
                lambda args: args[0].normalize(args[1]),
                zip(self.single_normalizers, slicer),
            )

    def denormalize(self, vector: np.ndarray, axis: int):
        assert (
            vector.dtype == np.float32
        ), "ERROR, the vector's dtype must be np.float32"
        assert (
            vector.shape[axis] == self.number_of_normalization
        ), f"ERROR, the vector's shape[{axis}] must be {self.number_of_normalization}(number of normalization)"

        slicer = Slicer(vector, axis)
        # 병렬 처리
        with ThreadPoolExecutor() as executor:
            executor.map(
                lambda args: args[0].denormalize(args[1]),
                zip(self.single_normalizers, slicer),
            )

    @property
    def scale(self) -> list[float]:
        return [nz._param.scale for nz in self.single_normalizers]

    @property
    def mean(self) -> list[float | None]:
        return [nz._param.mean for nz in self.single_normalizers]

    @property
    def std(self) -> list[float | None]:
        return [nz._param.std for nz in self.single_normalizers]

    @property
    def number_of_normalization(self) -> int:
        return len(self.single_normalizers)
