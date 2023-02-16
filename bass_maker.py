from notes import Sequence, Event
import numpy as np
from synth import SineSynth, SawtoothSynth, BassSubstractiveSynth1
from effects import reverb, waveshaper, custom_norm

class BassSequence(Sequence):

    def __init__(self, bpm, chord_pattern, sr):
        super().__init__(bpm, chord_pattern, sr)
        
        self.name = "bass"

        self.sound = np.random.choice([SineSynth, SawtoothSynth, BassSubstractiveSynth1], p = [0, 0, 1])

    def hold_bass(self):
        '''Function to make a pattern of held down bass line'''

        print("╠ Using 'hold_bass'...")

        # First octave shift randomly all root notes for the bass line
        note_selection = self.chord_pattern.roots
        l = len(note_selection)
        note_selection = note_selection + 12*np.random.randint(low = 2, high = 4, size = l)
       

        lengths = self.chord_pattern.lengths                        # Lengths of each note
        starts = (np.cumsum(np.append(0, np.delete(lengths, -1))))*self.beat_time    # Time of start of each chords
        ends = np.cumsum(lengths)*self.beat_time                    # Time of end of each chords

        #print(starts)
        for start, end, note in zip(starts, ends, note_selection):
            #print(chord)
            #print(start)
            self.events.append(
                Event(
                    note,
                    start,
                    end,
                    channel=0
                )
            )
        
        print("╠═╗")
        print("╚═╝")

    def make_seq(self):
        '''Method to make the sequence of notes'''

        print("╔═══════════════════════╗")
        print("║ Making Bass Sequence  ║")
        print("╠═══════════════════════╝")

        # Choose which chord making procedure to make
        method = np.random.choice([self.hold_bass])

        method()

    def play_sound(self, sig):
        '''Function to synthesize sound'''
        print("\n==== 🔊 Synthesizing bass sound... ====")

        self.sound(self.bpm, self, sig).play()


        # Adding waveshaper
        waveshaper(sig, intensity=custom_norm(3, 12, 4, 3))

        # Adding reverb
        if 0.03 > np.random.rand():
            reverb(
                sig,                            # Signal
                custom_norm(0.01, 4, 0.5, 0.1), # Length of reverb
                custom_norm(0, 1, 0.05, 0.1)     # Dry/Wet Mix
            )

        sig.signal += sig.signal / sig.LUFS()

        