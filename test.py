import numpy as np
from scipy.io import wavfile

# Define the sampling rate in samples per second
sampling_rate = 44100

# Define the duration of the WAV file in seconds
duration = 5

# Define the frequency of the sine wave in hertz
freq = 440

# Define the time vector for the sine wave
time = np.arange(int(duration * sampling_rate)) / sampling_rate

# Generate a stereo sine wave with left and right channels
sine_wave_l = np.sin(2 * np.pi * freq * time)
sine_wave_r = 0.5 * np.sin(2 * np.pi * freq*2 * time + np.pi / 2)

# Stack the left and right channels into a stereo signal
stereo_signal = np.column_stack((sine_wave_l, sine_wave_r))

# Save the stereo signal as a WAV file
wavfile.write("stereo_signal.wav", sampling_rate, stereo_signal)