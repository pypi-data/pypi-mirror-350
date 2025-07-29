from ._normalization_param import NormalizationParam
from ._single_normalizer import SingleNormalizer
from ._multi_normalizer import MultiNormalizer


class NormalizerFactory:
    __factory_map = {
        "gray-basic": SingleNormalizer(NormalizationParam(255.0)),
        "gray-gan": SingleNormalizer(NormalizationParam(255.0, 0.5, 0.5)),
        "color-basic": MultiNormalizer([NormalizationParam(255.0) for _ in range(3)]),
        "color-gan": MultiNormalizer(
            [NormalizationParam(255.0, 0.5, 0.5) for _ in range(3)]
        ),
        "color-imagenet": MultiNormalizer(
            [
                [
                    NormalizationParam(255.0, 0.485, 0.229),
                    NormalizationParam(255.0, 0.456, 0.224),
                    NormalizationParam(255.0, 0.406, 0.225),
                ][i % 3]
                for i in range(3)
            ]
        ),
    }

    @classmethod
    def create(cls, key: str) -> MultiNormalizer | SingleNormalizer:
        return cls.__factory_map[key]

    @classmethod
    def create_single(cls, key: str) -> SingleNormalizer:
        normalizer = cls.__factory_map[key]
        assert (
            type(normalizer) == SingleNormalizer
        ), f"ERROR, the normalizer for {key} must be {SingleNormalizer.__name__}"
        return normalizer

    @classmethod
    def create_multi(cls, key: str) -> MultiNormalizer:
        normalizer = cls.__factory_map[key]
        assert (
            type(normalizer) == MultiNormalizer
        ), f"ERROR, the normalizer for {key} must be {MultiNormalizer.__name__}"
        return normalizer
