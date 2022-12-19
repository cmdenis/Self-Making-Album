import numpy as np
from scipy.io.wavfile import write
from scipy.io import wavfile
import matplotlib.pyplot as plt
from notes import *
from effects import *

# Script to make a random sequence based on the random note generator

# Global data
filename = "random_sine.wav"
samplerate = 44100  # Sampling rate
length = 5 # (Seconds)

signal = np.zeros(samplerate*length)



# Make major scale
major = Scale(np.array([0, 2, 4, 5, 7, 9, 11]), 0)

sequence = play_random(
    major,
    [48, 84],
    8,
    0.5
)

def sine_synth(seq, file):
    # Loop over events in sequence
    for ev in seq:

        # Creating a sine wave
        samples = (ev.end - ev.start) * samplerate

        t0 = np.zeros(int(ev.start*samplerate))                       # Zeroes before start of sound
        t1 = np.sin(2*np.pi*ev.pitch*np.arange(samples)/samplerate)   # Sound
        t2 = np.zeros(int((length - ev.end)*samplerate))              # Zeroes at the end of sound
        buffer = np.zeros(10)   # Buffer to make all arrays of equal length

        file += np.concatenate((t0, t1, t2, buffer))[:samplerate*length]


# Create sine sequence  
print("Creating Sine Sequence...")
sine_synth(sequence, signal)

# Add some reverb
signal = reverb(signal, samplerate*0.5, new_ir=True)









signal =signal / np.max(signal)/10 # Normalizing
# Making sure signal has correct amplitude
data = np.iinfo(np.int16).max * signal
write(filename, samplerate, data.astype(np.int16))



# Read file
#samplerate, data = wavfile.read(filename)
#times = np.arange(len(data))/samplerate


#plt.plot(times, data/np.max(data))
#plt.xlabel("Time (s)")
#plt.ylabel("Amplitude")
#plt.show()
