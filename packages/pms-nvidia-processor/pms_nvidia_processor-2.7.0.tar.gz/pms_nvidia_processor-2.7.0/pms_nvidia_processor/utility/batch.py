from typing import Generator
import numpy as np


class BatchTool:

    @classmethod
    def batch_list(
        cls, target_list: list, batch_size: int
    ) -> Generator[list, None, None]:
        l = len(target_list)
        for ndx in range(0, l, batch_size):  # iterable 데이터를 배치 단위로 확인
            yield target_list[
                ndx : min(ndx + batch_size, l)
            ]  # batch 단위 만큼의 데이터를 반환

    @classmethod
    def batch_vector(
        cls, target_vector: np.ndarray, batch_size: int
    ) -> Generator[np.ndarray, None, None]:
        l = target_vector.shape[0]
        for ndx in range(0, l, batch_size):  # iterable 데이터를 배치 단위로 확인
            yield target_vector[
                ndx : min(ndx + batch_size, l)
            ]  # batch 단위 만큼의 데이터를 반환
