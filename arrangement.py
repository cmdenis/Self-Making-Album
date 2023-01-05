from pattern_maker import *

def make_arrangement():
    '''Function to make the overall multitrack sequence. Returns a MultiSequence object to be used to generate a signal.'''

    # To make things easier, I'll start with a single loop pattern with all instruments playing
    # In the future, I hope to add more parameters, 
    # and to be able to cut down entries and make more than one pattern and that sort of thing.
    root = 0
    instruments = ["bass_drum"]
    length = 4 # Length of pattern in quarter beats
    bpm = 120

    seqs = make_pattern(bpm, root, instruments)

    seqs.loop_multitrack(2, 0, length)






    return seqs