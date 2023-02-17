# Meta script that uses all other elements
from mixer import make_music
import numpy as np

# Let's make a couple of examples

for i in range(3):
    filename = "audio_tests/batches/output_"+str(i)
    print("-------------------------------")
    print("-------------------------------")
    print("-------------------------------")
    print("------- Making new song -------")
    print("-------------------------------")
    print("-------------------------------")
    print("-------------------------------")
    seed = np.random.randint(0, 100000000)
    make_music(seed, 44100, filename, mp3=False)