import numpy as np
from scipy.io.wavfile import write
from scipy.io import wavfile
import scipy.signal as sig
import matplotlib.pyplot as plt
from notes import *
from effects import *
from sound_generator import *
from math_samples import *

def bass_drum_parameters():
    

def make_4_4_drum(signal, length, track_list, master_only = True):
    '''Function to make drum tracks'''

    # List where the signals for each drum track will be stored
    tracks = []

    for track in track_list:    # Iterating over the different inputted functions for the tracks



