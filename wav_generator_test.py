import numpy as np
from scipy.io.wavfile import write
from scipy.io import wavfile
import matplotlib.pyplot as plt


# Global data
filename = "test.wav"
samplerate = 44100  # Sampling rate
length = 7 # (Seconds)


class Event:
    def __init__(self, pitch, start, end):
        # Handling possible misuse cases
        if start > end:
            raise NameError("Starting Time is After End Time...")
        if start < 0:
            raise NameError("Starting Time Before 0...")
        if end > length:
            raise NameError("Ending time greater than duration of the song...")

        
        # Initializing attributes
        self.pitch = pitch              # Pitch of sound (Hz)
        self.start = start              # Time of start of sound
        self.end = end                  # Time of end of sound
        #self.modulation = modulation   # Array with modulation data, WIP

    def sine(self):
        # Creating a sine wave

        samples = (self.end - self.start) * samplerate

        t0 = np.zeros(int(self.start*samplerate))                       # Zeroes before start of sound
        t1 = np.sin(2*np.pi*self.pitch*np.arange(samples)/samplerate)   # Sound
        t2 = np.zeros(int((length - self.end)*samplerate))              # Zeroes at the end of sound
        buffer = np.zeros(10)   # Buffer to make all arrays of equal length

        return np.concatenate((t0, t1, t2, buffer))[:samplerate*length]

    

beep1 = Event(200, 0.5, 3)
beep2 = Event(1000, 0.6, 3)
beep3 = Event(2000, 0.7, 3)
beep4 = Event(500, 4, 4.5)
beep5 = Event(700, 4.5, 5)
beep6 = Event(1000, 5, 5.5)

# Making a list of events.
# Each events corresponds to the start of a musical note (or sound)
# There 
event_list = np.array([
    beep1.sine(),
    beep2.sine(),
    beep3.sine(),
    beep4.sine(),
    beep5.sine(),
    beep6.sine()
])



signal = np.sum(event_list, axis = 0) 

signal = signal / np.max(signal) # Normalizing


# Making sure signal has correct amplitude
data = np.iinfo(np.int16).max * signal/1.1
write(filename, samplerate, data.astype(np.int16))



# Read file
samplerate, data = wavfile.read(filename)
times = np.arange(len(data))/samplerate


plt.plot(times, data/np.max(data))
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.show()
