import numpy as np
from scipy.io.wavfile import write
from scipy.io import wavfile
from scipy.signal import fftconvolve
import scipy as sci
import matplotlib.pyplot as plt
from notes import *


def spectrum(signal, window_func = np.cos):
    '''Function that looks at the frequency spectrum of a signal.'''
    x = np.linspace(0, np.pi, signal.length)

    window = window_func(x)
    #sig_spec = np.abs(np.fft.fft(signal.signal*window))**2
    spec_y = np.abs(sci.fft.rfft(signal.signal*window))
    spec_x = sci.fft.rfftfreq(signal.length, 1/signal.samplerate)

    #spec_y = spec_y[spec_x>=0]
    #spec_x = spec_x[spec_x>=0]

    plt.plot(spec_x, spec_y, label = "Spectrum")
    #plt.xscale("log")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Amplitude")
    plt.legend()
    plt.show()



def lowpass(signal, dry_wet = 1, filter_type = "gaussian"):
    '''
    Function that adds a low-pass filter to a signal.
    '''

    print("Adding a "+ filter_type + " LP filter...")

    x = np.arange(signal.length)

    if filter_type == "gaussian":
        cutoff = 1000
        sigma = signal.length/(cutoff*2*np.pi)
        kernel = np.exp(-x**2/(2*sigma**2))
        kernel = kernel/np.sum(kernel)
    else:
        print("Warning: filter_type missing!")

    signal.signal = fftconvolve(kernel, signal.signal)[0:signal.length]*dry_wet + signal.signal*(1-dry_wet)

    return signal





def reverb(signal, length, dry_wet, new_ir = False):
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
        kernel = kernel/np.sum(kernel)
         
        np.savetxt("impulse_responses/test_ir.txt", kernel)
    else:
        kernel = np.loadtxt("impulse_responses/test_ir.txt")

    #plt.plot(kernel, label = "Kernel")
    #plt.plot(signal.signal, label = "Original Signal")


    signal.signal = fftconvolve(kernel, signal.signal)[0:signal.length]*dry_wet + signal.signal*(1-dry_wet)
    #plt.plot(signal.signal, label = "Convolve Signal")
    #plt.legend()
    #plt.show()
    return signal