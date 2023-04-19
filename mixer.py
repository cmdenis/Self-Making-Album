import numpy as np
import scipy as sci
from arrangement import make_arrangement
from signals import Signal 
from effects import lp_4th_order, custom_norm, flanger, waveshaper
import matplotlib.pyplot as plt






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
        self.length = duration*sample_rate

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

        self.signals[-1].signal_side /= np.max(self.signals[-1].signal)
        self.signals[-1].signal /= np.max(self.signals[-1].signal)


    def play_sounds(self):
        '''Method to have each sequence play the sounds link to its instrument.'''
        for idx, seq in enumerate(self.seqs.sequences):
            
            seq.play_sound(self.signals[idx])

    def apply_master_effects(self):
        '''Function to apply some effects on the master track'''
        print("\n\n==== 🎛️ Applying effects to master channel... ====")
        self.get_master()

        #plt.plot(self.signals[-1].signal)
        #plt.show()
        # Sweeping low-pass
        if np.random.rand() < 0.1:
            print("Applying filter sweep")
            cutoff_sweep = np.sin(np.linspace(0, self.duration, self.signals[-1].length)*2*np.pi*(np.random.rand()/3+0.1) )*custom_norm(100, 10000, 2000, 1000) + custom_norm(500, 10000, 4000, 1000)

            self.signals[-1].signal = lp_4th_order(self.signals[-1].signal, cutoff_sweep, 0., self.signals[-1].length, self.sr)
            #plt.plot(self.signals[-1].signal)
            #plt.show()

        if np.random.rand() < 0.1:
            ws = custom_norm(0, 6, 0.2, 0.2) + np.random.choice([0, 3], p=[0.7, 0.3])
            print("Using waveshaper with parameter:", ws)
            waveshaper(self.signals[-1], ws)

        if True:#np.random.rand() < 0.1:
            delay = int(custom_norm(1, 30, 10, 10))
            print("Using flanger with delay:", delay, "samples")
            self.signals[-1].ms_to_stereo()
            self.signals[-1].sig_l = flanger(self.signals[-1].sig_l, delay)
            self.signals[-1].sig_r = flanger(self.signals[-1].sig_r, delay + 10)
            #self.signals[-1].sig_r = np.zeros(len( self.signals[-1].sig_r))

        if False:
            delay = int(self.seqs.beat_time*44100*np.random.choice(1/8, 1/4, 1/2, 1))
            times = np.random.choice(1, 2, 3, 4)
            print("Using ping pong delay:", delay/44100/self.seqs.beat_time)

            self.signals[-1].ms_to_stereo()
            self.signals[-1].sig_l = np.append(self.signals[-1].sig_l, np.zeros(int((1 + times)*delay)))
            self.signals[-1].sig_r = np.append(self.signals[-1].sig_l, np.zeros(int((1 + times)*delay)))
            for i in range(times):
                0==1


        



        print("Normalizing master track signal...")
        self.signals[-1].signal = self.signals[-1].signal/np.max(self.signals[-1].signal)

    def save_master(self, mp3 = False):
        self.signals[-1].save_sound(mp3=mp3, stereo=False)


def make_music(seed, sample_rate, filename, mp3 = True):
    '''Function that makes the music'''
    print("Using Seed:", seed, "\n")
    # Make note data
    seqs = make_arrangement()
    max_time = seqs.last_time()

    # Store notes to disk
    seqs.write_note_data()



    # Instantiate signal
    
    sigs = MultiSignal(seqs, sample_rate, filename+".wav", max_time + 2)
    # Synthesize sound
    sigs.play_sounds()
    # Get Master track
    sigs.get_master()
    # Add master effects
    #sigs.apply_master_effects()
    # Save sound
    sigs.save_master(mp3 = False)


if __name__ == "__main__":
    s = np.random.randint(0, 100000000)
    np.random.seed(s)
    
    make_music(s, 44100, "audio_tests/output", mp3=False)





