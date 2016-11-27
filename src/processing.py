"""
Author: Ben Thompson
Date: 2016-11-26
"""
from __future__ import division
import math

class WaveProcess(object):
    def __init__(self, sample_rate, window_period, format):
        """
        :param sample_rate: the sample rate of the audio file (in Hz)
        :param window_period: the width of the window (i.e. the time in seconds over which the average will be taken)
        :param grid_length: the length of the side of the LED grid
        :param normalization:  the value beyond which all LEDs will be ON
        """

        self._sample_rate = sample_rate
        """
        the sample rate of the audio file (in Hz)
        """

        self._window_period = window_period
        """
        the width of the window (i.e. the time in seconds over which the average will be taken)
        """

        self._window = []
        """
        stored values for the length of the window
        """

        self._window_samples = int(sample_rate * window_period)
        """
        the largest number of samples which fit into the window with the given sample rate
        """

        self._format = format
        """
        the way in which the grid will be drawn
        """

    def update(self, now):
        """
        updates the window contents to include a new value
        :param now: the new/current state to passed into the window. If the window is full the oldest value will be removed
        :return: None
        """
        window = self._window
        window.append(now)
        if len(window) > self._window_samples:
            window.pop(0)

    def get_square(self):
        return self._format.draw(self._window)


class Format(object):
    def __init__(self, grid_length, normalization):
        self._normalization = normalization
        self._grid_length = grid_length

    def _get_mean(self, window):
        return math.sqrt(sum([x**2 for x in window]) / len(window)) if len(window) > 0 else 0

    def draw(self, window):
        m = self._get_mean(window)
        grid_length = self._grid_length
        low = min(window) if len(window) > 0 else 0
        high = max(window) if len(window) > 0 else 0
        frac = grid_length * (m - low) / (high - low) if (low != high) else (grid_length/2)

        def generate():
            for a in range(grid_length):
                a = a*2 - grid_length + 1
                yield [abs(a) < frac and abs(b*2 - grid_length + 1) < frac for b in range(grid_length)]

        return [[v for v in r] for r in generate()]


class FormatLine(Format):
    def __init__(self, grid_length, normalization, period=15):
        super(FormatLine, self).__init__(grid_length, normalization)
        self._updates = 0
        self._period = period

    def draw(self, window):
        self._updates += 1
        m = self._get_mean(window)
        grid_length = self._grid_length
        frac = int(grid_length * m / self._normalization)

        def generate():
            a = 2*math.pi*self._updates/self._period
            x = [round(v/2 * math.cos(a)) for v in range(-frac, frac)]
            y = [round(v/2 * math.sin(a)) for v in range(-frac, frac)]
            for a in range(grid_length):
                a = a*2 - grid_length + 1
                # a /= 2
                # a = round(a)
                yield [a in x and (b*2 - grid_length + 1) in y for b in range(grid_length)]

        return [[v for v in r] for r in generate()]


# TODO later
# class FormatPulse(Format):
#     def __init__(self, grid_length, normalization):
#         super(FormatPulse, self).__init__(grid_length, normalization)
#         self._pulses = []
#
#     def draw(self, window):
#         pass
