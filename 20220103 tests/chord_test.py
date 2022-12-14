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
    5,                  # Duration (Seconds)
    "audio_tests/beat_chord_test.wav"   # file Name
)


# Make major scale
major = Scale(np.array([0, 2, 4, 5, 7, 9, 11]), 2)

# Obtain sequence of notes
sequence = Sequence(150, 44100)
chords = [
    0,
    5,
    4,
    1
]
roots = [
    0, 2, 5, 9
]

bounds = [
    [60, 77],
    [60, 77],
    [60, 77],
    [60, 77]
]

times = [
    [0, 4],
    [4, 4],
    [8, 4],
    [12, 4]
]


sequence.play_chord_sequence(roots, chords, bounds, times)

# Create sine sequence  
saw_synth(sequence.events, signal)

# Add some reverb
#signal = reverb(signal, 1, 0.5, new_ir = True)

# Add a LP Filter
#signal = lowpass(signal, filter_type="gaussian")


# Save signal
signal.save_sound()
