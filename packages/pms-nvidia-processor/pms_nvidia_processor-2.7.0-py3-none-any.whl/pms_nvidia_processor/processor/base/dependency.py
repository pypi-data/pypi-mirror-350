from typing import (
    Literal,
    TypeVar,
    Generic,
)
from abc import ABCMeta, abstractmethod, ABC
from dataclasses import dataclass
import os
import time
import uvloop
import asyncio
import numpy as np
import loguru
import enum
from itertools import chain
import cv2
import pms_tensorrt as TRT
from pms_inference_engine import IEngineProcessor, EngineIOData, register

InputTypeT = TypeVar("InputTypeT")
OutputTypeT = TypeVar("OutputTypeT")
