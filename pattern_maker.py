from notes import *




def make_pattern(bpm, length, root, instruments):

    
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

    # Make patterns
    seqs.make_loop(8)

