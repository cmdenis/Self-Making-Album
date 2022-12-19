import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 10, 1000)
y = np.sin(x*10)

pulse = np.exp(-x/2)*(np.random.rand(len(x))-0.5)

conv = np.convolve(y, pulse, mode = "full")
conv2 = (np.fft.irfft(np.fft.rfft(y*pulse)))

plt.plot(pulse)
plt.plot(y)
plt.plot(conv)
plt.plot(conv2)
plt.show()