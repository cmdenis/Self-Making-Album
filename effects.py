import numpy as np
from scipy.io.wavfile import write
from scipy.io import wavfile
from scipy.signal import fftconvolve
import matplotlib.pyplot as plt
from notes import *



def reverb(signal, length, dry_wet = 0.5, new_ir = False):
    '''
    Function to add reverb to signals.

    length: length of reverb's decay (in seconds)
    dry_wet: proportion of signal being wet and dry (1 -> wet, 0 -> dry)
    new_ir: generate a new random impulse response
    '''
    print("Adding some reverb...")
    x = np.arange(signal.length)

    if new_ir == True:
        kernel = np.exp(-x/(length*signal.samplerate))*np.random.randn(signal.length)
        
        kernel = fftconvolve(kernel, np.exp(-x/20000))  # Add a gaussian low pass to kernel
        np.savetxt("impulse_responses/test_ir.txt", kernel)
    else:
        kernel = np.loadtxt("impulse_responses/test_ir.txt")

    signal.signal = fftconvolve(kernel, signal.signal)[0:signal.length]

    return signal