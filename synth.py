import numpy as np
import scipy as sci



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

    def sine_synth(self):
        # Loop over events in sequence
        self.print_name()
        for ev in self.seq:
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

    def sine_synth(self):
        # Loop over events in sequence
        self.print_name()
        for ev in self.seq:
            # Creating a sine wave
            samples = (ev.end - ev.start) * self.sig.sr

            t0 = np.zeros(int(ev.start*self.sig.sr))                       # Zeroes before start of sound
            t1 = sci.signal.sawtooth(2*np.pi*ev.pitch*np.arange(samples)/self.sig.sr + np.pi)   # Sound
            t2 = np.zeros(int((self.sig.duration - ev.end)*self.sig.sr))              # Zeroes at the end of sound
            buffer = np.zeros(10)   # Buffer to make all arrays of equal length

            self.sig.signal += np.concatenate((t0, t1, t2, buffer))[:self.sig.sr*self.sig.duration]

    