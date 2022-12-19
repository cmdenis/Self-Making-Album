import mido 
import numpy as np


class Event:
    def __init__(self, midi_note, start, end):
        # Handling possible misuse cases
        if start > end:
            raise NameError("Starting Time is After End Time...")
        if start < 0:
            raise NameError("Starting Time Before 0...")
        #if end > length:
        #    raise NameError("Ending time greater than duration of the song...")

        
        # Initializing attributes
        self.midi_note = midi_note                  # Midi note
        self.pitch = 440*2**((midi_note - 69)/12)   # Pitch of sound (Hz)
        self.start = start                          # Time of start of sound
        self.end = end                              # Time of end of sound
        #self.modulation = modulation               # Array with modulation data, WIP

class Scale:
    '''Class to create a scale that can then conveniently bbe used to make music.'''
    def __init__(self, intervals, root):

        # For the intervals:
        # 0: Root
        # 1: 1 semi-tone above root
        # 2: 2 semi-tones above root
        # ...
        # 11: 11 semi-tones above root


        # For root, use the number corresponding to the note in the scale, C is 0, C# is 1, etc.

        # Check if the given intervals are contained within
        if np.max(intervals) > 11:
            print("Warning: Interval list is larger than octave. Notes above octave will get converted to fit within octave.")

        # Makes notes fit in an octave and finds non-repeated notes
        self.intervals = np.unique(np.mod(intervals, 12))
        self.nb_notes = len(self.intervals)

        # Creates array of octaves that each contain the notes from the scale
        self.octaves = np.empty([10, self.nb_notes])
        for idx, i in enumerate(self.octaves):
            self.octaves[idx] = self.intervals + idx*12

        self.octaves += root

def play_random(scale, bounds, nb, dt):
    '''Function that just plays random notes (each as a whole note) in a scale, with a certain range.'''
    np.random.seed(514)

    track = []

    for i in range(nb):
        note_choice = np.ndarray.flatten(scale.octaves)               # Flatten array with all possible note choices
        note_choice = note_choice[note_choice > bounds[0]]    # Notes within range
        note_choice = note_choice[note_choice < bounds[1]]    # Notes within range
        selected = np.random.choice(note_choice)              # Random selection of notes within range

        track.append(
            Event(selected, dt*i, dt*(i+1))       # Appending note on to track
        )

    return track






if __name__ == "__main__":

    major = Scale(np.array([0, 2, 4, 5, 7, 9, 11]), 0)

    print(np.ndarray.flatten(major.octaves))

    sequence = play_random(
        major,
        [48, 84],
        8,
        0.5
    )

    print(sequence)

                




            


    def test_notes():
        mido.Message('note_on', note=50, velocity=3, time=6.2)
        return 1
