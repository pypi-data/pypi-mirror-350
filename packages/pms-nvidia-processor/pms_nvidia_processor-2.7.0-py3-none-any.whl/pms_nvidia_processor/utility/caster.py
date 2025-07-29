import numpy as np


class Caster:
    __auto_clip_map = {
        np.dtype("uint8"): (0, 255),
    }

    def __init__(self, input_vector: np.ndarray) -> None:
        self._castable_type = input_vector.dtype
        self._uncastable_type = np.float32

    def cast(self, vector: np.ndarray) -> np.ndarray:  # A → B 변환
        assert (
            vector.dtype == self._castable_type
        ), f"ERROR, The vector's type must be {self._castable_type}"
        return vector.astype(self._uncastable_type)

    def uncast(self, vector: np.ndarray) -> np.ndarray:  # B → A 복구
        assert (
            vector.dtype == self._uncastable_type
        ), f"ERROR, The vector's type must be {self._uncastable_type}"
        if self._castable_type in self.__auto_clip_map:
            min, max = self.__auto_clip_map[self._castable_type]
            return np.clip(
                vector,
                min,
                max,
            ).astype(self._castable_type)
        else:
            return vector.astype(self._castable_type)
