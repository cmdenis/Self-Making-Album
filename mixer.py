import numpy as np
import scipy as sci
from scipy.io.wavfile import write



class Signal:
    '''Class that contains a signal'''
    def __init__(self, samplerate, duration, filename, save_samplerate = 44100):
        
        self.filename = filename                # Name of file
        self.samplerate = samplerate            # Sampling rate of array
        self.duration = int(np.ceil(duration))       # (Seconds)
        self.save_samplerate = save_samplerate  # Sample rate of saved file

        self.signal = np.zeros(samplerate*self.duration) # Signal
        self.length = duration * samplerate
    
    def __add__(self, x):
        new = Signal(self.samplerate, self.duration, self.filename)
        new.signal = self.signal + x.signal
        return new

    def save_sound(self):
        # Interpolate data to make sampling frequencies match
        print("Original signal is at", self.samplerate, "Hz sampling rate.")
        print("Saving signal at", self.save_samplerate, "Hz sampling rate.")
        og_smp = np.arange(self.duration*self.samplerate)
        new_smp = np.linspace(0, self.duration*self.samplerate, self.duration*self.save_samplerate)
        #plt.plot(self.signal[0:10])
        data = np.interp(new_smp, og_smp, self.signal)
        #plt.plot(data[0:10])
        #plt.show()
        # Normalizing and Making sure signal has correct amplitude
        data = np.iinfo(np.int16).max * data / np.max(data) / 10 

        # Write signal to disk
        write(self.filename, self.save_samplerate, data.astype(np.int16))

    def rms(self):
        '''Method to get the rms of the signal for mixing purposes.'''
        return np.sqrt(np.sum(self.signal**2)/self.length)

class MultiSignal():
    def __init__(self, seqs, sample_rate, filename, duration) -> None:
        self.nb_tracks = len(seqs.names) + 1
        self.names = seqs.names
        self.names.append("master")
        self.seqs = seqs
        self.sample_rate = sample_rate
        self.filname = filename
        self.duration = duration

        self.signals = [Signal(sample_rate, duration, filename[0:-4]+"_"+name+".wav") for name in self.names]

    def mix_signals(self):
        '''Method to mix the individual signals. To be refined'''
        # No mixing happening yet here
        for sig in self.signals[0:-1]:
            sig.signal = sig.signal/sig.rms

    def get_master(self):
        '''Method to put all the signals in the master signal together.'''
        for sig in self.signals[0:-1]:
            self.signals[-1].signal += sig.signal

    def play_sounds(self):
        '''Method to have each sequence play the sounds link to its instrument.'''
        for idx, seq in enumerate(self.seqs.sequences):
            seq.play_sound(self.signals[idx])





if __name__ == "__main__":

    get_master()

