import numpy as np
from scipy.io.wavfile import write
from effects import hp_butterworth
import scipy as sci
try:
    from pydub import AudioSegment
except:
    print("Warning! It seems you do not have pydub installed... Everything **should** run fine as long as you don't try to convert anything to MP3...")
import os

class Signal:
    '''Class that contains a signal'''
    def __init__(self, samplerate, duration, filename, save_samplerate = 44100):
        
        self.filename = filename                # Name of file
        self.sr = samplerate            # Sampling rate of array
        self.duration = int(np.ceil(duration))       # (Seconds)
        self.save_samplerate = save_samplerate  # Sample rate of saved file

        self.signal = np.zeros(samplerate*self.duration) # Signal (mid part)
        self.signal_side = np.zeros(samplerate*self.duration) # Signal (side part)
        self.length = self.duration * samplerate
    
    def __add__(self, x):
        new = Signal(self.sr, self.duration, self.filename)
        new.signal = self.signal + x.signal
        return new

    def save_sound(self, mp3 = False, stereo = False):



        # Interpolate data to make sampling frequencies match
        print("\n==== 💾 Saving to disk... ====")
        print("Original signal is at", self.sr, "Hz sampling rate.")
        print("Saving signal at", self.save_samplerate, "Hz sampling rate.")
        og_smp = np.arange(self.duration*self.sr)
        new_smp = np.linspace(0, self.duration*self.sr, self.duration*self.save_samplerate)
        #plt.plot(self.signal[0:10])
        data = np.interp(new_smp, og_smp, self.signal)
        #plt.plot(data[0:10])
        #plt.show()
        # Normalizing and Making sure signal has correct amplitude
        data = np.iinfo(np.int16).max * data / np.max(np.abs(data))
        print(np.max(data))

        # Write signal to disk
        if stereo:
            self.stereo_signal = np.column_stack((self.sig_l, self.sig_r))
            write(self.filename, self.save_samplerate, self.stereo_signal)
        else:
            write(self.filename, self.save_samplerate, data.astype(np.int16))
        
        if mp3 == True:
            AudioSegment.from_wav(self.filename).export(self.filename[0:-4]+".mp3", format="mp3")
            os.remove(self.filename)

    def rms(self):
        '''Method to get the rms of the signal for mixing purposes.'''
        return np.sqrt(np.sum(self.signal**2)/self.length)

    def LUFS(self):
        cutoff = 500
        order = 1
        sig_fft = sci.fft.fft(self.signal)    # FFT of signal
        sig_freq = sci.fft.fftfreq(self.length, 1/self.sr)  # Frequencies of fft

        filt = 1- 1/np.sqrt(1 + (sig_freq/cutoff)**(2*order))  # Butterworth filter

        
        sig_filt_fft = sig_fft * filt   # Filtered frequencies
        new = sci.fft.ifft(sig_filt_fft).real  # Inverse fft)
        return np.sqrt(np.sum(new**2)/self.length)
    
    def ms_to_stereo(self):
        self.sig_l = self.signal + self.signal_side
        self.sig_r = self.signal - self.signal_side

    