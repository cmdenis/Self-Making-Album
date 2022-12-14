from pattern_maker import *

def make_arrangement():
    '''Function to make the overall multitrack sequence. Returns a MultiSequence object to be used to generate a signal.'''

    # To make things easier, I'll start with a single loop pattern with all instruments playing
    # In the future, I hope to add more parameters, 
    # and to be able to cut down entries and make more than one pattern and that sort of thing.
    root = 0
    instruments = [DrumSequence]
    length = 4 # Length of pattern in quarter beats
    bpm = 60

    seqs = make_pattern(bpm, root, instruments)

    seqs.loop_multitrack(length, 0, 4)

    return seqs






    return seqs

if __name__ == "__main__":
    seqs = make_arrangement()

    seqs.sequences[0].print_beat()


