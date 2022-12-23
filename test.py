import numpy as np
import matplotlib.pyplot as plt

samp_rate = 44100
time = 5
nb_samples = samp_rate*time
x = np.linspace(0, 10, nb_samples)
noise = np.random.rand(nb_samples)*2-1


noise_ft = np.fft.fft(noise)
noise_freq = np.fft.fftfreq(nb_samples, 1/samp_rate)

gauss_filt = np.exp(-noise_freq**2/10000**2)


noise_filt_ft = noise_ft*gauss_filt


noise_filt = np.fft.ifft(noise_filt_ft).imag


#plt.plot(noise)
#plt.title("Time Domain")
#plt.show()

plt.plot(noise_freq, np.abs(noise_ft))
plt.plot(noise_freq, np.abs(noise_filt_ft))
plt.title("Frequency domain")
plt.show()

plt.plot(noise_filt)
plt.title("Time Domain")
plt.show()

assert(0==1)

y = np.sin(x*10)

pulse = np.exp(-x/2)*(np.random.rand(len(x))-0.5)

conv = np.convolve(y, pulse, mode = "full")
conv2 = (np.fft.irfft(np.fft.rfft(y*pulse)))

plt.plot(pulse)
plt.plot(y)
plt.plot(conv)
plt.plot(conv2)
plt.show()