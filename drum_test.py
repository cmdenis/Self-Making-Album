import numpy as np
from scipy.io.wavfile import write
from scipy.io import wavfile
import scipy.signal as sig
import matplotlib.pyplot as plt
from notes import *
from effects import *
from sound_generator import *
from math_samples import *

np.random.seed(5401)


signal = Signal(
    44100,              # Sampling rate
    11,                  # Duration (Seconds)
    "audio_tests/drum_test.wav"   # file Name
)

final_beat = 4
bpm = 140
sample_rate = 44100


# First create HH pattern
hh_sequence = Sequence(
    bpm,    # BPM
    44100   # Sampling rate
)

# Make 1 bar sequence
hh_sequence.make_hihat(0, final_beat)

# Loop the sequence 4 times
hh_sequence.loop_sequence(4, 0, final_beat*60/bpm)



hh = SampleFunction("hi_hat", 2, sample_rate)
p_hh = [
    0.005,   # p[0]: Noise decay
    1,      # p[1]: AM mod
    1000,    # p[2]: AM frequency
]

play_function(
    signal,
    hh_sequence,
    hh,
    p_hh,
    choke = True
)


# bass drum pattern
bd_sequence = Sequence( # Initialize sequence
    bpm,                # BPM
    sample_rate         # Sampling rate
)

#bd_sequence.play_metronome(0, final_beat, 1)    # Make beats

bd_sequence.make_bd(0, final_beat)

# Loop the sequence 4 times
bd_sequence.loop_sequence(4, 0, final_beat*60/bpm)

bd = SampleFunction("bass_drum", 2, sample_rate) # Initialize sample
p_bd = [
    30,    # p[0]: Pitch (Hz)
    7,    # p[1]: Pitch mod
    0.05,    # p[2]: Pitch decay (s)
    0.5,    # p[3]: Amp decay (s)
]

play_function(  # Play sample
    signal,
    bd_sequence,
    bd,
    p_bd,
    choke = False
)

'''
# Make snare drum

sd_sequence = Sequence( # Initialize sequence
    bpm,    # BPM
    44100   # Sampling rate
)
sd_sequence.play_metronome(2, final_beat, 4)    # Make beats

sd = SampleFunction("snare_drum", 2, sample_rate)
p_sd = [
    400,    # p[0]: Pitch (Hz)
    2,    # p[1]: Pitch mod
    0.1,    # p[2]: Pitch decay (s)
    0.1,    # p[3]: Amp decay (s)
    0.07,    # p[4]: noise decay
    0.5     # p[5]: noise/tone ratio
]

play_function(
    signal,
    sd_sequence,
    sd,
    [
        200,    # p[0]: Pitch (Hz)
        1.05,    # p[1]: Pitch mod
        0.1,    # p[2]: Pitch decay (s)
        0.08,    # p[3]: Pitch Amp decay (s)
        0.08,    # p[4]: Noise decay
        0.5     # p[5]: noise/tone ratio
    ],
    choke = False
)

# p[0]: Pitch (Hz)
            # p[1]: Pitch mod
            # p[2]: Pitch decay (s)
            # p[3]: Amp decay (s)
            # p[4]: Noise decay
            # p[5]: noise/tone ratio
'''
# Save signal
signal.save_sound()
