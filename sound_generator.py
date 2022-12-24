import numpy as np
from scipy.io.wavfile import write
import scipy as sci
import matplotlib.pyplot as plt
from effects import *

class Signal:
    '''Class that contains a signal'''
    def __init__(self, samplerate, duration, filename, save_samplerate = 44100):
        
        self.filename = filename                # Name of file
        self.samplerate = samplerate            # Sampling rate of array
        self.duration = duration                # (Seconds)
        self.save_samplerate = save_samplerate  # Sample rate of saved file

        self.signal = np.zeros(samplerate*duration) # Signal
        self.length = duration * samplerate

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


def saw_synth(seq, file):
    # Loop over events in sequence
    print("Using 'saw_synth' generator...")
    for ev in seq:
        # Creating a sine wave
        samples = (ev.end - ev.start) * file.samplerate

        t0 = np.zeros(int(ev.start*file.samplerate))                       # Zeroes before start of sound
        t1 = sci.signal.sawtooth(2*np.pi*ev.pitch*np.arange(samples)/file.samplerate + np.pi)   # Sound
        t2 = np.zeros(int((file.duration - ev.end)*file.samplerate))              # Zeroes at the end of sound
        buffer = np.zeros(10)   # Buffer to make all arrays of equal length

        file.signal += np.concatenate((t0, t1, t2, buffer))[:file.samplerate*file.duration]

def ADSR(x, a, d, s, r, show_plot = False):
    '''Function to generate an ADSR enveloppe on data x'''
    if True: #x[-1] >= (a + d + r): In the future could possibly make this quicker by checking if signal is shorter then a,d,r
        attack = lambda x: x/a
        decay = lambda x: (a + d - a*s)/d - x*(1-s)/d
        sustain = lambda x: s
        pre_rel_x = x[x < (x[-1] - r)]
        pre_rel = np.piecewise(
            pre_rel_x, 
            [pre_rel_x < a, np.logical_and(a <= pre_rel_x, pre_rel_x < a+d), a+d<=pre_rel_x],
            [attack, decay, sustain]
        )

        release = x[-1]*pre_rel[-1]/r - pre_rel[-1]/r*x[x[-1] - r <= x]

        if show_plot == True:
            plt.plot(np.concatenate((pre_rel, release)))
            plt.show()

        return np.concatenate((pre_rel, release))

    attack = x[x<a]/a
    decay = (a + d - a*s)/d - x[np.logical_and(a <= x, x < a+d)]*(1-s)/d
    sustain = s + 0*x[np.logical_and(a+d <= x, x < x[-1]-r)]
    release = x[-1]*s/r - s/r*x[x[-1] - r <= x]

    return np.concatenate((attack, decay, sustain, release))

def substractive_synth_1(seq, file, cutoff, amp_adsr, waveshape_1, waveshape_2, pitch_1 = 0, pitch_2 = 0):
    print("Using 'substractive_synth_1' generator...")

    for ev in seq:
        amp_A, amp_D, amp_S, amp_R = amp_adsr

        # Making samples
        samples = np.arange((ev.end + amp_R - ev.start) * file.samplerate)/file.samplerate



        # Creating sound
        if waveshape_1 == 'sine':
            wave_1 = np.sin
        elif waveshape_1 == 'saw':
            wave_1 = lambda x: sci.signal.sawtooth(x + np.pi)
        elif waveshape_1 == 'square':
            wave_1 = sci.signal.square
        elif waveshape_1 == 'triangle':
            wave_1 = lambda x: sci.signal.sawtooth(x + np.pi/2, 0.5)
        else:
            print("Didn't recognize inputted 'waveshape_1'! Defaulting to 'sine'")
            wave_1 = np.sin

        if waveshape_2 == 'sine':
            wave_2 = np.sin
        elif waveshape_2 == 'saw':
            wave_2 = lambda x: sci.signal.sawtooth(x + np.pi)
        elif waveshape_2 == 'square':
            wave_2 = sci.signal.square
        elif waveshape_2 == 'triangle':
            wave_2 = lambda x: sci.signal.sawtooth(x + np.pi/2, 0.5)
        else:
            print("Didn't recognize inputted 'waveshape_2'! Defaulting to 'sine'")
            wave_2 = np.sin

        t0 = np.zeros(int(ev.start*file.samplerate))                       # Zeros before start of sound


        
        t1 = wave_1(2*np.pi*(ev.pitch+pitch_1)*samples)     # Create waveform 1
        t1 += wave_2(2*np.pi*(ev.pitch+pitch_2)*samples)    # Add waveform 2
        t1 = lp_butterworth(t1, file.samplerate, cutoff, 2)      # Add Butterworth LP filter                                 # Apply low-pass butterworth filter
        t1 = t1*ADSR(samples, amp_A, amp_D, amp_S, amp_R)   # Apply envelope
    

        t2 = np.zeros(int((file.duration - ev.end)*file.samplerate))              # Zeros at the end of sound
        buffer = np.zeros(10)   # Buffer to make all arrays of equal length

        file.signal += np.concatenate((t0, t1, t2, buffer))[:file.samplerate*file.duration]
        

def bass_drum(file, seq):
    print("Making a bass drum line...")

    # Making the bass drum sample
    length = 2
    pitch = 30
    pitch_mod = 6
    pitch_decay = 0.1
    amp_decay = 2

    x = np.arange(length*file.samplerate)/file.samplerate

    # Loop over events in sequence
    for ev in seq.events:
        # Creating a sine wave

        t0 = np.zeros(int(ev.start*file.samplerate))                       # Zeroes before start of sound
        t1 = np.sin(2*np.pi*((1-pitch_mod)*pitch_decay*np.exp(-x/pitch_decay) - (1-pitch_mod)*pitch_decay +x)*pitch)*np.exp(-x/amp_decay)   # Sound
        t2 = np.zeros(int((file.duration - (ev.start+length))*file.samplerate))              # Zeroes at the end of sound
        buffer = np.zeros(10)   # Buffer to make all arrays of equal length

        file.signal += np.concatenate((t0, t1, t2, buffer))[:file.samplerate*file.duration]




def white_noise(file):
    '''Generates a white noise signal'''
    print("Making White Noise...")
    file.signal = np.random.rand(file.length)*2 - 1