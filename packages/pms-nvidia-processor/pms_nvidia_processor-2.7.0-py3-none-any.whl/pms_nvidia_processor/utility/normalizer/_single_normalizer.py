import numpy as np
from ._normalization_param import NormalizationParam


class SingleNormalizer:

    def __init__(
        self,
        param: NormalizationParam,
    ) -> None:
        self._param: NormalizationParam = param

    def normalize(self, vector: np.ndarray):
        assert (
            vector.dtype == np.float32
        ), "ERROR, the vector's dtype must be np.float32"
        np.divide(vector, self.scale, vector)
        if self.mean is not None:
            np.subtract(vector, self.mean, vector)
        if self.std is not None:
            np.divide(vector, self.std, vector)

    def denormalize(self, vector: np.ndarray):
        assert (
            vector.dtype == np.float32
        ), "ERROR, the vector's dtype must be np.float32"
        if self.std is not None:
            np.multiply(vector, self.std, vector)
        if self.mean is not None:
            np.add(vector, self.mean, vector)
        np.multiply(vector, self.scale, vector)

    @property
    def scale(self):
        return self._param.scale

    @property
    def mean(self):
        return self._param.mean

    @property
    def std(self):
        return self._param.std
