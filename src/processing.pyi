"""
Author: Ben Thompson
Date: 2016-11-26
"""
from typing import *

def get_output(wave: List[float]) -> List[List[float]]:
    """
    :param wave: the sliding waveform to be processed. Pass only the slice to be used for current diode illumination
    :return: a 2D array of booleans corresponding to the on/off state of the LED on the grid
    """
    ...