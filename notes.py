import mido 
import numpy as np


class Event:
    def __init__(self, midi_note, start, end, message = None):
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

    def shift_notes_beat(self, shift):
        '''Shifts notes by a number of beats'''
        for ev in self.events:
            ev.start += shift*self.beat_time
            ev.end += shift*self.beat_time


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
        for root, idx, bound, chord_time in zip(roots, chord_idx, bounds, chord_times):
            self.play_chord(root, idx, bound, chord_time[0]*self.beat_time, chord_time[1]*self.beat_time)
    
    def play_metronome(self, start_time, end_time, note_length, midi_note = 0):
        '''Plays a single note repeatedly with interval corresponding to note_length. Starts sequence at 'start_time' and ends at 'end_time'.'''

        for shot in np.arange(start_time, end_time, note_length)*self.beat_time:
            self.events.append(
                Event(
                    midi_note,
                    shot,
                    shot+0.01
                )
            )

    def sort_sequence(self, sort_pitch_mode = 'lower_last'):
        '''Function to sort the elements of the sequence temporally. Can be useful for choked percussions.'''
        if sort_pitch_mode == 'lower_last':
            self.events.sort(key = lambda x: x.midi_note)   # Sort by pitch
            self.events.sort(key = lambda x: x.start)       # Sort by time
        elif sort_pitch_mode == 'higher_last':
            self.events.sort(key = lambda x: x.midi_note)
            self.events.sort(key = lambda x: x.start)
        else:
            self.events.sort(key = lambda x: x.start)

    def make_hihat(self, start_time, end_time, extra_note_scaling = 0.25, midi_note = 0):
        '''Method to make hi-hat sequence'''
        print("Making Hi-Hat Sequence...")
        note_length = np.random.choice(
            [1, 0.5, 0.25],         # Decide for note lengths of hi-hat
            p = [0.25, 0.5, 0.25]   # more likely to use 8th notes
        ) 

        # Make usual pattern (with note on each time)
        self.play_metronome(
            start_time, # Note start
            end_time,   # Note end
            note_length,# Note length
            midi_note=midi_note
        )

        # Create a weight that depends on the length of the notes
        weight = (-4*(note_length - 0.7)**2 + 1.15)*extra_note_scaling

        # Add extra random notes in between main notes
        for shot in np.arange(start_time + note_length/2, end_time, note_length)*self.beat_time:
            if np.random.rand() < 0.2*weight and (0<= np.mod(shot, 2) < 1):
                self.events.append(
                    Event(
                        midi_note,
                        shot,
                        shot+0.01
                    )
                )

            elif np.random.rand() < 0.3*weight and (1 <= np.mod(shot, 2) < 1.5):
                self.events.append(
                    Event(
                        midi_note,
                        shot,
                        shot+0.01
                    )
                )

            elif np.random.rand() < 0.4*weight and (1.5 <= np.mod(shot, 2) < 2):
                self.events.append(
                    Event(
                        midi_note,
                        shot,
                        shot+0.01
                    )
                )

    def make_bd(self, start_time, end_time, midi_note = 0):
        '''Making Bass Drum sequence'''
        print("Making Bass Drum Sequence...")

        # Duration of sequence in 8th notes
        duration = int(2*(end_time - start_time))

        # Boolean array to determine if beats are being selected
        beats = np.tile(np.array([
            0.9,    # 1
            0.35,   # 1+
            0.6,    # 2
            0.3,    # 2+
            0.1,    # 3
            0.3,    # 3+
            0.4,    # 4
            0.2     # 4+
        ]), int(np.ceil(duration/8))) > np.random.rand(int(np.ceil(duration/8)*8))


        # Cut down the one-bar beat to proper length
        beats = beats[0:duration]

        # Loop over notes
        for i in np.arange(start_time, end_time, 0.5):
            self.events.append(
                Event(midi_note, (start_time + i)*self.beat_time, (end_time + i)*self.beat_time)
            )
        
        self.events = list(np.array(self.events)[beats])

    def make_sd(self, start_time, end_time, midi_note = 0):
        '''Making Snare Drum sequence'''
        print("Making Snare Drum Sequence...")

        # Duration of sequence in 8th notes
        duration = int(2*(end_time - start_time))

        # Boolean array to determine if beats are being selected
        probs = np.array([
            0.05,    # 1
            0.10,   # 1+
            0.05,    # 2
            0.05,    # 2+
            0.98,    # 3
            0.05,    # 3+
            0.2,    # 4
            0.2     # 4+
        ])
        beats = np.tile(probs, int(np.ceil(duration/8))) > np.random.rand(int(np.ceil(duration/8)*8))

        # Cut down the one-bar beat to proper length
        beats = beats[0:duration]

        # Loop over notes
        for i in np.arange(start_time, end_time, 0.5):
            self.events.append(
                Event(midi_note, (start_time + i)*self.beat_time, (end_time + i)*self.beat_time)
            )
        
        self.events = list(np.array(self.events)[beats])


    def loop_sequence(self, n, start_time, end_time):
        '''Method to loop a section n times after it has occured.
        This will overwrite whatever occurs in the looping time region.'''

        # Should not be needed, I think...
        self.sort_sequence()

        # Duration of the loop
        loop_duration = end_time-start_time

        # Copy events before emptying the list
        all_events = self.events.copy()
        self.events = []

        # Iterate over events
        for ev in all_events:

            # If events are in desired loop range, loop them over different times
            if start_time <= ev.start < end_time:
                for i in range(n):
                    self.events.append(
                        Event(
                            ev.midi_note,
                            ev.start + i * loop_duration,
                            ev.end + i * loop_duration
                        )
                    )

            # If events are not part of loop, simply append them to event list
            elif start_time + loop_duration * n < ev.start or ev.start < start_time:
                self.events.append(ev)


            




        




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
