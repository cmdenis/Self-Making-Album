# This file contains the sample function class that allows to create samples to be used by the
# drum/sample sound generator

import numpy as np
from scipy.io.wavfile import write
import scipy as sci
import matplotlib.pyplot as plt
from effects import *

class Sample_function:
    def __init__(self, func_name, length, func = None):
        '''Initializes object. If func is left blank, then it will be replaced by the preset samples from 'make_sample'.'''

        self.name = _func_name      # Name of instrument
        self.length = length        # Length of sample (in seconds)

        if self.func == None:
            self.make_sample()
        else:
            self.func = func        # Function for the sample, first argument is time and the second is parameters

    def make_sample(self):
        '''Method to create sample based on 'func_name'.'''

        if func_name == "bass_drum":
            self.func = lambda x, p: np.sin(2*np.pi*((1-p[1])*p[2]*np.exp(-x/p[2]) - (1-p[1])*p[2] +x)*p[0])*np.exp(-x/p[3]),
            self.length = 2
        
        elif func_name == "snare_drum":
            self.func = 0
            self.length = 1
    






'''
# Bass drum 
bass_drum = Sample_function(
    lambda x, p: np.sin(2*np.pi*((1-p[1])*p[2]*np.exp(-x/p[2]) - (1-p[1])*p[2] +x)*p[0])*np.exp(-x/p[3]), 
    2,   # Duration in seconds
    "Bass Drum"
)
# Parameters for bass_drum
# p[0]: Pitch (Hz)
# p[1]: Pitch mod
# p[2]: Pitch decay (s)
# p[3]: Amp decay (s)
'''