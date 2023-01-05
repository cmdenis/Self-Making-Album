from notes import Event, Sequence, Multitrack, ChordPattern
from drum_maker import DrumSequence
from melody_maker import MelodySequence
from bass_maker import BassSequence
from chord_maker import ChordSequence
import numpy as np





def make_pattern(bpm, root, instruments):

    
    # Initializes the tracks
    seqs = Multitrack(
        bpm, 
        instruments, 
        ChordPattern(
            np.array([0, 7, 5, 9]),
            np.array([0, 0, 0, 1]),
            np.array([2, 2, 2, 2])
        )
    )

    seqs.make_seqs()

    return seqs


if __name__=="__main__":

    seqs = make_pattern(
        120,
        0,
        [DrumSequence]
    )

    '''for ev in seqs.sequences[0].events:
        print("Strinking", ev.message, "at time", ev.start)
'''
    seqs.sequences[0].print_beat()


    