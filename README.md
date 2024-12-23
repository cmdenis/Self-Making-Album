# Self-Making-Album

## Explanations

Hello!

You have stumbled on my procedural music project. The project should be in somewhat working order. So far it is very basic and produces pretty crappy tunes... but hey I can call them tunes, so that's already pretty cool... There's some audio demos in the `audio_tests` folder. 

**If you want to try it out yourself, I invite you to clone the repo and run the `meta.py` file script on your own machine.**

 Everything uses the `numpy`, `scipy`, `matplotlib`, `os` and `pydub` libraries, so if you've got those, you should be good to go. `pydub` is only used to convert the `.wav` files to `.mp3`, to make things lighter, but if you don't convert stuff, you won't need it. Just make sure to turn off any settings converting stuff to MP3. 

### Structure

Here is a little explanation at how this system works. It works in a couple of distinct step. You could think of it in this way:
1. Meta info generation -> generates all "meta" info, such as the number of instruments, the BPM, the key, etc.
2. Notes and rhythm generation -> generates all the notes and rythms to be played (based on the constraints, e.g. key, BPM). In a way, this steps makes some pseudo MIDI info or sheet music for the computer if you will.
3. Sound design generation -> procedurally makes the synth's sounds by tweaking through a bunch of parameters, envelopes, filters, waveshape, detuning, etc. This is done not only for synths, but also for the percussions (for instance, the bass drum has its length, root note, envelope, etc. all being adjusted procedurally)
4. Making the song -> the "pseudo-midi" (I'm calling it pseudo midi cause it's not really MIDI, but effectively does pretty much the same within the scope of this script) is fed through the instruments. Then a sound file is generated by combining them together.

Overall, everything is procedural, but as the designer, I chose certain parameter regions that I know sound a certain way to avoid too much unpleasantness. 

### Areas of improvements

- More elaborate chord progressions, and also more elaborate melody and bass generation (based on the chords).
- I'm thinking that it would be cool to map our different regions in parameter space for different styles of synths. The multidimensional landscape in which the synth programming exist is most likely multimodal and it would be nice to capture this in a nicer way than the currect way I'm doing it (by just defining a bunch of categories of instruments, like bass, pad, arp, etc. and for each of these categories defining the distribution of parameters).
- Sync up some modulation parameters with time (is this already done maybe?)
- Way to add section to songs while maintaining both tonal and timbral cohesion accross a song.

## Random Stuff

The idea here is to make a bunch of interelated scripts which will generate a musical album. In this repo, I'll make some sound engines to make noise. I'll also make some automated composition tools which will randomly be able to select from a set of chord and melody generating algorithms.

If everything goes well, the script should be able to produce a complete album that is at least interesting to listen to. Using some random parameters, I think it'd be cool if you could generate basically a entirely new album everytime you run the script. 

I haven't decided yet if I'll build the system with a central seed so as to be able to reproduce an album. 


## Audio Examples

So far the examples are very basic. This is mainly due to very rudimentary sound design and rythms. Here are some sound demos:

[Demo 1](https://github.com/cmdenis/Self-Making-Album/blob/main/audio_tests/demo_1.mp3)

[Demo 2](https://github.com/cmdenis/Self-Making-Album/blob/main/audio_tests/demo_2.mp3)

[Demo 3](https://github.com/cmdenis/Self-Making-Album/blob/main/audio_tests/demo_3.mp3)

[Demo 4](https://github.com/cmdenis/Self-Making-Album/blob/main/audio_tests/demo_4.mp3)

[Demo 5](https://github.com/cmdenis/Self-Making-Album/blob/main/audio_tests/demo_5.mp3)


