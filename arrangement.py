from pattern_maker import *




def make_arrangement():
    '''Function to make the overall multitrack sequence. Returns a MultiSequence object to be used to generate a signal.'''

    # To make things easier, I'll start with a single loop pattern with all instruments playing
    # In the future, I hope to add more parameters, 
    # and to be able to cut down entries and make more than one pattern and that sort of thing.
    root = 0
    instruments = [MelodySequence, ChordSequence, BassSequence, DrumSequence]
    bpm = np.random.rand()*100+40

    seqs = make_pattern(bpm, root, instruments, 44100)

    length = seqs.chord_pattern.pat_length # Length of pattern in quarter beats


    seqs.loop_multitrack(2, 0, length)

    return seqs

if __name__ == "__main__":
    seqs = make_arrangement()
    counter = 0
    for i in seqs.sequences[0].events:
        #print(counter)
        #print(i)
        counter += 1
        

    


