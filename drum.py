# This file contains the sample function class that allows to create samples to be used by the
# drum/sample sound generator

import numpy as np
from scipy.io.wavfile import write
import scipy as sci
import matplotlib.pyplot as plt
from effects import *   # Important for distribution stuff

class SampleFunction:
    def __init__(self, func_name, length, sample_rate, func = None):
        '''Initializes object. If func is left blank, then it will be replaced by the preset samples from 'make_sample'.'''

        self.name = func_name      # Name of instrument
        self.length = length        # Length of sample (in seconds)
        self.sample_rate = sample_rate

        # Checks if user inputted custom function
        if func == None:
            self.make_sample()
        else:
            self.func = func        # Function for the sample, first argument is time and the second is parameters

    def make_sample(self):
        '''Method to create sample based on 'func_name'.'''

        if self.name == "bass_drum":
            self.func = lambda x, p: np.sin(2*np.pi*((1-p[1])*p[2]*np.exp(-x/p[2]) - (1-p[1])*p[2] +x)*p[0])*np.exp(-x/p[3])
            self.length = 2

            # Create drum parameters
            self.param = [
                custom_norm(20, 20000, 40, 20),         # p[0]: Pitch (Hz)
                custom_norm(0.9, 15, 6, 2),             # p[1]: Pitch mod
                custom_norm(0.005, 1, 0.03, 0.03),      # p[2]: Pitch decay (s)
                custom_norm(0.002, 3, 0.2, 1.5),        # p[3]: Amp decay (s)
            ]
            
        elif self.name == "snare_drum":
            def sd(x, p):
                sound = np.sin(2*np.pi*((1-p[1])*p[2]*np.exp(-x/p[2]) - (1-p[1])*p[2] +x)*p[0])*np.exp(-x/p[3])*(1-p[5]) + np.random.uniform(-1, 1, len(x))*np.exp(-x/p[4])*p[5]
                filt = sci.signal.butter(3, 200, btype="highpass", fs = self.sample_rate, output="sos")
                return sci.signal.sosfilt(filt, sound)

            self.func = sd
            self.length = 1
            self.param = [
                custom_norm(100, 800, 200, 25),     # p[0]: Pitch (Hz)
                custom_norm(0.99, 5, 1, 0.1),       # p[1]: Pitch mod
                custom_norm(0, 5, 0.1, 2),          # p[2]: Pitch decay (s)
                custom_norm(0.01, 3, 0.1, 0.1),     # p[3]: Amp decay (s)
                custom_norm(0.01, 3, 0.07, 0.1),    # p[4]: noise decay
                custom_norm(0, 1, 0.5, 0.5)         # p[5]: noise/tone ratio
            ]

        elif self.name == "hi_hat":
            def hh(x, p):
                sound = np.random.uniform(-1, 1, len(x))*np.exp(-x/p[0])*(1 - p[1]*np.sin(2*np.pi*p[2]*x)**2) + np.sin(2*np.pi*x*2000)*(1 - p[1]*np.sin(2*np.pi*p[2]*x)**2)*np.exp(-x/0.01)*0.2
                filt = sci.signal.butter(3, 500, btype="highpass", fs = self.sample_rate, output="sos")
                return sci.signal.sosfilt(filt, sound)
            
            self.func = hh
            self.length = 1

            self.param = [
                custom_norm(0.001, 0.01, 0.005, 0.005),     # p[0]: Noise decay
                custom_norm(0, 10, 5, 4),                   # p[1]: AM mod
                custom_norm(200, 4000, 1000, 1000)          # p[2]: AM frequency
            ]

def play_drum_sound(sig, seq, instrument_func, parameters, choke = False):
    print("Making a '" + instrument_func.name + "'...")

    # Making the sample
    
    x = np.arange(instrument_func.length*sig.samplerate)/sig.samplerate

    if choke == True:
        seq.sort_sequence()

    # Loop over events in sequence
    for ev in seq.events:
        # Creating a sine wave
        #print("Starting sample at:", ev.start)
        t0 = np.zeros(int(ev.start*sig.samplerate))                       # Zeroes before start of sound
        t1 = instrument_func.func(x, parameters) # Sound
        t2 = np.zeros(int((sig.duration - (ev.start+instrument_func.length))*sig.samplerate))              # Zeroes at the end of sound
        buffer = np.zeros(10)   # Buffer to make all arrays of equal length

        # If choke is true then remove other sounds when new sound starts playing.
        if choke==True:
            sig.signal[int(ev.start*sig.samplerate):int(((ev.start+instrument_func.length))*sig.samplerate)] = 0

        # Add sound to signal
        sig.signal += np.concatenate((t0, t1, t2, buffer))[:sig.samplerate*sig.duration]


def play_drum()