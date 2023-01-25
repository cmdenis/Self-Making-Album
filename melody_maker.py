from notes import Sequence, Event
import numpy as np
from synth import SineSynth, SawtoothSynth, SubstractiveSynth1
from effects import reverb, waveshaper, custom_norm

class MelodySequence(Sequence):

    def __init__(self, bpm, chord_pattern, sr):
        super().__init__(bpm, chord_pattern, sr)
        self.name = "melody"

        self.sound = np.random.choice([SineSynth, SawtoothSynth, SubstractiveSynth1], p = [0.10, 0.10, 0.80])

    def arpeggio_melody(self):
        '''Method to make an arpeggio based on the chords used. Will randomly select amongst different arpegiating patterns.'''
        print("╠ Using 'arpeggio_melody'...")




        # First make the notes in each chords
        chord_selection = self.chord_pattern.select_note_range(
            [48, 80], # Midi notes range
        )
        #print(chord_selection)

        lengths = self.chord_pattern.lengths        # Lengths of each chords
        starts = (np.cumsum(np.append(0, np.delete(lengths, -1))))*self.beat_time     # Time of start of each chords
        #print("the starts are:", starts)
        ends = np.cumsum(lengths)*self.beat_time                 # Time of end of each chords
        #print("the ends are:", ends)

        prob = np.array([30, 20, 25, 5, 5])
        note_length = np.random.choice([0.25, 0.5, 1, 0.25, 4], p=prob/np.sum(prob))*self.beat_time
        #print(note_length)
        # Circulate through chords
        for start, end, chord in zip(starts, ends, chord_selection):
            # Pick notes to play for chord pattern
            nb_notes = np.random.randint(3, 6)
            #print(nb_notes)
            #print(len(chord))
            notes = np.tile(np.random.choice(chord, size = nb_notes), 16)
            # Make start and end of each note:
            note_starts = np.arange(start, end, note_length)
            note_ends = note_starts + note_length
            # fix last note length
            note_ends[-1] = end
            notes = notes[:len(note_ends)]
            #print(note_ends, note_starts, notes)
            assert(len(notes)==len(note_starts)==len(note_ends))
            
            for note, note_start, note_end in zip(notes, note_starts, note_ends):
                self.events.append(
                    Event(
                        note,
                        note_start,
                        note_end,
                        channel=0
                    )
                )
        
        print("╠═╗")
        print("╚═╝")

    def make_seq(self):
        '''Method to make the sequence of notes'''

        print("╔═══════════════════════╗")
        print("║Making Melodic Sequence║")
        print("╠═══════════════════════╝")

        # Choose which chord making procedure to make
        method = np.random.choice([self.arpeggio_melody])

        method()

    def play_sound(self, sig):
        '''Function to synthesize sound'''
        print("\n==== 🎵 Synthesizing melody sound... ====")

        # Calling sound generator method
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

        sig.signal += sig.signal / sig.LUFS()*2
        