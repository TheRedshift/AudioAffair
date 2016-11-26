"""
Author: Ben Thompson
Date: 2016-11-26
"""
from typing import *
import math


class WaveProcess(object):
    def __init__(self, sample_rate: int, window_period: float, grid_length: int, normalization: float):
        """
        :param sample_rate: the sample rate of the audio file (in Hz)
        :param window_period: the width of the window (i.e. the time in seconds over which the average will be taken)
        :param grid_length: the length of the side of the LED grid
        :param normalization:  the value beyond which all LEDs will be ON
        """

        self._sample_rate = sample_rate
        """
        :type: int
        the sample rate of the audio file (in Hz)
        """

        self._window_period = window_period  # type: float
        """
        :type: float
        the width of the window (i.e. the time in seconds over which the average will be taken)
        """

        self._window = []  # type: List[float]
        """
        :type: List[float]
        stored values for the length of the window
        """

        self._window_samples = int(sample_rate * window_period)  # type: int
        """
        :type: int
        the largest number of samples which fit into the window with the given sample rate
        """

        self._grid_length = grid_length  # type: int
        """
        :type: int
        the length of the side of the LED grid
        """

        self._normalization = normalization  # type: float
        """
        :type:
        the value beyond which all LEDs will be ON
        """

    def update(self, now: float) -> None:
        """
        updates the window contents to include a new value
        :param now: the new/current state to passed into the window. If the window is full the oldest value will be removed
        :return: None
        """
        window = self._window
        window.append(now)
        if len(window) > self._window_samples:
            window.pop(0)

    def get_rms(self) -> float:
        """
        :return: the rms value over the whole window.
        """
        window = self._window
        if len(window) == 0:
            return 0
        else:
            window_squared = [x**2 for x in window]
            rms = math.sqrt(sum(window_squared)/len(window_squared))
            return rms

    def get_square(self) -> List[List[bool]]:
        """
        generates the LED square, with the on square centred and sized proportional to the average of the window

        :return: a 2D array containing the on/off states for each of the LEDs
        """
        rms = self.get_rms()
        grid_length = self._grid_length
        frac = grid_length * rms / self._normalization

        def generate():
            for r in range(grid_length):
                r = r*2 - grid_length
                for c in range(grid_length):
                    c = c*2 - grid_length
                    yield abs(r) < frac and abs(c) < frac

        return [[v for v in r] for r in generate()]

