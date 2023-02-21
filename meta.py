# Meta script that uses all other elements
from mixer import make_music
import numpy as np

# Let's make a couple of examples

n = 10

for i in range(20):
    filename = "audio_tests/batches/output_"+str(i)
    print("\n\n-------------------------------")
    print("-------------------------------")
    print("-------------------------------")
    print("------- Making new song -------")
    print("-------------------------------")
    print("-------------------------------")
    print("-------------------------------\n")
    seed = np.random.randint(0, 100000000)
    make_music(seed, 44100, filename, mp3=False)