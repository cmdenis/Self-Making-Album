import numpy as np
from scipy.io.wavfile import write
from scipy.io import wavfile
import matplotlib.pyplot as plt


def sine_synth(seq, file):
    # Loop over events in sequence
    print("Using 'sine_synth' generator...")
    for ev in seq:
        # Creating a sine wave
        samples = (ev.end - ev.start) * file.samplerate

        t0 = np.zeros(int(ev.start*file.samplerate))                       # Zeroes before start of sound
        t1 = np.sin(2*np.pi*ev.pitch*np.arange(samples)/file.samplerate)   # Sound
        t2 = np.zeros(int((file.duration - ev.end)*file.samplerate))              # Zeroes at the end of sound
        buffer = np.zeros(10)   # Buffer to make all arrays of equal length

        file.signal += np.concatenate((t0, t1, t2, buffer))[:file.samplerate*file.duration]
