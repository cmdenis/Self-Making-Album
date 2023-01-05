from notes import Sequence
import numpy as np

class ChordSequence(Sequence):

    def __init__(self, bpm, chord_pattern):
        super().__init__(bpm, chord_pattern)
        self.name = "chords"
        