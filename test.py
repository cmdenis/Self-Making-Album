import numpy as np
from scipy.io.wavfile import write
import struct
import matplotlib.pyplot as plt
from signals import *
import numba as nb

# Set the parameters for the noise
samplerate = 44100
duration = 120
frequency = 1000

sig = Signal(samplerate, duration, "")

# Generate the white noise
sig.signal = (np.random.rand(samplerate * duration) * 2) - 1



#plt.plot(scales)
#plt.show()

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

lp_4th_order(sig, 1000 + 1000*np.sin(np.linspace(0, 120, 44100*120)*2*np.pi), 1)

to_exp = sig.signal
to_exp = to_exp.astype(np.float32)

#print("Mean:", np.mean(to_exp))
#print("Max:", np.max(to_exp))

filename = 'white_noise_lowpass_500Hz.wav'
write(filename, samplerate, to_exp)

# Plot the frequency spectrum of the filtered noise
'''f = np.fft.fftfreq(samplerate*duration, d=1 / samplerate)
Y = np.abs(np.fft.fft(to_exp))

plt.loglog(f, Y, label='frequency spectrum')
plt.legend()
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude')
plt.xlim([0, 20000])
plt.show()'''
