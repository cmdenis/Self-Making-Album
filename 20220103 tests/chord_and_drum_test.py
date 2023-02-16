from notes import *
from effects import *
from sound_generator import *
from math_samples import *
from chord_pattern_maker import *
from drum_maker import *
from notes_maker import *
from pydub import AudioSegment
import os

#np.random.seed(π)

# Initial parameters
bpm = custom_norm(70, 200, 120, 100)
length = 64
time = length*60/bpm + 4
sr = 44100
file_name = "audio_tests/bass_drums_chords_test"
mp3 = True

# Making signals

# Chords
chord_signal = Signal(sr, time, None)
probs = np.array([1, 2, 8, 1, 1])
probs = probs/np.sum(probs)
notes_maker(
    chord_signal,                                   # Signal
    bpm,                                            # BPM
    np.random.randint(0, high = 11),                # Scale
    np.random.choice([2, 3, 4, 5, 6], p = probs),   # Number of chords
    0,                                              # Start beat
    4,                                              # Chord length
    length,                                         # Pattern length
    [sine_synth, saw_synth]                         # Instrument used
)

# Drums
drums_signal = Signal(sr, time, None)
make_4_4_drum(drums_signal, bpm, 0, length, ["bass_drum", "snare_drum", "hi_hat"])

# Master signal
master = Signal(sr, time, file_name+".wav")
master.signal = 6*drums_signal.signal/drums_signal.rms() + chord_signal.signal/chord_signal.rms()
master.save_sound()

if mp3 == True:
    AudioSegment.from_wav(file_name+".wav").export(file_name+".mp3", format="mp3")
    os.remove(file_name+".wav")
