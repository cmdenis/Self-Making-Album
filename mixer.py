import numpy as np
import scipy as sci
from arrangement import make_arrangement
from signals import Signal 





class MultiSignal():
    def __init__(self, seqs, sample_rate, filename, duration) -> None:
        self.nb_tracks = len(seqs.names) + 1
        self.names = seqs.names
        self.names.append(filename)
        self.seqs = seqs
        self.sr = sample_rate
        self.save_sr = sample_rate
        self.filename = filename
        self.duration = duration

        #self.signals = [Signal(self.sr, duration, filename[0:-4]+"_"+name+".wav") for name in self.names]
        self.signals = [Signal(self.sr, duration, name) for name in self.names]

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

    def save_master(self):
        self.get_master()
        self.signals[-1].save_sound(mp3=True)





if __name__ == "__main__":


    # Make note data
    seqs = make_arrangement()
    max_time = seqs.last_time()

    # Instantiate signal
    sigs = MultiSignal(seqs, 44100, "audio_tests/output.wav", max_time + 2)

    # Synthesize sound
    sigs.play_sounds()

    # Save sound
    sigs.save_master()





