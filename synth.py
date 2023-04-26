import numpy as np
import scipy as sci
from effects import custom_norm, lp_butterworth, lp_4th_order
import matplotlib.pyplot as plt

def ADSR(x, a, d, s, r, k = -3, show_plot = False):
    '''Function to generate an ADSR enveloppe on data x'''
    if True: #x[-1] >= (a + d + r): In the future could possibly make this quicker by checking if signal is shorter then a,d,r
        val = 1-np.exp(-k)
        attack = lambda x: (1-np.exp(-k*x/a))/val
        decay = lambda x: 1 - (1-s)*(np.exp(k*(x-a)/d)-1)/(np.exp(k)-1)
        sustain = lambda x: s
        pre_rel_x = np.append(0, x[x < (x[-1] - r)])    # Appending a 0 in the begining in case the duration is 0
        pre_rel = np.piecewise(
            pre_rel_x, 
            [pre_rel_x < a, np.logical_and(a <= pre_rel_x, pre_rel_x < a+d), a+d<=pre_rel_x],
            [attack, decay, sustain]
        )

        #print(pre_rel_x)
        
        #release = (x[-1]*pre_rel[-1]/r - pre_rel[-1]/r*x[x[-1] - r <= x])[1:]
        release = (pre_rel[-1]*(1 - (np.exp(k*(x[x[-1] - r <= x]-x[-1]+r)/(r+0.000001))-1)/(np.exp(k)-1)))[1:]
        

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
        self.amp_R = 1 #custom_norm(0, 3, 0.05, 0.2)

        # Env1 
        self.env1_A = 0# custom_norm(0, 2, 0.1, 0.1)        # a, b, mean, sigma
        self.env1_D = 0.8 #custom_norm(0, 3, 0.2, 0.1)   # Should make a correlation with release parameter
        self.env1_S = 0#custom_norm(0, 1, 0.8, 0.1)
        self.env1_R = 0.8# custom_norm(0, 3, 0.05, 0.2)

        self.env1_filt_amt = 100

        # Filter
        # Should implement an envelope enventually
        self.cutoff = 40# custom_norm(300, 20000, 10000, 10000)
        self.resonance = custom_norm(0, 1, 0.3, 0.4)

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

    def play(self):
        print("Using 'substractive_synth_1' generator...")
        count = True
        for ev in self.seq.events:

            # Making samples
            samples = np.arange((ev.end + self.amp_R - ev.start) * self.sig.sr)/self.sig.sr

            t0 = np.zeros(int(ev.start*self.sig.sr))                       # Zeros before start of sound

            t1 = self.wave_1(2*np.pi*(ev.pitch*(1 + self.pitch_1)*samples))     # Create waveform 1
            t1 += self.wave_2(2*np.pi*(ev.pitch*(1 + self.pitch_2)*samples))    # Add waveform 2

            filt_env = self.cutoff + self.env1_filt_amt*ADSR(samples, self.env1_A, self.env1_D, self.env1_S, self.env1_R)
            if count == True:
                #plt.plot(samples, filt_env)
                #plt.show()
                count = False

            t1 = lp_4th_order(t1, filt_env, self.resonance, self.sig.sr)
            t1 = t1*ADSR(samples, self.amp_A, self.amp_D, self.amp_S, self.amp_R)   # Apply envelope
    
        
            t2 = np.zeros(int((self.sig.duration - ev.end)*self.sig.sr))              # Zeros at the end of sound
            buffer = np.zeros(10)   # Buffer to make all arrays of equal length

            self.sig.signal += np.concatenate((t0, t1, t2, buffer))[:self.sig.sr*self.sig.duration]
        
        #self.sig.signal = lp_4th_order(self.sig.signal, self.cutoff, self.resonance, self.sig.sr)      # Add Butterworth LP filter                                 # Apply low-pass butterworth filter

class BassSubstractiveSynth1(SubstractiveSynth1):
    def __init__(self, bpm, seq, sig) -> None:
        super().__init__(bpm, seq, sig)   

        self.name = "bass_substractive_synth1"
        
        # Synth parameters
        # a, b, mean, sigma

        # Amp enveloppe
        self.amp_A = custom_norm(0, 2, 0.05, 0.1)        # a, b, mean, sigma
        self.amp_D = custom_norm(0, 3, 0.2, 0.1)   # Should make a correlation with release parameter
        self.amp_S = custom_norm(0, 1, 0.8, 0.1)
        self.amp_R = custom_norm(0, 3, 0.05, 0.2)

        # Filter
        # Shoudl implement an envelope enventually
        if np.random.rand() < 0.:
            # Fixed cutoff
            self.cutoff = custom_norm(300, 20000, 10000, 10000)
            self.resonance = custom_norm(0, 1, 0.3, 0.4)
        else:
            # LFO modulated cutoff
            base_freq = custom_norm(300, 20000, 10000, 10000)
            lfo_amt = 5000#custom_norm(10, 15000, 300, 500)
            lfo_freq = 1/seq.beat_time * np.random.choice([0.25, 0.5, 1, 2, 4])
            self.cutoff = base_freq + lfo_amt*np.cos(np.linspace(0, sig.duration, sig.length)*2*np.pi*lfo_freq)
            self.resonance = custom_norm(0, 1, 0.3, 0.4)

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

class ChordSubstractiveSynth1(SubstractiveSynth1):
    def __init__(self, bpm, seq, sig) -> None:
        super().__init__(bpm, seq, sig)   

        self.name = "chord_substractive_synth1"
        
        # Synth parameters
        # a, b, mean, sigma

        # Amp enveloppe
        self.amp_A = custom_norm(0, 2, 0.05, 0.1)        # a, b, mean, sigma
        self.amp_D = custom_norm(0, 3, 0.2, 0.1)   # Should make a correlation with release parameter
        self.amp_S = custom_norm(0, 1, 0.8, 0.1)
        self.amp_R = custom_norm(0, 3, 0.05, 0.2)

        # Filter
        # Shoudl implement an envelope enventually
        self.cutoff = custom_norm(300, 20000, 10000, 10000)

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

class MelodySubstractiveSynth1(SubstractiveSynth1):
    def __init__(self, bpm, seq, sig) -> None:
        super().__init__(bpm, seq, sig)   

        self.name = "melody_substractive_synth1"
        
        # Synth parameters
        # a, b, mean, sigma

        # Amp enveloppe
        self.amp_A = custom_norm(0, 2, 0.05, 0.1)        # a, b, mean, sigma
        self.amp_D = custom_norm(0, 3, 0.2, 0.1)   # Should make a correlation with release parameter
        self.amp_S = custom_norm(0, 1, 0.8, 0.1)
        self.amp_R = custom_norm(0, 3, 0.05, 1)

        # Filter
        # Shoudl implement an envelope enventually
        self.cutoff = custom_norm(300, 20000, 10000, 10000)

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


        # Choosing a style of synth that will "correct the default parameeters"
        style = np.random.choice(
            [
                #self.panw,
                #self.plucky,
                self.hold,
                #self.smooth
            ]
        )

        style()

        if True:
            print("Amp ADSR:", self.amp_A, self.amp_D, self.amp_S, self.amp_R)
            print("Env1 ADSR:", self.env1_A, self.env1_D, self.env1_S, self.env1_R)
            print("Cutoff:", self.cutoff, "Hz")
            print("OSC 1 Detune:", self.pitch_1)
            print("OSC 1 Wave:", self.wave_1)
            print("OSC 2 Detune:", self.pitch_2)
            print("OSC 2 Wave:", self.wave_2)   

    def plucky(self):
        print("Using synth preset: 'plucky'")
        self.amp_A = custom_norm(0, 2, 0.001, 0.001)        # a, b, mean, sigma
        self.amp_D = custom_norm(0.05, 3, 0.3, 1)   # Should make a correlation with release parameter
        self.amp_S = 0
        self.amp_R = self.amp_D

        self.cutoff = custom_norm(30, 20000, 1000, 4000)
        self.env1_filt_amt = custom_norm(0, 20000, 1000, 10000)

        # Env1 
        self.env1_A = custom_norm(0, 2, 0.001, 0.001)        # a, b, mean, sigma
        self.env1_D = custom_norm(0, 3, 0.2, 0.1)   # Should make a correlation with release parameter
        self.env1_S = custom_norm(0, 1, 0.3, 0.1)
        self.env1_R = self.amp_D

    def pwouet(self):
        print("Using synth preset: 'pwouet'")
        self.amp_A = custom_norm(0, 2, 0.001, 0.001)        # a, b, mean, sigma
        self.amp_D = custom_norm(0.05, 3, 0.3, 1)   # Should make a correlation with release parameter
        self.amp_S = custom_norm(0, 1, 0.5, 0.5)
        self.amp_R = custom_norm(0.05, 3, 0.01, 1)

        self.cutoff = custom_norm(20, 20000, 20, 200)
        self.env1_filt_amt = custom_norm(1000, 20000, 2000, 10000)
        self.resonance = custom_norm(0, 1, 0.3, 0.5)

        # Env1 
        self.env1_A = custom_norm(0.1, 2, 0.1, 0.15)        # a, b, mean, sigma
        self.env1_D = custom_norm(0, 3, 0.2, 0.1)   # Should make a correlation with release parameter
        self.env1_S = custom_norm(0, 1, 0.5, 0.5)
        self.env1_R = self.env1_D

    def panw(self):
        print("Using synth preset: 'panw'")
        self.amp_A = custom_norm(0, 2, 0.001, 0.001)        # a, b, mean, sigma
        self.amp_D = custom_norm(0.05, 3, 0.3, 1)   # Should make a correlation with release parameter
        self.amp_S = custom_norm(0, 1, 0.5, 0.5)
        self.amp_R = custom_norm(0.05, 3, 0.01, 0.05)

        self.cutoff = custom_norm(20, 20000, 20, 200)
        self.env1_filt_amt = custom_norm(1000, 20000, 2000, 10000)
        self.resonance = custom_norm(0, 1, 0.3, 0.5)

        # Env1 
        self.env1_A = custom_norm(0, 1, 0.001, 0.05)        # a, b, mean, sigma
        self.env1_D = custom_norm(0, 3, 0.25, 0.05)  
        self.env1_S = custom_norm(0, 1, 0.8, 0.1) 
        self.env1_R = custom_norm(0, 3, 0.2, 0.1)

    def hold(self):
        print("Using synth preset: 'hold'")
        self.amp_A = custom_norm(0, 2, 0.001, 0.001)        # a, b, mean, sigma
        self.amp_D = custom_norm(0.05, 3, 0.3, 1)           # Should make a correlation with release parameter
        self.amp_S = custom_norm(0, 1, 1, 0.1)
        self.amp_R = custom_norm(0.05, 3, 0.01, 0.05)

        self.cutoff = custom_norm(20, 20000, 20, 200)
        self.env1_filt_amt = custom_norm(1000, 20000, 200, 8000)
        self.resonance = custom_norm(0, 1, 0.3, 0.5)

        # Env1 
        self.env1_A = custom_norm(0, 1, 0.001, 0.01)        # a, b, mean, sigma
        self.env1_D = custom_norm(0, 3, 0.25, 0.05)  
        self.env1_S = custom_norm(0, 1, 1, 0.1) 
        self.env1_R = custom_norm(0, 3, 0.05, 0.01)

    def smooth(self):
        print("Using synth preset: 'smooth'")
        self.amp_A = custom_norm(0, 2, 0.1, 0.1)        # a, b, mean, sigma
        self.amp_D = custom_norm(0.05, 3, 0.3, 1)           # Should make a correlation with release parameter
        self.amp_S = custom_norm(0, 1, 0.9, 0.1)
        self.amp_R = custom_norm(0.05, 3, 0.5, 0.05)

        self.cutoff = custom_norm(20, 20000, 300, 5000)
        self.env1_filt_amt = custom_norm(0, 20000, 2000, 5000)
        self.resonance = custom_norm(0, 1, 0.3, 0.5)

        # Env1 
        self.env1_A = custom_norm(0, 1, 0.1, 0.05)        # a, b, mean, sigma
        self.env1_D = custom_norm(0, 3, 0.25, 0.05)  
        self.env1_S = custom_norm(0, 1, 0.9, 0.1) 
        self.env1_R = custom_norm(0, 3, 0.5, 0.1)