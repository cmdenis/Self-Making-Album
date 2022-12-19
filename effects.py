import numpy as np
from scipy.io.wavfile import write
from scipy.io import wavfile
from scipy.signal import fftconvolve
import matplotlib.pyplot as plt
from notes import *



def reverb(signal, length, new_ir = False):
    print("Adding some reverb...")
    x = np.arange(len(signal))

    l = len(signal)

    
    if new_ir == True:
        kernel = np.exp(-x/length)*np.random.randn(l)
        # Add a low pass to kernel
        kernel = fftconvolve(kernel, np.exp(-x/20000))
        np.savetxt("impulse_responses/test_ir.txt", kernel)
    else:
        kernel = np.loadtxt("impulse_responses/test_ir.txt")

    processed = fftconvolve(kernel, signal)

    return processed