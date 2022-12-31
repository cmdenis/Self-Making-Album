from notes import *
from effects import *
from sound_generator import *
from math_samples import *
from chord_pattern_maker import *
from drum_maker import *
from pydub import AudioSegment
import os

np.random.seed(71)

# Initial parameters
bpm = custom_norm(70, 200, 120, 40)
length = 32
time = length*60/bpm + 4
sr = 44100
file_name = "audio_tests/chord_and_drum_test"
mp3 = True

# Making signals

# Chords
chord_signal = Signal(sr, time, None)
probs = np.array([1, 2, 8, 1, 1])
probs = probs/np.sum(probs)
simple_chord_maker(
    chord_signal,                                   # Signal
    bpm,                                            # BPM
    np.random.randint(0, high = 11),                # Scale
    np.random.choice([2, 3, 4, 5, 6], p = probs),   # Number of chords
    0,                                              # Start beat
    4,                                              # Chord length
    length,                                         # Pattern length
    saw_synth                                       # Instrument used
)

# Drums
drums_signal = Signal(sr, time, None)
make_4_4_drum(drums_signal, bpm, 0, length, ["bass_drum", "snare_drum", "hi_hat"])

# Master signal
master = Signal(sr, time, file_name+".wav")
master.signal = drums_signal.signal + chord_signal.signal/12
master.save_sound()

if mp3 == True:
    AudioSegment.from_wav("audio_tests/chord_and_drum_test"+".wav").export("audio_tests/chord_and_drum_test"+".mp3", format="mp3")
    os.remove(file_name+".wav")
