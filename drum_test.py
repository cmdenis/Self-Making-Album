import numpy as np
from scipy.io.wavfile import write
from scipy.io import wavfile
import scipy.signal as sig
import matplotlib.pyplot as plt
from notes import *
from effects import *
from sound_generator import *
from math_samples import *

#np.random.seed(514)


signal = Signal(
    44100,              # Sampling rate
    11,                  # Duration (Seconds)
    "audio_tests/drum_test.wav"   # file Name
)



# First create HH pattern

sequence = Sequence(
    120,    # BPM
    44100   # Sampling rate
)

'''sequence.play_metronome(
    0,  # Note start
    4, # Note end
    np.random.choice(
        [1, 0.5, 0.25],  # Decide for note lengths of hi-hat
        p = [0.25, 0.5, 0.25]   # more likely to use 8th notes
    ) 
)'''

sequence.make_hihat(0, 4)


sd = SampleFunction("snare_drum", 2)
p_sd = [
    200,    # p[0]: Pitch (Hz)
    1.1,    # p[1]: Pitch mod
    0.1,    # p[2]: Pitch decay (s)
    0.1,    # p[3]: Amp decay (s)
    0.1,    # p[4]: noise decay
    0.5     # p[5]: noise/tone ratio
]

bd = SampleFunction("bass_drum", 2)

hh = SampleFunction("hi_hat", 2)
p_hh = [
    0.01,   # p[0]: Noise decay
    1,    # p[1]: AM mod
    500,    # p[2]: AM frequency
]

'''
play_function(
    signal,
    sequence,
    sd,
    [
        0.2,    # p[0]: Noise Decay
        400,    # p[1]: Tone pitch
        1,      # p[2]: Pitch decay (s)
        0.1,    # p[3]: Pitch Amp decay (s)
        0.1,    # p[4]: pitch mod
        0.5     # p[5]: noise/tone ratio
    ],
    choke = True
)'''


play_function(
    signal,
    sequence,
    hh,
    p_hh,
    choke = True
)


# Save signal
signal.save_sound()
