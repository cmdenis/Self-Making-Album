import numpy as np
from scipy.io.wavfile import write
from scipy.io import wavfile
import scipy.signal as sig
import matplotlib.pyplot as plt
from notes import *
from effects import *
from sound_generator import *



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

bass_drum(
    signal,
    sequence,
    1,  # Length (s)
    40, # Pitch (Hz)
    6,  # Pitch mod
    0.1,# Pitch decay (s)
    0.2   # Amp decay (s)
)

# Save signal
signal.save_sound()
