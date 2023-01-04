import numpy as np
from scipy.io.wavfile import write
import scipy.signal as sig
import matplotlib.pyplot as plt
from notes import *
from effects import *
from sound_generator import *
np.random.seed(911)

# Script to make a random sequence based on the random note generator


# Global signal
    
signal = Signal(
    44100,              # Sampling rate
    5,                  # Duration (Seconds)
    "audio_tests/random_substractive_synth.wav"   # file Name
)


# Make major scale
major = Scale(np.array([0, 2, 4, 5, 7, 9, 11]), 0)

# Obtain sequence of notes
sequence = play_random(
    major,
    [48, 84],
    8,
    0.5
)

# Create sine sequence  
substractive_synth_1(sequence, signal, 2000, [0.5, 0.5, 0.5, 0.5], 'saw', 'saw', pitch_1 = 2, pitch_2 = -2)

# Add some reverb
#signal = reverb(signal, 1, 0.5, new_ir = True)

# Add a LP Filter
#signal = lowpass(signal, filter_type="gaussian")


# Save signal
signal.save_sound()
