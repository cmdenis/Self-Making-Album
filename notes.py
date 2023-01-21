import numpy as np


class Event:
    '''Class for note events. Contains info about pitch, start and length of the notes.'''
    def __init__(self, midi_note, start, end, channel, message = None):
        # Handling possible misuse cases
        if start > end:
            raise NameError("Starting Time is After End Time...")
        if start < 0:
            raise NameError("Starting Time Before 0...")

        # Initializing attributes
        self.midi_note = midi_note                  # Midi note
        self.pitch = 440*2**((midi_note - 69)/12)   # Pitch of sound (Hz)
        self.start = start                          # Time of start of sound
        self.end = end                              # Time of end of sound
        self.channel = channel
        self.message = message


class Sequence:
    '''Class for the sequence of events.'''

    def __init__(self, bpm, chord_pattern, sr):
        self.bpm = bpm              # Beats per mins
        self.sr = sr                # Sample rate
        self.beat_time = 60/bpm     # Duration of a whole note (in seconds)
        self.chord_pattern = chord_pattern
        self.events = []

    def shift_notes_beat(self, shift):
        '''Shifts notes by a number of beats'''
        for ev in self.events:
            ev.start += shift*self.beat_time
            ev.end += shift*self.beat_time

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

    def loop_sequence(self, n, start_time, end_time):
        '''Method to loop a section n times after it has occured.
        This will overwrite whatever occurs in the looping time region.'''

        # Should not be needed, I think...
        self.sort_sequence()


        # Duration of the loop
        loop_duration = (end_time-start_time)*self.beat_time
    

        # Copy events before emptying the list
        all_events = self.events.copy()
        self.events = []

        # Iterate over events
        for ev in all_events:

            # If events are in desired loop range, loop them over different times
            if start_time*self.beat_time <= ev.start < end_time*self.beat_time:
                for i in range(n):
                    self.events.append(
                        Event(
                            ev.midi_note,
                            ev.start + i * loop_duration,
                            ev.end + i * loop_duration,
                            ev.channel
                        )
                    )

            # If events are not part of loop, simply append them to event list
            elif start_time + loop_duration * n <= ev.start or ev.start < start_time:
                self.events.append(ev)



class ChordPattern:
    '''Class for chord pattern object'''
    def __init__(self, roots, chords, lengths):

        self.roots = roots      # Array with roots of chords used
        #self.chords = chords    # Array with chords used
        self.chords = []
        self.lengths = lengths  # Array with lengths of chords
        
        # Create chords
        self.C = np.array([0, 4, 7])                # X
        self.Cm = np.array([0, 3, 7])               # Xm
        self.C7 = np.array([0, 4, 7, 10])           # X7
        self.Cm7 = np.array([0, 3, 7, 10])          # Xm7
        self.Cm7b5 = np.array([0, 3, 6, 10])        # Xm7b5
        self.Cmaj7 = np.array([0, 4, 7, 11])        # Xmaj7
        self.Csus4 = np.array([0, 5, 7])            # Xsus4
        self.Csus2 = np.array([0, 2, 7])            # Xsus2
        self.Cadd2 = np.array([0, 2, 4, 7])         # Xadd9/Cadd2
        self.Cdim = np.array([0, 3, 6])             # Xdim
        self.Cdim7 = np.array([0, 2, 7, 9])         # Xdim7
        self.CmM7 = np.array([0, 2, 7, 11])         # XmM7
        self.Caug = np.array([0, 4, 8])             # Xaug
        self.Caug7 = np.array([0, 4, 8, 10])        # Xaug7
        self.C6 = np.array([0, 4, 7, 9])            # X6
        self.Cm6 = np.array([0, 3, 7, 9])           # Xm6
        self.C6_9 = np.array([0, 2, 4, 7, 9])       # X6/9
        self.C5 = np.array([0, 5])                  # X5
        self.C9 = np.array([0, 2, 4, 7, 10])        # X9
        self.Cm9 = np.array([0, 2, 3, 7, 10])       # Xm9
        self.Cmaj9 = np.array([0, 2, 4, 7, 11])     # Xmaj9
        self.C11 = np.array([0, 2, 4, 5, 7, 10])    # X11
        self.Cm11 = np.array([0, 2, 3, 5, 7, 10])   # Xm11

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


        # Make list of chords containing midi notes
        # Each element of the list contains all the possible notes linked to a chord
        # Will have to be bounded when used with the different makers
        for i, j in zip(chords, roots):

            # For each chord and root this simply makes a vector with all the possible notes
            self.chords.append(np.unique(np.ndarray.flatten(
                np.outer(
                    np.mod(self.chord_list[i]+j, 12), np.ones(10)
                ) + np.outer(np.ones(3), np.arange(10))*12
            )))

    def transpose(self, shift):
        "Transpose chord pattern by amount in semi-tones."
        self.roots = np.mod(self.roots+shift, 12)
        

class Multitrack:
    '''Class to make many tracks/sequences.'''
    def __init__(self, bpm, instruments, chord_pattern, sample_rate):
        self.instruments = instruments      # List of classes
        self.bpm = bpm
        self.chord_pattern = chord_pattern

        self.sequences = []

        # Instantiating instruments
        for instrument in instruments:
            self.sequences.append(
                instrument(
                    bpm,
                    chord_pattern,
                    sample_rate
                )
            )
        
        # Appending names of sequences to variable
        self.names = [seq.name for seq in self.sequences]

    def make_seqs(self):
        '''Method to create sequence for all sequences in the multitrack.'''
        for seq in self.sequences:
            seq.make_seq()

    def loop_multitrack(self, n, start_time, end_time):
        '''Method to loop a section n times after it has occured.
        This will overwrite whatever occurs in the looping time region.'''

        for seq in self.sequences:
            seq.loop_sequence(n, start_time, end_time)





if __name__=="__main__":

    mychords = ChordPattern(
        [0, 1, 2, 3], 
        [0, 1, 0, 1],
        [1, 1, 1, 1]
    ) 

    print(mychords.chords)
