from notes import *
from effects import *
from sound_generator import *
from math_samples import *
from chord_pattern_maker import *
from drum_maker import *

np.random.seed(3003)

# Initial parameters
bpm = custom_norm(70, 200, 120, 40)
length = 32
time = length*60/bpm + 4
sr = 44100

# Making signals

# Chords
chord_signal = Signal(sr, time, None)
simple_chord_maker(
    chord_signal,   # Signal
    bpm,            # BPM
    0,              # Scale
    4,              # Number of chords
    0,              # Start beat
    4,              # Chord length
    length,         # Pattern length
    saw_synth       # Instrument used
)

# Drums
drums_signal = Signal(sr, time, None)
make_4_4_drum(drums_signal, bpm, 0, length, ["bass_drum", "snare_drum", "hi_hat"])

# Master signal
master = Signal(sr, time, "audio_tests/chord_and_drum_test.wav")
master.signal = drums_signal.signal + chord_signal.signal/12
master.save_sound()

