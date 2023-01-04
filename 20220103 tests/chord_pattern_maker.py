import numpy as np
import copy
from scipy.io.wavfile import write
from scipy.io import wavfile
import scipy.signal as sig
import matplotlib.pyplot as plt
from notes import *
from effects import *
from sound_generator import *
from math_samples import *


def simple_chord_maker(sig, bpm, scale, nb_chords, start_beat, chord_length, length, instrument):
    '''Function to make a simple chord pattern.'''

    # Obtain sequence of notes
    seq = Sequence(bpm, sig.samplerate)

    # Root notes
    roots = np.random.choice(
        [0, 2, 4, 5, 7, 9],
        size=nb_chords
    )
    roots = np.mod(roots + scale, 12)

    # Chords
    chords = np.random.randint(0, high=4, size=nb_chords)

    # Creating bounds for midi notes
    low_bound = custom_norm(20, 80, 60, 8)
    high_bound = low_bound + custom_norm(10, 40, 17, 8)
    bounds = np.tile(
        np.array([low_bound, high_bound]),
        (4, 1)
    )

    # Case: larger length than chord length
    if length > chord_length:
        launches = int(np.floor(length/chord_length))
        remainder = length/chord_length - launches
        times = []
        # Append starting times of chords
        for i in range(launches):
            times.append([i*chord_length + start_beat, chord_length])
        # Add last chord
        if remainder != 0:
            times.append([launches*chord_length + start_beat, chord_length*remainder])

        # Tile up the other arrays so that the number of events matches up
        n = int(np.ceil((launches + 1)/nb_chords))
        cut = int(np.ceil(length/chord_length))
        roots = np.tile(roots, n)[0:cut]
        bounds = np.tile(bounds, (n,1))[0:cut]
        chords = np.tile(chords, n)[0:cut]

    # Case: smaller length than chord length
    elif length <= chord_length:
        times = [[start_beat, length]]
        roots = roots[0:1]
        bounds = bounds[0:1]
        chords = chords[0:1]


    if not (len(roots) == len(chords) == len(bounds) == len(times)):
        raise ValueError("Lengths of roots, chords, bounds and times are not the same in 'simple_chord_maker'!")
    
    seq.play_chord_sequence(roots, chords, bounds, times)

    # Create sine sequence  
    instrument(seq.events, sig)



if __name__=="__main__":
    # Initial parameters
    bpm = 120
    length = 4
    time = length*60/bpm + 4

    # Making signals
    signal = Signal(44100, time, "audio_tests/chord_pattern_test.wav")
    simple_chord_maker(signal, bpm, 0, 4, 0, 4, length, saw_synth)

    # Storing signal
    signal.save_sound()