#! /usr/bin/env python

from sys import exit

def pitchreader (filename, sameplerate):

    from aubio import source, pitch

    downsample = 1

    win_s = 4096 // downsample
    hop_s = 512 // downsample

    s = source('test.wav', sameplerate, hop_s)
    samplerate = s.samplerate

    tolerance = 0.8

    pitch_o = pitch("yin", win_s, hop_s, samplerate)
    pitch_o.set_unit("midi")
    pitch_o.set_tolerance(tolerance)

    pitches = []
    confidences = []

    totalFrames = 0

    while True:
        samples, read = s()
        pitch = pitch_o(samples)[0]
        # pitch = int(round(pitch))
        confidence = pitch_o.get_confidence()
        print("%f %f" % (totalFrames / float(samplerate), pitch))
        pitches += [pitch]
        confidences += [confidence]
        totalFrames += read
        if read < hop_s: break

pitchreader('a', 44100)
