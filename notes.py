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

class Sequence:
    '''Class for the sequence of events'''
    def __init__(self, bpm, sr):
        self.bpm = bpm              # Beats per mins
        self.sr = sr                # Sample rate
        self.beat_time = 60/bpm     # Duration of a whole note (in seconds)

        self.events = []

    def play_random(self, scale, start_beat, bounds, nb, note_length = 1):
        '''Function that just plays random notes (each as a whole note) in a scale, with a certain range.'''

        for i in range(nb):
            note_choice = np.ndarray.flatten(scale.octaves)                 # Flatten array with all possible note choices
            note_choice = note_choice[note_choice > bounds[0]]              # Notes within range
            note_choice = note_choice[note_choice < bounds[1]]              # Notes within range
            selected = np.random.choice(note_choice)                        # Random selection of notes within range

            self.events.append(
                Event(selected, self.beat_time*start_beat + i*note_length, self.beat_time*(i+1)*note_length)       # Appending note on to track
            )

    def play_chord(self, root, chord_idx, bounds, chord_start, chord_duration):
        scale = Scale(np.array([0]), root)
        note_choice = np.ndarray.flatten(scale.chord_scale_list[chord_idx])     # Flatten array with all possible note choices
        note_choice = note_choice[note_choice > bounds[0]]                      # Notes within range
        note_choice = note_choice[note_choice < bounds[1]]                      # Notes within range

        # Cycle through notes in chord and adding events
        for note in note_choice:
            self.events.append(
                Event(
                    note, 
                    self.beat_time*chord_start, 
                    self.beat_time*(chord_start + chord_duration)
                    )      # Appending note on to sequence
            )


    def play_chord_sequence(self, roots, chord_idx, bounds, chord_times):
        nb_chords = len(roots)
        for root, idx, bound, chord_time in zip(roots, chord_idx, bounds, chord_times):
            self.play_chord(root, idx, bound, chord_time[0]*self.beat_time, chord_time[1]*self.beat_time)




class Scale:
    '''Class to create a scale that can then conveniently be used to make music.'''
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

        # Makes set of midi notes based on given intervals
        def make_octaves(notes):
            # Creates array of octaves that each contain the notes from the scale
            octaves = np.empty([10, len(notes)])
            for idx, i in enumerate(octaves):
                octaves[idx] = notes + idx*12
            return octaves
        self.octaves = make_octaves(self.intervals)

        self.octaves += root

        self.root = root


        # Create chords
        self.C = np.array([0, 4, 7])                # C
        self.Cm = np.array([0, 3, 7])               # Cm
        self.C7 = np.array([0, 4, 7, 10])           # C7
        self.Cm7 = np.array([0, 3, 7, 10])          # Cm7
        self.Cm7b5 = np.array([0, 3, 6, 10])        # Cm7b5
        self.Cmaj7 = np.array([0, 4, 7, 11])        # Cmaj7
        self.Csus4 = np.array([0, 5, 7])            # Csus4
        self.Csus2 = np.array([0, 2, 7])            # Csus2
        self.Cadd2 = np.array([0, 2, 4, 7])         # Cadd9/Cadd2
        self.Cdim = np.array([0, 3, 6])             # Cdim
        self.Cdim7 = np.array([0, 2, 7, 9])         # Cdim7
        self.CmM7 = np.array([0, 2, 7, 11])         # CmM7
        self.Caug = np.array([0, 4, 8])             # Caug
        self.Caug7 = np.array([0, 4, 8, 10])        # Caug7
        self.C6 = np.array([0, 4, 7, 9])            # C6
        self.Cm6 = np.array([0, 3, 7, 9])           # Cm6
        self.C6_9 = np.array([0, 2, 4, 7, 9])       # C6/9
        self.C5 = np.array([0, 5])                  # C5
        self.C9 = np.array([0, 2, 4, 7, 10])        # C9
        self.Cm9 = np.array([0, 2, 3, 7, 10])       # Cm9
        self.Cmaj9 = np.array([0, 2, 4, 7, 11])     # Cmaj9
        self.C11 = np.array([0, 2, 4, 5, 7, 10])    # C11
        self.Cm11 = np.array([0, 2, 3, 5, 7, 10])   # Cm11

        # List of chords
        self.chord_list = [
            self.C, 
            self.Cm, 
            self.C7, 
            self.Cm7,
            self.Cm7b5,
            self.Cmaj7,
            self.Csus4,
            self.Csus2,
            self.Cadd2,
            self.Cdim,
            self.Cdim7,
            self.CmM7,
            self.Caug,
            self.Caug7,
            self.C6,
            self.Cm6,
            self.C6_9,
            self.C5,
            self.C9,
            self.Cm9,
            self.Cmaj9,
            self.C11,
            self.Cm11
        ]

        # Make midi notes list for all chords
        self.chord_scale_list = []
        for i in self.chord_list:
            self.chord_scale_list.append(make_octaves(i) + self.root)
            
    




    def transpose(self, shift):
        # Re-instantiate scale object
        self = Scale(self.intervals, self.root + np.mod(shift, 12))


def play_random(scale, bounds, nb, dt):
    '''Function that just plays random notes (each as a whole note) in a scale, with a certain range.'''

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
