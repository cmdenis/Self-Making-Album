import numpy as np
import random as rand


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
    
    def __str__(self) -> str:
        string = "\nEvent:"
        string += "\n\t MIDI Note: " + str(self.midi_note)
        string += "\n\t Pitch: " + str(self.pitch) + " Hz"
        string += "\n\t Start: " + str(self.start)
        string += "\n\t End: " + str(self.end)
        string += "\n\t Length: " + str(self.end - self.start)
        string += "\n\t Channel: " + str(self.channel)
        string += "\n\t Message: " + str(self.message)
        return string


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
                
                for i in range(int(np.ceil(n))):
                    '''print(Event(
                            ev.midi_note,
                            ev.start + i * loop_duration,
                            ev.end + i * loop_duration,
                            ev.channel
                        ))'''
                    # Since looping over ceil of n
                    # Must make sure the event actually happens
                    # within n before appending it
                    if ev.start + i * loop_duration < n*loop_duration:
                        
                        self.events.append(
                            Event(
                                ev.midi_note,
                                ev.start + i * loop_duration,
                                ev.end + i * loop_duration,
                                ev.channel,
                                ev.message
                            )
                        )
                

            # If events are not part of loop, simply append them to event list
            elif start_time + loop_duration * n <= ev.start or ev.start < start_time:
                #print("here")
                #print("note:", ev.midi_note)
                self.events.append(ev)



class ChordPattern:
    '''Class for chord pattern object'''
    def __init__(self, roots, chords, lengths):

        self.roots = roots      # Array with roots of chords used
        #self.chords = chords    # Array with chords used
        self.chords = []    # Will be filled with all the notes for the chords
        self.lengths = lengths  # Array with lengths of chords
        self.nb_chords = len(chords)
        self.pat_length = np.sum(lengths)
        
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
            chord_length = len(self.chord_list[i])
            # For each chord and root this simply makes a vector with all the possible notes
            self.chords.append(np.unique(np.ndarray.flatten(
                np.outer(
                    np.mod(self.chord_list[i]+j, 12), np.ones(10)
                ) + np.outer(np.ones(chord_length), np.arange(10))*12
            )))

    def transpose(self, shift):
        "Transpose chord pattern by amount in semi-tones."
        self.roots = np.mod(self.roots+shift, 12)

    def select_note_scattered(self, note_range, min_notes = 3, max_notes = 5):
        '''Method that selects notes to be played in a chord'''
        to_play = []    # Array containing notes to play
        print("╠ Using 'select_note_scattered'...")
        nb_notes = np.random.randint(low = min_notes, high=max_notes, size = self.nb_chords)
        
        for nb, chord in zip(nb_notes, self.chords):
            to_play.append(
                np.random.choice(chord[np.logical_and(note_range[0] <= chord, chord <= note_range[1])], size = nb, replace=False)
            )
        return to_play

    def select_note_range(self, note_range):
        '''Play all notes in  range'''
        to_play = []    # Array containing notes to play
        print("╠ Using 'select_note_range'...")
        for chord in self.chords:
            to_play.append(
                chord[np.logical_and(note_range[0] <= chord, chord <= note_range[1])]
            )
        return to_play

    def get_chord(self, note_range):
        '''Selects a method for chord generation'''
        method = np.random.choice(
            [
                self.select_note_range,
                self.select_note_scattered
            ],
            #p = [0.75, 0.25]
        )

        return method(note_range)

        

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

    def last_time(self):
        '''Method to get final released note. Is used when trying to figure out how long the audio file should be.'''
        max_time = 0
        for seq in self.sequences:
            for ev in seq.events:
                if max(ev.start, ev.end) > max_time:
                    max_time = max(ev.start, ev.end)
        return max_time


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
