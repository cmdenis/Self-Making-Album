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
    3,                  # Duration (Seconds)
    "audio_tests/drum_test.wav"   # file Name
)

bass_drum(signal, None)


# Save signal
signal.save_sound()
