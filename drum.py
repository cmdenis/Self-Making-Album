# This file contains the sample function class that allows to create samples to be used by the
# drum/sample sound generator

import numpy as np
from scipy.io.wavfile import write
import scipy as sci
import matplotlib.pyplot as plt
from effects import *   # Important for distribution stuff


class DrumSound:
    def __init__(self, length, sample_rate, chord_pattern, func = None):
        '''Initializes instrument. Instruments such as bass drum or snare inherit attributes from this class.'''
        
        self.length = length            # Length of sample (in seconds)
        self.sr = sample_rate  # Sample rate
        self.func = func        # Function for the sample, first argument is time and the second is parameters


class SnareDrumSound(DrumSound):
    def __init__(self, length, sample_rate, chord_pattern, func=None):
        super().__init__(length, sample_rate, chord_pattern, func)

        self.param = [
            custom_norm(100, 800, 200, 25),     # p[0]: Pitch (Hz)
            custom_norm(0.99, 5, 1, 0.1),       # p[1]: Pitch mod
            custom_norm(0, 5, 0.1, 2),          # p[2]: Pitch decay (s)
            custom_norm(0.01, 3, 0.1, 0.1),     # p[3]: Amp decay (s)
            custom_norm(0.01, 3, 0.07, 0.1),    # p[4]: noise decay
            custom_norm(0, 1, 0.5, 0.5)         # p[5]: noise/tone ratio
        ]

    def make_sample(self, x, p):
        '''To make snare drum sound'''
        sound = np.sin(2*np.pi*((1-p[1])*p[2]*np.exp(-x/p[2]) - (1-p[1])*p[2] +x)*p[0])*np.exp(-x/p[3])*(1-p[5]) + np.random.uniform(-1, 1, len(x))*np.exp(-x/p[4])*p[5]
        filt = sci.signal.butter(3, 200, btype="highpass", fs = self.sr, output="sos")
        return sci.signal.sosfilt(filt, sound)

class BassDrumSound(DrumSound):
    def __init__(self, length, sample_rate, chord_pattern, func=None):
        super().__init__(length, sample_rate, chord_pattern, func)

        # Create drum parameters
        self.param = [
            custom_norm(20, 20000, 40, 20),         # p[0]: Pitch (Hz)
            custom_norm(0.9, 15, 4, 2),             # p[1]: Pitch mod
            custom_norm(0.005, 1, 0.03, 0.03),      # p[2]: Pitch decay (s)
            custom_norm(0.002, 3, 0.2, 0.8),        # p[3]: Amp decay (s)
        ]
    
    def make_sample(self, x, p):
        '''To make bass drum sound'''
        return np.sin(2*np.pi*((1-p[1])*p[2]*np.exp(-x/p[2]) - (1-p[1])*p[2] +x)*p[0])*np.exp(-x/p[3])

class HihatSound(DrumSound):
    def __init__(self, length, sample_rate, chord_pattern, func=None):
        super().__init__(length, sample_rate, chord_pattern, func)

        self.param = [
                custom_norm(0.001, 0.01, 0.005, 0.005),     # p[0]: Noise decay
                custom_norm(0, 10, 5, 4),                   # p[1]: AM mod
                custom_norm(200, 4000, 1000, 1000)          # p[2]: AM frequency
            ]

    def make_sample(self, x, p):
        sound = np.random.uniform(-1, 1, len(x))*np.exp(-x/p[0])*(1 - p[1]*np.sin(2*np.pi*p[2]*x)**2) + np.sin(2*np.pi*x*2000)*(1 - p[1]*np.sin(2*np.pi*p[2]*x)**2)*np.exp(-x/0.01)*0.2
        filt = sci.signal.butter(3, 500, btype="highpass", fs = self.sr, output="sos")
        return sci.signal.sosfilt(filt, sound)
    
class ClickSound(DrumSound):
    def __init__(self, length, sample_rate, chord_pattern, func=None):
        super().__init__(length, sample_rate, chord_pattern, func)

        self.param = [
            custom_norm(100, 1000, 550, 50),     # p[0]: Pitch (Hz)
            custom_norm(0.99, 5, 1, 0.05),       # p[1]: Pitch mod
            custom_norm(0, 5, 0.1, 2),          # p[2]: Pitch decay (s)
            custom_norm(0.01, 3, 0.1, 0.1),     # p[3]: Amp decay (s)
        ]


    def make_sample(self, x, p):
        '''To make snare drum sound'''
        return np.sin(2*np.pi*((1-p[1])*p[2]*np.exp(-x/p[2]) - (1-p[1])*p[2] +x)*p[0])*np.exp(-x/p[3])
