from dataclasses import dataclass


@dataclass
class NormalizationParam:
    scale: float
    mean: float | None = None
    std: float | None = None
