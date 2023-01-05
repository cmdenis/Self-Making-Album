from scipy.io.wavfile import write
import scipy as sci
import matplotlib.pyplot as plt
from effects import *   # Important for distribution stuff
from notes import *




class DrumSequence(Sequence):

    def __init__(self, bpm, chord_pattern):
        super().__init__(bpm, chord_pattern)
        self.name = "drum"
        self.tracks = ["bass_drum", "snare_drum", "hi_hat"] # Can be randomized here in the future
    

    def play_metronome(self, start_time, end_time, note_length, midi_note = 0, message = None):
        '''Plays a single note repeatedly with interval corresponding to note_length. Starts sequence at 'start_time' and ends at 'end_time'.'''

        for shot in np.arange(start_time, end_time, note_length)*self.beat_time:
            self.events.append(
                Event(
                    midi_note,
                    shot,
                    shot+0.01,
                    2,
                    message=message
                )
            )

    def make_hihat(self, start_time, end_time, extra_note_scaling = 0.25, midi_note = 0):
            '''Method to make hi-hat sequence'''
            print("╠ Making Hi-Hat Sequence...")
            note_length = np.random.choice(
                [1, 0.5, 0.25],         # Decide for note lengths of hi-hat
                p = [0.25, 0.5, 0.25]   # more likely to use 8th notes
            ) 

            # Make usual pattern (with note on each time)
            self.play_metronome(
                start_time, # Note start
                end_time,   # Note end
                note_length,# Note length
                midi_note=midi_note,
                message= "hi_hat"
            )

            # Create a weight that depends on the length of the notes
            weight = (-4*(note_length - 0.7)**2 + 1.15)*extra_note_scaling

            # Add extra random notes in between main notes
            for shot in np.arange(start_time + note_length/2, end_time, note_length)*self.beat_time:
                if np.random.rand() < 0.2*weight and (0<= np.mod(shot, 2) < 1):
                    self.events.append(
                        Event(
                            midi_note,          # Note used
                            shot,               # Start of note
                            shot+0.01,          # End of note
                            2,                  # Channel
                            message = "hi_hat"  # Message
                        )
                    )

                elif np.random.rand() < 0.3*weight and (1 <= np.mod(shot, 2) < 1.5):
                    self.events.append(
                        Event(
                            midi_note,
                            shot,
                            shot+0.01,
                            2,                  # Channel
                            message = "hi_hat"  # Message
                        )
                    )

                elif np.random.rand() < 0.4*weight and (1.5 <= np.mod(shot, 2) < 2):
                    self.events.append(
                        Event(
                            midi_note,
                            shot,
                            shot+0.01,
                            2,                  # Channel
                            message = "hi_hat"  # Message
                        )
                    )

    def make_sd(self, start_time, end_time, midi_note = 0):
        '''Making Snare Drum sequence'''
        print("╠ Making Snare Drum Sequence...")

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
        
        # Cut down the beat to proper length
        beats = beats[0:duration]

        events = []
        # Loop over notes
        for i in np.arange(start_time, end_time, 0.5):
            events.append(
                Event(
                    midi_note,                          # Midi note
                    (start_time + i)*self.beat_time,    # Start time
                    (end_time + i)*self.beat_time,      # End time
                    1,                                  # Channel
                    message = "snare"                   # Message
                )
            )
        
        self.events = self.events + list(np.array(events)[beats])

    def make_bd(self, start_time, end_time, midi_note = 0):
            '''Making Bass Drum sequence'''
            print("╠ Making Bass Drum Sequence...")

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
                    Event(
                        midi_note,                          # Midi note
                        (start_time + i)*self.beat_time,    # Start time 
                        (end_time + i)*self.beat_time,      # End time
                        0,                                  # Channel
                        message="bass_drum"                 # Message
                    )
                )
            
            self.events = list(np.array(self.events)[beats])

    def make_seq(self):
        '''Function to make 4/4 drum tracks.'''
        print("╔══════════════╗")
        print("║ Making drums ║")
        print("╠══════════════╝")
        print("║")

        nb_bars = 4 # np.random.choice([1, 2, 3, 4], p = [0.15, 0.4, 0.20, 0.25]) # Number of bars to loop
        self.nb_bars = nb_bars

        chokes = np.ones(len(self.tracks))   # Make all tracks choked

        for track, choke in zip(self.tracks, chokes):    # Iterating over the different inputted functions for the tracks
            
            # Make appropriate sequence
            if track == "bass_drum":
                self.make_bd(0, 4*nb_bars)
            elif track == "snare_drum":
                self.make_sd(0, 4*nb_bars)
            elif track == "hi_hat":
                self.make_hihat(0, 4*nb_bars)
            else:
                print("░ Can't recognize drum sound! ░")
        print("║")

        self.print_beat()
       
                    
    def print_beat(self):   
        '''Function to print out a grid presenting the sequence of notes that were played.'''

        # Max beat
        starts = [ev.start for ev in self.events]
        m = int((np.max(starts))/self.beat_time*4+1)


        beats = np.zeros((len(self.tracks), self.nb_bars*16))
        to_print =  "╠══════════╗\n"
        to_print += "║  Tracks  ║ " + "  " + ("1---2---3---4---"*(int(m/16))) + "\n"
        to_print += "╠══════════╩═══" + 16*(int(m/16))*"═" + "╗\n"

        # Times of each 16th notes in sequence
        times = np.arange(0, self.nb_bars*4, 0.25)
      
        for ev in self.events:
            beats[ev.channel, (np.abs(times - ev.start/self.beat_time)).argmin()] = 1

        for idx, track in enumerate(self.tracks):
  
            name_cut = 12 
            heading = track
            heading = heading.ljust(name_cut)
            heading = heading[0:name_cut]
            to_print += ("║" + heading + ": ")

            for strike in beats[idx]:
                if strike == 1:
                    to_print += "█"
                else:
                    to_print += " "
            to_print += "║\n"

        to_print += "╚"+(name_cut+2+16*(int(m/16)))*"═" + "╝"

        print(to_print)



            
          


