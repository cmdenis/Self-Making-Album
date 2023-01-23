from notes import Event, Sequence, Multitrack, ChordPattern
from drum_maker import DrumSequence
from melody_maker import MelodySequence
from bass_maker import BassSequence
from chord_maker import ChordSequence
import numpy as np





def make_pattern(bpm, root, instruments, sample_rate):

    
    # Initializes the tracks
    seqs = Multitrack(
        bpm, 
        instruments, 
        ChordPattern(
            np.array([0, 9, 5, 7]) + np.random.randint(11),
            np.array([0, 1, 0, 0]),
            np.array([2, 2, 2, 2])
        ),
        sample_rate
    )

    seqs.make_seqs()

    return seqs


if __name__=="__main__":

    seqs = make_pattern(
        120,
        0,
        [DrumSequence, ChordSequence],
        44100
    )


    