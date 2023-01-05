# This file contains the sample function class that allows to create samples to be used by the
# drum/sample sound generator

import numpy as np
from scipy.io.wavfile import write
import scipy as sci
import matplotlib.pyplot as plt
from effects import *   # Important for distribution stuff
from notes import Event

def play_metronome(self, start_time, end_time, note_length, midi_note = 0):
    '''Plays a single note repeatedly with interval corresponding to note_length. Starts sequence at 'start_time' and ends at 'end_time'.'''

    for shot in np.arange(start_time, end_time, note_length)*self.beat_time:
        self.events.append(
            Event(
                midi_note,
                shot,
                shot+0.01,
                2
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
        play_metronome(
            self,
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
                        shot+0.01,
                        2
                    )
                )

            elif np.random.rand() < 0.3*weight and (1 <= np.mod(shot, 2) < 1.5):
                self.events.append(
                    Event(
                        midi_note,
                        shot,
                        shot+0.01,
                        2
                    )
                )

            elif np.random.rand() < 0.4*weight and (1.5 <= np.mod(shot, 2) < 2):
                self.events.append(
                    Event(
                        midi_note,
                        shot,
                        shot+0.01,
                        2
                    )
                )

def make_sd(seq, start_time, end_time, midi_note = 0):
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
                midi_note, 
                (start_time + i)*seq.beat_time, 
                (end_time + i)*seq.beat_time,
                1
            )
        )
    
    seq.events = seq.events + list(np.array(events)[beats])

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
                Event(midi_note, (start_time + i)*self.beat_time, (end_time + i)*self.beat_time, 0)
            )
        
        self.events = list(np.array(self.events)[beats])

def make_drum(seq, tracks):
    '''Function to make 4/4 drum tracks.'''
    print("Making drums")
    print("║")

    nb_bars = 4 # np.random.choice([1, 2, 3, 4], p = [0.15, 0.4, 0.20, 0.25]) # Number of bars to loop

    chokes = np.ones(len(tracks))   # Make all tracks choked

    for track, choke in zip(tracks, chokes):    # Iterating over the different inputted functions for the tracks
        
        # Make appropriate sequence
        if track == "bass_drum":
            make_bd(seq, 0, 4*nb_bars)
        elif track == "snare_drum":
            make_sd(seq, 0, 4*nb_bars)
        elif track == "hi_hat":
            make_hihat(seq, 0, 4*nb_bars)
        else:
            print("░ Can't recognize drum sound! ░")
    print("║")
    print("╚ Done making drums\n")
                
            
            
          




if __name__=='__main__':
    bpm = custom_norm(70, 200, 120, 40)
    length = 24

    time = length*60/bpm + 4

    sig = Signal(44100, time, "audio_tests/drum_maker44.wav")
    
    make_4_4_drum(sig, bpm, 0, length, ["bass_drum", "snare_drum", "hi_hat"])

    sig.save_sound()



