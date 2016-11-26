"""
Author: Ben Thompson
Date: 2016-11-26
"""
from typing import *
import math


class WaveProcess(object):
    def __init__(self, sample_rate: int, window_period: float, grid_length: int, normalization: float):
        self._sample_rate = sample_rate  # type: int
        self._window_period = window_period  # type: float
        self._window = []  # type: List[float]
        self._window_samples = int(sample_rate * window_period)  # type: int
        self._grid_length = grid_length  # type: int
        self._normalization = normalization  # type: float

    def update(self, now: float) -> None:
        window = self._window
        window.append(now)
        if len(window) > self._window_samples:
            window.pop(0)

    def get_rms(self) -> float:
        window = self._window
        if len(window) == 0:
            return 0
        else:
            window_squared = [x**2 for x in window]
            rms = math.sqrt(sum(window_squared)/len(window_squared))
            return rms

    def get_square(self) -> List[List[bool]]:
        rms = self.get_rms()
        grid_length = self._grid_length
        frac = grid_length * rms / self._normalization

        def generate():
            for r in range(grid_length):
                for c in range(grid_length):
                    yield r < frac and c < frac

        return [[v for v in r] for r in generate()]

