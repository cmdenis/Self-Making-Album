import numpy as np
from scipy.io.wavfile import write
from scipy.io import wavfile
import scipy.signal as sig
import matplotlib.pyplot as plt
from notes import *
from effects import *
from sound_generator import *
from math_samples import *



def make_4_4_drum(signal, bpm, start_beat, length, tracks, master_only = True, chokes  = None):
    '''Function to make drum tracks'''

    # List where the signals for each drum track will be stored
    sound_tracks = []
    midi_tracks = []

    # Select the number of bars to loop
    nb_bars = np.random.choice([1, 2, 3, 4], p = [0.15, 0.4, 0.20, 0.25])
    nb_bars = 3

    # No choke parameters, make all tracks chocked
    if chokes == None:
        chokes = np.ones(len(tracks))

    for track, choke in zip(tracks, chokes):    # Iterating over the different inputted functions for the tracks
        
        # First initialize sound and midi tracks
        sig = Signal(signal.samplerate, signal.duration, signal.filename)
        seq = Sequence(bpm, signal.samplerate)

        # Choose sample
        sound = SampleFunction(track, 2, signal.samplerate)

        # Make appropriate sequence
        if track == "bass_drum":
            seq.make_bd(0, 4*nb_bars)
        elif track == "snare_drum":
            seq.make_sd(0, 4*nb_bars)
        elif track == "hi_hat":
            seq.make_hihat(0, 4*nb_bars)
        
        '''# Pick notes that will go after the looping
        extra_beats = np.mod(length, nb_bars*4)
        to_add = []
        seq.sort_sequence()
        for i in seq.events:
            if i.start < extra_beats*seq.beat_time:
                ev = i.copy()
                ev.start += (nb_bars*4)*seq.beat_time
                ev.end += (nb_bars*4)*seq.beat_time
                to_add.append(ev)
            else:
                break

        # Loop sequence 
        seq.loop_sequence(int(np.floor(length/nb_bars/4)), 0, 4*nb_bars*seq.beat_time)

        # Add notes to complete sequence
        for ev in to_add:
            seq.events.append(ev)'''

        play_function(sig, seq, sound, sound.param, choke = choke)

        sound_tracks.append(sig)
        midi_tracks.append(seq)
    
    # Add all tracks to master signal
    for track in sound_tracks:
        signal.signal += track.signal



if __name__=='__main__':

    sig = Signal(44100, 11, "audio_tests/drum_maker44.wav")

    make_4_4_drum(sig, 120, 0, 16, ["bass_drum", "snare_drum", "hi_hat"])

    sig.save_sound()



