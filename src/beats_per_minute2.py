#! /usr/bin/env python

from aubio import source, tempo
from numpy import median, diff

#can access bpms2 array from any file, bpm changes throughout audio file
bpms2 = []

def get_file_bpm(path, params = None):
    """ Calculate the beats per minute (bpm) of a given file.
        path: path to the file
        param: dictionary of parameters
    """
    if params is None:
        params = {}
    try:
        win_s = params['win_s']
        samplerate = params['samplerate']
        hop_s = params['hop_s']
    except KeyError:
        """
        # super fast
        samplerate, win_s, hop_s = 4000, 128, 64
        # fast
        samplerate, win_s, hop_s = 8000, 512, 128
        """
        # default:
        samplerate, win_s, hop_s = 44100, 1024, 512

    s = source(path, samplerate, hop_s)
    samplerate = s.samplerate
    o = tempo("specdiff", win_s, hop_s, samplerate)
    # List of beats, in samples
    beats = []
    # Total number of frames read
    total_frames = 0

    while True:
        samples, read = s()
        is_beat = o(samples)
        if is_beat:
            this_beat = o.get_last_s()
            beats.append(this_beat)
            #if o.get_confidence() > .2 and len(beats) > 2.:
            #    break
        total_frames += read
        if read < hop_s:
            break

    # Convert to periods and to bpm
    if len(beats) > 1:
        if len(beats) < 4:
            print("few beats found in {:s}".format(path))
        bpms = 60./diff(beats)
        for element in bpms:
            print element
            bpms2.append(bpms)
        b = median(bpms)
    else:
        b = 0
        print("not enough beats found in {:s}".format(path))
    return b

def controlLightArray(lightArray):

    x_channel_list = [3, 5, 7, 8, 10, 11, 12, 13]
    y_channel_list = [15, 16, 18, 22]

    lights.updateLEDs(grid, x_channel_list, y_channel_list)

    for element in bpms2:
        flashLEDs(grid, x_channel_list, y_channel_list, element)

def flashLEDs(grid, x, y, beatsPerMinute):
    if(beatsPerMinute > 130):
        lights.directFlashLED(grid, x, y, 0.1)
    elif(beatsPerMinute <= 130 and beatsPerMinute > 110):
        lights.directFlashLED(grid, x, y, 0.3)
    elif(beatsPerMinute <= 110 and beatsPerMinute > 90):
        lights.directFlashLED(grid, x, y, 0.5)
    else:
        lights.directFlashLED(grid, x, y, 0.7)

if __name__ == '__main__':
    import sys
    for f in sys.argv[1:]:
        bpm = get_file_bpm(f)
        for element in bpms2:
            print element
        print("{:6s} {:s}".format("{:2f}".format(bpm), f))