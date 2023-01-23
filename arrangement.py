from pattern_maker import *


def make_arrangement():
    '''Function to make the overall multitrack sequence. Returns a MultiSequence object to be used to generate a signal.'''

    # To make things easier, I'll start with a single loop pattern with all instruments playing
    # In the future, I hope to add more parameters, 
    # and to be able to cut down entries and make more than one pattern and that sort of thing.
    root = 0
    instruments = [ChordSequence, DrumSequence]
    length = 2 # Length of pattern in quarter beats
    bpm = np.random.rand()*100+60

    seqs = make_pattern(bpm, root, instruments, 44100)

    seqs.loop_multitrack(length, 0, 8)

    return seqs






    return seqs

if __name__ == "__main__":
    seqs = make_arrangement()
    counter = 0
    for i in seqs.sequences[0].events:
        #print(counter)
        print(i)
        counter += 1
        

    


