import numpy as np
from scipy.io.wavfile import write
from scipy.io import wavfile
import matplotlib.pyplot as plt

samplerate = 44100; fs = 100
t = np.linspace(0., 1., samplerate)
amplitude = np.iinfo(np.int16).max
data = amplitude * np.sin(2. * np.pi * fs * t)
write("example.wav", samplerate, data.astype(np.int16))



# Read file
samplerate, data = wavfile.read("example.wav")
times = np.arange(len(data))/samplerate


plt.plot(times, data)
plt.show()
