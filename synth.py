import numpy as np
import scipy as sci
from effects import custom_norm, lp_butterworth
import matplotlib.pyplot as plt

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

class Synth:
    def __init__(self, bpm, seq, sig) -> None:
        self.bpm = bpm  # BPM
        self.seq = seq  # Sequence of notes
        self.sig = sig  # Signal

    def print_name(self):
        print("Using", self.name, "generator...")


class SineSynth(Synth):
    def __init__(self, bpm, seq, sig) -> None:
        super().__init__(bpm, seq, sig)
        self.name = "sine_synth"

    def play(self):
        # Loop over events in sequence
        self.print_name()
        for ev in self.seq.events:
            # Creating a sine wave
            samples = (ev.end - ev.start) * self.sig.sr

            t0 = np.zeros(int(ev.start*self.sig.sr))                       # Zeroes before start of sound
            t1 = np.sin(2*np.pi*ev.pitch*np.arange(samples)/self.sig.sr)   # Sound
            t2 = np.zeros(int((self.sig.duration - ev.end)*self.sig.sr))              # Zeroes at the end of sound
            buffer = np.zeros(10)   # Buffer to make all arrays of equal length

            self.sig.signal += np.concatenate((t0, t1, t2, buffer))[:self.sig.sr*self.sig.duration]

class SawtoothSynth(Synth):
    def __init__(self, bpm, seq, sig) -> None:
        super().__init__(bpm, seq, sig)
        self.name = "sawtooth_synth"

    def play(self):
        # Loop over events in sequence
        self.print_name()
        for ev in self.seq.events:
            # Creating a sine wave
            samples = (ev.end - ev.start) * self.sig.sr

            t0 = np.zeros(int(ev.start*self.sig.sr))                       # Zeroes before start of sound
            t1 = sci.signal.sawtooth(2*np.pi*ev.pitch*np.arange(samples)/self.sig.sr + np.pi)   # Sound
            t2 = np.zeros(int((self.sig.duration - ev.end)*self.sig.sr))              # Zeroes at the end of sound
            buffer = np.zeros(10)   # Buffer to make all arrays of equal length

            self.sig.signal += np.concatenate((t0, t1, t2, buffer))[:self.sig.sr*self.sig.duration]

    
class SubstractiveSynth1(Synth):
    def __init__(self, bpm, seq, sig) -> None:
        super().__init__(bpm, seq, sig)

        self.name = "substractive_synth1"
        
        # Synth parameters
        # a, b, mean, sigma

        # Amp enveloppe
        self.amp_A = custom_norm(0, 2, 0.05, 0.1)        # a, b, mean, sigma
        self.amp_D = custom_norm(0, 3, 0.2, 0.1)   # Should make a correlation with release parameter
        self.amp_S = custom_norm(0, 1, 0.8, 0.1)
        self.amp_R = custom_norm(0, 3, 0.05, 0.2)

        # Filter
        # Shoudl implement an envelope enventually
        self.cutoff = custom_norm(300, 20000, 10000, 5000)

        # OSC 1
        self.wave_1 = np.random.choice(
            [np.sin, lambda x: sci.signal.sawtooth(x + np.pi), sci.signal.square, lambda x: sci.signal.sawtooth(x + np.pi/2, 0.5)],
            p = [0.15, 0.45, 0.3, 0.1]
        )
        self.pitch_1 = custom_norm(-1, 1, 0, 0.02)*(2**(1/12)-1)

        # OSC 2
        self.wave_2 = np.random.choice(
            [np.sin, lambda x: sci.signal.sawtooth(x + np.pi), sci.signal.square, lambda x: sci.signal.sawtooth(x + np.pi/2, 0.5)],
            p = [0.15, 0.45, 0.3, 0.1]
        )
        self.pitch_2 = custom_norm(-1, 1, 0, 0.02)*(2**(1/12)-1)

        if True:
            print("ADSR:", self.amp_A, self.amp_D, self.amp_S, self.amp_R)
            print("Cutoff:", self.cutoff, "Hz")
            print("OSC 1 Detune:", self.pitch_1)
            print("OSC 1 Wave:", self.wave_1)
            print("OSC 2 Detune:", self.pitch_2)
            print("OSC 2 Wave:", self.wave_2)


    def play(self):
        print("Using 'substractive_synth_1' generator...")

        for ev in self.seq.events:

            # Making samples
            samples = np.arange((ev.end + self.amp_R - ev.start) * self.sig.sr)/self.sig.sr

            t0 = np.zeros(int(ev.start*self.sig.sr))                       # Zeros before start of sound

            t1 = self.wave_1(2*np.pi*(ev.pitch*(1 + self.pitch_1)*samples))     # Create waveform 1
            t1 += self.wave_2(2*np.pi*(ev.pitch*(1 + self.pitch_2)*samples))    # Add waveform 2
            t1 = lp_butterworth(t1, self.sig.sr, self.cutoff, 2)      # Add Butterworth LP filter                                 # Apply low-pass butterworth filter
            t1 = t1*ADSR(samples, self.amp_A, self.amp_D, self.amp_S, self.amp_R)   # Apply envelope
        
            t2 = np.zeros(int((self.sig.duration - ev.end)*self.sig.sr))              # Zeros at the end of sound
            buffer = np.zeros(10)   # Buffer to make all arrays of equal length

            self.sig.signal += np.concatenate((t0, t1, t2, buffer))[:self.sig.sr*self.sig.duration]
            