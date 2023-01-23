from notes import Sequence, Event
import numpy as np
from synth import SineSynth


class ChordSequence(Sequence):
    def __init__(self, bpm, chord_pattern, sr):
        super().__init__(bpm, chord_pattern, sr)
        
        self.name = "chords"

        self.sound = np.random.choice([SineSynth])

    def hold_chord(self):
        '''Function to make a pattern of held down chords for one bar at a time.'''

        print("╠ Using 'hold_chord'...")



        # First make the notes in each chords
        chord_selection = self.chord_pattern.chord_notes_selection(
            [48, 72], # Midi notes range
        )

        lengths = self.chord_pattern.lengths        # Lengths of each chords
        starts = np.cumsum(lengths - lengths[0])    # Time of start of each chords
        ends = np.cumsum(lengths)                   # Time of end of each chords

        for start, end, chord in zip(starts, ends, chord_selection):
            for note in chord:
                self.events.append(
                    Event(
                        note,
                        start,
                        end,
                        channel=0
                    )
                )
        
        print("╠═╗")
        print("╚═╝")

    def make_seq(self):
        '''Method to make the sequence of notes'''

        print("╔═══════════════════════╗")
        print("║ Making Chord Sequence ║")
        print("╠═══════════════════════╝")

        # Choose which chord making procedure to make
        method = np.random.choice([self.hold_chord])

        method()

        