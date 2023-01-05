from notes import *
from drum_maker import *




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

    # Circulates around the different instruments and creates the sequence based on the instrument
    for instrument, seq in zip(seqs.instruments, seqs.sequences):

        if instrument == "chords":
            make_chords(seq, seqs.chord_pattern, length)
        elif instrument == "bass":
            make_bass(seq, seqs.chord_pattern, length)
        elif instrument == "melody":
            make_melody(seq, seqs.chord_pattern, length)
        elif instrument == "drum":
            make_drum(seq, ["bass_drum", "snare_drum", "hi_hat"])


if __name__=="__main__":

    make_pattern(
        120,
        4,
        0,
        ["drum", "chords", "bass"]
    )