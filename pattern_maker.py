from notes import Event, Sequence, Multitrack, ChordPattern
from drum_maker import DrumSequence
from melody_maker import MelodySequence
from bass_maker import BassSequence
from chord_maker import ChordSequence
import numpy as np

#np.random.seed(2)

def hard_coded_patterns():
    '''User defined chord progression to be randomly selected from.'''
    print("Using Hard coded presets")
    choices = [
        ChordPattern(
            np.mod(np.array([0, 9, 5, 7]) + np.random.randint(11), 12),
            np.array([0, 1, 0, 0]),
            np.array([2, 2, 2, 2])
        ),
        ChordPattern(
            np.mod(np.array([0, 5, 7]) + np.random.randint(11), 12),
            np.array([0, 0, 0]),
            np.array([4, 4, 8])
        ),
        ChordPattern(
            np.mod(np.array([0, 5, 7, 2]) + np.random.randint(11), 12),
            np.array([0, 0, 0, 0]),
            np.array([4, 4, 4, 4])
        ),

        ChordPattern(
            np.mod(np.array([0, 4, 7, 11]) + np.random.randint(11), 12),
            np.array([0, 1, 0, 1]),
            np.array([4, 4, 4, 4])
        ),
        ChordPattern(
            np.mod(np.array([0, 10, 5]) + np.random.randint(11), 12),
            np.array([0, 0, 0]),
            np.array([2, 2, 4])
        ),
        ChordPattern(
            np.mod(np.array([0, 5, 3, 2]) + np.random.randint(11), 12),
            np.array([5, 5, 5, 0]),
            np.array([2, 2, 2, 2])
        ),
    ]

    return np.random.choice(choices)



def completly_random_patterns():
    '''Makes random chord pattern'''
    print("Using Random Pattern Generator:")
    length_prob = np.array([1, 5, 10, 20, 10, 8])
    pat_length = np.random.choice([1, 2, 3, 4, 5, 6], p = length_prob/np.sum(length_prob))
    roots = np.mod(
            np.random.randint(
                0, 
                high = 11, 
                size = pat_length,
            ) + np.random.randint(11), 12
        )



    chords = np.random.choice([0, 1, 2, 3], size = pat_length)

    lengths = np.random.choice([4, 2], size=pat_length, p = [0.95, 0.05])

    print("Roots:", roots)
    print("Chords:", chords)
    print("Lengths:", lengths)
    print()
    return ChordPattern(roots, chords, lengths)
   




def make_pattern(bpm, root, instruments, sample_rate):

    # Select a mode for getting chord pattern
    mode = np.random.choice(
        [hard_coded_patterns,
        completly_random_patterns], p = [0.3, 0.7]
    )
    
    # Initializes the tracks
    seqs = Multitrack(
        bpm, 
        instruments, 
        mode(),
        sample_rate
    )

    seqs.make_seqs()

    return seqs


if __name__=="__main__":

    seqs = make_pattern(
        120,
        0,
        [DrumSequence, ChordSequence, BassSequence],
        44100
    )


    