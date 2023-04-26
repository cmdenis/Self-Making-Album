from pattern_maker import *




def make_arrangement():
    '''Function to make the overall multitrack sequence. Returns a MultiSequence object to be used to generate a signal.'''

    # To make things easier, I'll start with a single loop pattern with all instruments playing
    # In the future, I hope to add more parameters, 
    # and to be able to cut down entries and make more than one pattern and that sort of thing.
    root = 0
    #instruments = [DrumSequence, BassSequence, MelodySequence, ChordSequence]
    instruments = []
    orch = [
            [DrumSequence, BassSequence, MelodySequence, ChordSequence],
            [DrumSequence, DrumSequence, MelodySequence, ChordSequence], 
            [DrumSequence, DrumSequence, MelodySequence],
            [DrumSequence, DrumSequence, BassSequence, MelodySequence, ChordSequence],
            [BassSequence, MelodySequence, ChordSequence]
        ]
    instruments = orch[np.random.choice([0, 1, 2, 3, 4])]
    

    '''# Deciding how many drums:
    for i in range(np.random.choice([0, 1, 2, 3], p = [0.22, 0.75, 0.02, 0.01])):
        instruments.append(DrumSequence)

    # Deciding how many chord makers
    for i in range(np.random.choice([0, 1, 2, 3], p = [0.22, 0.75, 0.02, 0.01])):
        instruments.append(ChordSequence)

    # Deciding how many basses
    for i in range(np.random.choice([0, 1, 2, 3], p = [0.06, 0.91, 0.02, 0.01])):
        instruments.append(BassSequence)

    # Deciding how many melodies
    for i in range(np.random.choice([0, 1, 2, 3], p = [0.1, 0.87, 0.02, 0.01])):
        instruments.append(MelodySequence)'''



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
        

    


