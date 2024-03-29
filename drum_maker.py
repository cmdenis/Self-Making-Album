from scipy.io.wavfile import write
import scipy as sci
import matplotlib.pyplot as plt
from effects import *   # Important for distribution stuff
from notes import Sequence, Event
from drum import *
from signals import Signal



class PercussionInstrumentSequence(Sequence):
    
    def __init__(self, bpm, chord_pattern, sr, channel, drum_index, midi_note = 0):
        super().__init__(bpm, chord_pattern, sr)
        self.channel = channel
        self.midi_note = midi_note
        self.name = None
        self.drum_index = drum_index

    
    def play_metronome(self, start_time, end_time, note_length, midi_note = 0):
        '''Plays a single note repeatedly with interval corresponding to note_length. Starts sequence at 'start_time' and ends at 'end_time'.'''

        for shot in np.arange(start_time, end_time, note_length)*self.beat_time:
            self.events.append(
                Event(
                    self.midi_note,
                    shot,
                    shot+self.beat_time,
                    self.channel,
                    message = self.name
                )
            )

    def play_sound(self, sig):
        print("Synthesizing a '" + self.name + "' sound...")

        # Making the samples
        x = np.arange(int(self.sample.length*sig.sr+1))/sig.sr
        if self.choke == True:
            self.sort_sequence()

        # Loop over events in sequence
        for ev in self.events:

            # Creating a sine wave
            #print("Starting sample at:", ev.start)
            t0 = np.zeros(int(ev.start*sig.sr))                       # Zeroes before start of sound
            t1 = self.sample.make_sample(x, self.sample.param)                    # Sound
            t2 = np.zeros(int((sig.duration - (ev.start+self.sample.length))*sig.sr))              # Zeroes at the end of sound
    
            buffer = np.zeros(10)   # Buffer to make all arrays of equal length

            # If choke is true then remove other sounds when new sound starts playing.
            if self.choke==True:
                sig.signal[int(ev.start*sig.sr):int(((ev.start+self.sample.length))*sig.sr)] = 0

            # Add sound to signal
            #print(len(np.concatenate((t0, t1, t2, buffer))[:sig.sr*sig.duration]))
            sig.signal += np.concatenate((t0, t1, t2, buffer))[:sig.sr*sig.duration]

class BassDrumSequence(PercussionInstrumentSequence):
    def __init__(self, bpm, chord_pattern, sr, channel, drum_index, midi_note=0):
        super().__init__(bpm, chord_pattern, sr, channel, drum_index, midi_note)

        self.name = "bass_drum"

        self.choke = False
        
        # Instantiates bass drum sample
        self.sample = BassDrumSound(2, self.sr, chord_pattern)


    def make_seq(self, start_time, end_time, midi_note = 0):
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
                    self.midi_note,                          # Midi note
                    (start_time + i)*self.beat_time,    # Start time 
                    (start_time + 1 + i)*self.beat_time,      # End time
                    self.channel,                                  # Channel
                    message="bass_drum"                 # Message
                )
            )
        
        self.events = list(np.array(self.events)[beats])

class SnareDrumSequence(PercussionInstrumentSequence):
    def __init__(self, bpm, chord_pattern, sr, channel, drum_index, midi_note=0):
        super().__init__(bpm, chord_pattern, sr, channel, drum_index, midi_note)

        self.name = "snare_drum"

        self.choke = False

        # Instantiates bass drum sample
        self.sample = SnareDrumSound(2, self.sr, chord_pattern)

    def make_seq(self, start_time, end_time, midi_note = 0):
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
                    self.midi_note,                          # Midi note
                    (start_time + i)*self.beat_time,    # Start time
                    (start_time + 1 + i)*self.beat_time,      # End time
                    self.channel,                                  # Channel
                    message = "snare"                   # Message
                )
            )
        
        self.events = self.events + list(np.array(events)[beats])

class HihatSequence(PercussionInstrumentSequence):
    def __init__(self, bpm, chord_pattern, sr, channel, drum_index, midi_note=0):
        super().__init__(bpm, chord_pattern, sr, channel, drum_index, midi_note)

        self.name = "hi_hat"

        self.choke = False

        # Instantiates bass drum sample
        self.sample = HihatSound(0.1, self.sr, chord_pattern)    

    def make_seq(self, start_time, end_time, extra_note_scaling = 0.25, midi_note = 0):
        '''Method to make hi-hat sequence'''
        print("╠ Making Hi-Hat Sequence...")
        note_length = np.random.choice(
            [1, 0.5, 0.25],         # Decide for note lengths of hi-hat
            p = [0.25, 0.5, 0.25]   # more likely to use 8th notes
        ) 

        # Make usual pattern (with note on each time)
        self.play_metronome(
            start_time, # Note start
            start_time + self.beat_time,   # Note end
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
                        self.midi_note,          # Note used
                        shot,               # Start of note
                        shot+self.beat_time,          # End of note
                        self.channel,                  # Channel
                        message = "hi_hat"  # Message
                    )
                )

            elif np.random.rand() < 0.3*weight and (1 <= np.mod(shot, 2) < 1.5):
                self.events.append(
                    Event(
                        self.midi_note,
                        shot,
                        shot+self.beat_time,
                        self.channel,                  # Channel
                        message = "hi_hat"  # Message
                    )
                )

            elif np.random.rand() < 0.4*weight and (1.5 <= np.mod(shot, 2) < 2):
                self.events.append(
                    Event(
                        self.midi_note,
                        shot,
                        shot+self.beat_time,
                        self.channel,                  # Channel
                        message = "hi_hat"  # Message
                    )
                )

class ClickSequence(PercussionInstrumentSequence):
    def __init__(self, bpm, chord_pattern, sr, channel, drum_index, midi_note=0):
        super().__init__(bpm, chord_pattern, sr, channel, drum_index, midi_note)

        self.name = "click_sound"

        self.choke = False

        # Instantiates sample
        self.sample = ClickSound(1, self.sr, chord_pattern)

    def make_seq(self, start_time, end_time, midi_note = 0):
        '''Making click sounf sequence'''
        print("╠ Making Click Sound Sequence...")

        # Duration of sequence in 8th notes
        duration = int(2*(end_time - start_time))

        # Boolean array to determine if beats are being selected
        probs = np.array([
            0.05,   # 1
            0.05,
            0.10,   # 1+
            0.05,
            0.05,   # 2
            0.05,
            0.5,    # 2+
            0.05,
            0.98,   # 3
            0.05,
            0.05,   # 3+
            0.05,
            0.2,    # 4
            0.05,
            0.4,    # 4+
            0.05
        ])

        # Select how many strike per bar:
        pp = np.array([1, 5, 8, 15, 15, 10, 4, 2, 1])   # Probs for nb of strikes
        nb = np.random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8], p = pp/np.sum(pp))

        beats = np.full(16, False)   # Initialize array full of false
        beats[np.random.choice(np.arange(16), nb, replace = False, p=probs/np.sum(probs))] = True

        beats = np.tile(beats, int(np.ceil(duration/16)))

        #beats = np.tile(probs, int(np.ceil(duration/16))) > np.random.rand(int(np.ceil(duration/8)*8))
        
        # Cut down the beat to proper length
        beats = beats[0:duration]

        events = []
        # Loop over notes
        for i in np.arange(start_time, end_time, 0.5):
            events.append(
                Event(
                    self.midi_note,                          # Midi note
                    (start_time + i)*self.beat_time,    # Start time
                    (start_time + i+1)*self.beat_time,      # End time
                    self.channel,                                  # Channel
                    message = "snare"                   # Message
                )
            )
        
        self.events = self.events + list(np.array(events)[beats])


class DrumSequence(Sequence):

    def __init__(self, bpm, chord_pattern, sr):
        super().__init__(bpm, chord_pattern, sr)
        self.name = "drum"

        self.tracks = []

        channel = 0
        midi_note = 0
        idx = 0
        # Appending bass drum(s) to track
        for i in range(np.random.choice([0, 1, 2, 3], p = [0.07, 0.8, 0.1, 0.03])):
            self.tracks.append(BassDrumSequence(self.bpm, self.chord_pattern, self.sr, 0, idx, midi_note=midi_note))
            #channel += 1
            midi_note += 1
            idx += 1

        # Appending snare drum(s) to track
        midi_note = 10
        for i in range(np.random.choice([0, 1, 2, 3], p = [0.07, 0.8, 0.1, 0.03])):
            self.tracks.append(SnareDrumSequence(self.bpm, self.chord_pattern, self.sr, 1, idx, midi_note=midi_note))
            #channel += 1
            midi_note += 1
            idx += 1

        # Appending hh drum(s) to track
        midi_note = 20
        for i in range(np.random.choice([0, 1, 2, 3], p = [0.15, 0.75, 0.08, 0.02])):
            self.tracks.append(HihatSequence(self.bpm, self.chord_pattern, self.sr, 2, idx, midi_note=midi_note))
            #channel += 1
            midi_note += 1
            idx += 1


        # Appending some click sounds to track
        midi_note = 30
        for i in range(np.random.choice([0, 1, 2, 3], p = [0.15, 0.75, 0.08, 0.02])):
            self.tracks.append(ClickSequence(self.bpm, self.chord_pattern, self.sr, 3, idx, midi_note=midi_note))
            #channel += 1
            midi_note += 1
        

        '''self.tracks = list([
            np.random.choice(
                [
                    BassDrumSequence(self.bpm, self.chord_pattern, self.sr), 
                    SnareDrumSequence(self.bpm, self.chord_pattern, self.sr), 
                    HihatSequence(self.bpm, self.chord_pattern, self.sr)
                ],
                size = 3,
                p = [0.4, 0.3, 0.3]
            )
        ])'''


        
        # Can be randomized here in the future
    
    def make_seq(self):
        '''Function to make 4/4 drum tracks.'''
        print("╔══════════════╗")
        print("║ Making drums ║")
        print("╠══════════════╝")
        print("║")

        nb_bars = 4 # np.random.choice([1, 2, 3, 4], p = [0.15, 0.4, 0.20, 0.25]) # Number of bars to loop
        self.nb_bars = nb_bars


        for track in self.tracks:    # Iterating over the different drum sounds
            # Make sequence
            track.make_seq(0, 4*nb_bars)
            track.loop_sequence((self.chord_pattern.pat_length)/(4*nb_bars), 0, 4*nb_bars)

            
        print("║")

        # Add events to overall drum sequence
        #self.make_bus_events()
        #self.print_beat()
        self.make_bus_events()

    def loop_sequence(self, n, start_time, end_time):
        '''Overriding loop_sequence for DrumSequence because need to loop individual sub-sequences'''
        for track in self.tracks:
            track.loop_sequence(n, start_time, end_time)
        self.make_bus_events()

    def make_bus_events(self):
        '''Add all events from individual tracks to overall drum events'''
        self.events = []
        # Circulate through different drums sounds/tracks
        for track in self.tracks:
            self.events += track.events

        self.sort_sequence()
              
    def print_beat(self):   
        '''Function to print out a grid presenting the sequence of notes that were played.'''
        # Max beat
        starts = [ev.start for ev in self.events]
        m = int((np.max(starts))/self.beat_time*4)


        beats = np.zeros((len(self.tracks), 16*(int(m/16)+1)))
        to_print =  "╠══════════╗\n"
        to_print += "║  Tracks  ║ " + "  " + ("1---2---3---4---"*(int(m/16)+1)) + "\n"
        to_print += "╠══════════╩═══" + 16*(int(m/16)+1)*"═" + "╗\n"

        # Times of each 16th notes in sequence
        times = np.arange(0, 16*(int(m/16)+1), 0.25)
    
        for ev in self.events:
            beats[ev.idx, (np.abs(times - ev.start/self.beat_time)).argmin()] = 1

        for idx, track in enumerate(self.tracks):

            name_cut = 12 
            heading = track.name
            heading = heading.ljust(name_cut)
            heading = heading[0:name_cut]
            to_print += ("║" + heading + ": ")

            for strike in beats[idx]:
                if strike == 1:
                    to_print += "█"
                else:
                    to_print += " "
            to_print += "║\n"

        to_print += "╚"+(name_cut+2+16*(int(m/16)+1))*"═" + "╝"

        print(to_print)
       


    def play_sound(self, sig):
        print("\n==== 🥁 Synthesizing drum sound... ====")

        for track in self.tracks:
            # Making drum signal
            temp_sig = Signal(sig.sr, sig.duration, None)
            track.play_sound(temp_sig)

            # Adding reverb
            if 0.4 > np.random.rand():
                reverb(
                    temp_sig,                            # Signal
                    custom_norm(0.01, 4, 0.5, 0.5), # Length of reverb
                    custom_norm(0, 1, 0, 0.2)     # Dry/Wet Mix
                )

            # Adding waveshaper
            waveshaper(temp_sig, intensity=custom_norm(3, 8, 4, 1))

            sig.signal += temp_sig.signal / temp_sig.LUFS()


        
            



                
            


