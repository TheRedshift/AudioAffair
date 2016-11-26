#!/usr/bin/python
DOC = ''' This program detects bpm for mp3 files. It relies on soundstretch being installed on your system.

Usage:
    %s <filename>
-or pipe filenames to it.

Example:
    find . -name "*.mp3"| %s\n''' % (__file__, __file__)

import os
import pipes
import select
import subprocess
import sys

## Define the window for sane bpm values. This may depend on genre of music. ##
BPM_WINDOW_MAX = 240
# Do not change this one
BPM_WINDOW_MIN = BPM_WINDOW_MAX / 2

def _get_bpm_from_soundstretch(output):
    """Gets bpm value from soundstretch output"""

    output = output.split(bytes('\n', 'utf-8'))
    for line in output:
        if bytes('Detected BPM rate ', 'utf-8') in line:
            bpm = line[18:]
            return float(bpm)
    return None  # Could not parse output

def fit_bpm_in_window(bpm_suggestion):
    """Double or halve a bpm suggestion until it fits inside the bpm window"""

    if bpm_suggestion is not None:
        while bpm_suggestion < (BPM_WINDOW_MIN):
            bpm_suggestion = bpm_suggestion * 2
        while bpm_suggestion > (BPM_WINDOW_MAX):
            bpm_suggestion = bpm_suggestion / 2
    return bpm_suggestion

def analyze_mp3(mp3filespec):
    "Uses soundstretch to analyze an mp3 file for its bpm rate"

    # Call soundstretch to analyze the wav file
    bpm_command = 'soundstretch %s -bpm' % mp3filespec
    p = subprocess.Popen([bpm_command], shell=True, stdout=subprocess.PIPE)
    output = p.communicate()[0]

    bpm_suggestion = _get_bpm_from_soundstretch(output)

    return fit_bpm_in_window(bpm_suggestion)

def process_input(mp3filespec):
    bpm_suggestion = analyze_mp3(pipes.quote(mp3filespec))
    if bpm_suggestion is None:
        print
        "Unable to detect bpm for file %s" % mp3filespec
    else:
        print
        "BPM rate for %s is estimated to be %s" % (mp3filespec, bpm_suggestion)

if __name__ == "__main__":
    mp3filespec = input()
    mp3filespec = os.path.abspath(mp3filespec)
    process_input(mp3filespec)

    #include functionality to change light array + split wav file into pieces