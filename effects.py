import numpy as np
from scipy.io.wavfile import write
from scipy.io import wavfile
from scipy.signal import fftconvolve
import scipy as sci
import matplotlib.pyplot as plt
from notes import *

def custom_norm(a, b, mean, sigma):
    '''Function to create a normal distribution with bounds a to b, std sigma and mean'''
    return sci.stats.truncnorm.rvs((a-mean)/sigma, (b-mean)/sigma)*sigma + mean

def spectrum(signal, window_func = np.cos):
    '''Function that looks at the frequency spectrum of a signal.'''
    # Make cosine windowing
    x = np.linspace(0, np.pi, signal.length)
    window = window_func(x)

    # Take fft and appropriate axis
    spec_y = np.abs(sci.fft.rfft(signal.signal*window))
    spec_x = sci.fft.rfftfreq(signal.length, 1/signal.samplerate)
    
    # Plot result
    plt.plot(spec_x, spec_y, label = "Spectrum")
    plt.xscale("log")
    plt.xlim((20, 20000))   # Audio range 20 Hz to 20 000 Hz
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Amplitude")
    plt.legend()
    plt.show()


def lp_butterworth(signal, samplerate, cutoff, order, dry_wet = 1, show_plot = False):
    #print("Applying 'lp_butterworth' filter...")
    sig_fft = sci.fft.fft(signal)    # FFT of signal
    sig_freq = sci.fft.fftfreq(len(signal), 1/samplerate)  # Frequencies of fft

    filt = 1/np.sqrt(1 + (sig_freq/cutoff)**(2*order))  # Butterworth filter


    sig_filt_fft = sig_fft * filt   # Filtered frequencies

    # Plot power spectrum if boolean is true
    if show_plot:
        plt.plot(sig_freq, np.abs(sig_fft)**2, label = "Unfiltered Frequencies")
        plt.plot(sig_freq, np.abs(sig_filt_fft)**2, label = "Filtered Frequencies")
        plt.plot(sig_freq, filt, label = "Filter")
        plt.xscale("log")
        plt.show()

        plt.plot(sci.fft.ifft(sig_filt_fft).real)
        plt.show()

    signal = sci.fft.ifft(sig_filt_fft).real*dry_wet + signal*(1-dry_wet) # Inverse fft
    return signal

def ladder_test(signal, samplerate, cutoff, order, dry_wet = 1, show_plot = False):
    #print("Applying 'lp_butterworth' filter...")

    sig = signal.signal()

    # Plot power spectrum if boolean is true
    if show_plot:
        plt.plot(sig_freq, np.abs(sig_fft)**2, label = "Unfiltered Frequencies")
        plt.plot(sig_freq, np.abs(sig_filt_fft)**2, label = "Filtered Frequencies")
        plt.plot(sig_freq, filt, label = "Filter")
        plt.xscale("log")
        plt.show()

        plt.plot(sci.fft.ifft(sig_filt_fft).real)
        plt.show()

    return signal

def lp_4th_order(sig, cutoff, res):
    '''Function that applies a 4th order lowpass filter on a signal.
    Cutoff can be a 1D array of the same size as the signal.'''

    samples = np.empty(sig.length) 

    cutoff = cutoff*np.ones(sig.length)
    cutoff[cutoff<=0] = 0           # Making sure the cutoff stays within right bounds
    cutoff[cutoff>22000] = 22000

    fs = sig.sr
    cutoff = -np.exp(-(cutoff-43350)/4900) + 7000
    ff = 2 * cutoff / fs
    kk = 3.6*ff - 1.6*ff**2 -1
    pp = (kk+1)*0.5
    rr = res*15*np.ones(sig.length)

    y1=y2=y3=y4=oldx=oldy1=oldy2=oldy3=0


    for i, sample, k, p, r in zip(range(sig.length), sig.signal, kk, pp, rr):

        y1=(  sample - r*y4  )*p + oldx*p - k*y1
        y2=y1*p+oldy1*p - k*y2
        y3=y2*p+oldy2*p - k*y3
        y4=y3*p+oldy3*p - k*y4

        samples[i] = y4


    samples = samples
    #samples = temp
    samples = np.arctan(samples/1.6/np.max(samples))*1.6

    sig.signal = samples



def hp_butterworth(signal, cutoff, order, dry_wet = 1, show_plot = False):

    sig_fft = sci.fft.fft(signal.signal)    # FFT of signal
    sig_freq = sci.fft.fftfreq(signal.length, 1/signal.sr)  # Frequencies of fft

    filt = 1- 1/np.sqrt(1 + (sig_freq/cutoff)**(2*order))  # Butterworth filter


    sig_filt_fft = sig_fft * filt   # Filtered frequencies

    # Plot power spectrum if boolean is true
    if show_plot:
        plt.plot(sig_freq, np.abs(sig_fft)**2, label = "Unfiltered Frequencies")
        plt.plot(sig_freq, np.abs(sig_filt_fft)**2, label = "Filtered Frequencies")
        plt.plot(sig_freq, filt, label = "Filter")
        plt.xscale("log")
        plt.show()

        plt.plot(sci.fft.ifft(sig_filt_fft).real)
        plt.plot(signal.signal)
        plt.show()

    signal.signal = sci.fft.ifft(sig_filt_fft).real*dry_wet + signal.signal*(1-dry_wet) # Inverse fft





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

    #return signal





def reverb(signal, length, dry_wet, new_ir = True):
    '''
    Function to add reverb to signals.
    
    length: length of reverb's decay (in seconds)
    dry_wet: proportion of signal being wet and dry (1 -> wet, 0 -> dry)
    new_ir: generate a new random impulse response
    '''
    print("Adding some reverb...")
    x = np.arange(signal.length)

    if new_ir == True:
        kernel = np.exp(-x/(length*signal.sr))*np.random.randn(signal.length)
        kernel = kernel/np.sum(kernel)
         
        #np.savetxt("impulse_responses/test_ir.txt", kernel)
    else:
        kernel = np.loadtxt("impulse_responses/test_ir.txt")

    #plt.plot(kernel, label = "Kernel")
    #plt.plot(signal.signal, label = "Original Signal")


    signal.signal = fftconvolve(kernel, signal.signal)[0:signal.length]*dry_wet + signal.signal*(1-dry_wet)
    #plt.plot(signal.signal, label = "Convolve Signal")
    #plt.legend()
    #plt.show()
    return signal

def waveshaper(signal, intensity = 4, func = None):
    '''Waveshaping function to add distortion to signal.'''
    print("Applying waveshaping to signal...")
    if func == None:
        signal.signal = 1 - 2/(1+np.exp(intensity*signal.signal))
    else:
        signal.signal = func(signal.signal)

if __name__=="__main__":
    x = np.linspace(-5, 5, 1000)
    for i in range(3):
        y = butterworth(x, i+1)
        plt.plot(x, y, label = "Order: " + str(i+1))

    plt.legend()
    plt.show()
