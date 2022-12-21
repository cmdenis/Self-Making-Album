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

# Instantiate signal
signal = Signal(
    44100,              # Sampling rate
    4,                  # Duration (Seconds)
    "white_noise_test.wav"   # file Name
)

# Add white noise
white_noise(signal)


# Look at spectrum
spectrum(signal)

# Save file
signal.save_sound()
