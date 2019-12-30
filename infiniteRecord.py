#!/usr/bin/env python

import sox
import os

'''
Using SoX to record automatically audio from the default microfono just if the audio sensed is above noise level,
create WAV files in MONO encoding called record_ followed by a 3 digit number.. example: record_001.wav, 
record_002.wav, etc. At the end Saving the files in the same root directory
'''


def record_Save():
    os.system(
        "sox -t waveaudio default record_.wav channels 1 silence 1 0.1 1% 1 5.0 1% : newfile : restart")


if __name__ == "__main__":
    record_Save()
