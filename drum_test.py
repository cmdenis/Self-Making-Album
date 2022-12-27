import numpy as np
from scipy.io.wavfile import write
from scipy.io import wavfile
import scipy.signal as sig
import matplotlib.pyplot as plt
from notes import *
from effects import *
from sound_generator import *
from math_samples import *



signal = Signal(
    44100,              # Sampling rate
    11,                  # Duration (Seconds)
    "audio_tests/drum_test.wav"   # file Name
)

sequence = Sequence(120, 44100)

sequence.play_metronome(
    0,  # Note start
    16, # Note end
    1   # Note length
)

bd = SampleFunction("bass_drum", 2)

play_function(
    signal,
    sequence,
    bd,
    [
        200, # Pitch (Hz)
        5,  # Pitch mod
        0.1,# Pitch decay (s)
        1   # Amp decay (s)
    ],
    choke = True
)


# Save signal
signal.save_sound()
