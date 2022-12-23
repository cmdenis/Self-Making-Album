import numpy as np
from scipy.io.wavfile import write
from scipy.io import wavfile
import scipy.signal as sig
import matplotlib.pyplot as plt
from notes import *
from effects import *
from sound_generator import *

# Script to make a random sequence based on the random note generator


# Global signal
class Signal:
    '''Class that contains a signal'''
    def __init__(self, samplerate, duration, filename, save_samplerate = 44100):
        
        self.filename = filename                # Name of file
        self.samplerate = samplerate            # Sampling rate of array
        self.duration = duration                # (Seconds)
        self.save_samplerate = save_samplerate  # Sample rate of saved file

        self.signal = np.zeros(samplerate*duration) # Signal
        self.length = duration * samplerate

    def save_sound(self):

        if self.save_samplerate == 44100: # If no extra sample rate specified, use the one from the array
            # Normalizing and Making sure signal has correct amplitude
            data = np.iinfo(np.int16).max * self.signal / np.max(self.signal)/10 
            # Write signal to disk
            write(self.filename, self.samplerate, data.astype(np.int16))

        else:
            # Interpolate data to make sampling frequencies match
            og_smp = np.arange(self.duration*self.samplerate)
            new_smp = np.arange(self.duration*self.save_samplerate)
            data = np.interp(new_smp, og_smp, self.signal)
            # Normalizing and Making sure signal has correct amplitude
            data = np.iinfo(np.int16).max * data / np.max(data) / 10 

            # Write signal to disk
            write(self.filename, self.save_samplerate, data.astype(np.int16))

        
        
 




signal = Signal(
    44100,              # Sampling rate
    5,                  # Duration (Seconds)
    "test_chord.wav"   # file Name
)


# Make major scale
major = Scale(np.array([0, 2, 4, 5, 7, 9, 11]), 0)

# Obtain sequence of notes
sequence = Sequence(120, 44100)
sequence.play_chord(major, 0, [60, 77], 0, 8)

# Create sine sequence  
sine_synth(sequence.events, signal)

# Add some reverb
#signal = reverb(signal, 1, 0.5, new_ir = True)

# Add a LP Filter
#signal = lowpass(signal, filter_type="gaussian")


# Save signal
signal.save_sound()
