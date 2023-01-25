from notes import Sequence, Event
import numpy as np
from synth import SineSynth, SawtoothSynth, SubstractiveSynth1
from effects import reverb, waveshaper, custom_norm



class ChordSequence(Sequence):
    def __init__(self, bpm, chord_pattern, sr):
        super().__init__(bpm, chord_pattern, sr)
        
        self.name = "chords"

        self.sound = np.random.choice([SineSynth, SawtoothSynth, SubstractiveSynth1], p = [0.2, 0.2, 0.6])

    def hold_chord(self):
        '''Function to make a pattern of held down chords for one bar at a time.'''

        print("╠ Using 'hold_chord'...")

        # First make the notes in each chords
        chord_selection = self.chord_pattern.get_chord(
            [48, 72], # Midi notes range
        )
        #print(chord_selection)

        lengths = self.chord_pattern.lengths        # Lengths of each chords
        starts = (np.cumsum(np.append(0, np.delete(lengths, -1))))*self.beat_time     # Time of start of each chords
        ends = np.cumsum(lengths)*self.beat_time                 # Time of end of each chords

        #print(starts)
        for start, end, chord in zip(starts, ends, chord_selection):
            #print(chord)
            #print(start)
            for note in chord:
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
        print("║ Making Chord Sequence ║")
        print("╠═══════════════════════╝")

        # Choose which chord making procedure to make
        method = np.random.choice([self.hold_chord])

        method()

    def play_sound(self, sig):
        '''Function to synthesize sound'''
        print("\n==== 🎹 Synthesizing synth sound... ====")

        self.sound(self.bpm, self, sig).play()


        # Adding reverb
        if 0.1 > np.random.rand():
            reverb(
                sig,                            # Signal
                custom_norm(0.01, 4, 0.5, 0.5), # Length of reverb
                custom_norm(0, 1, 0.05, 0.2)     # Dry/Wet Mix
            )

        # Adding waveshaper
        #waveshaper(sig, intensity=custom_norm(3, 8, 4, 1))

        sig.signal += sig.signal / sig.LUFS()

        