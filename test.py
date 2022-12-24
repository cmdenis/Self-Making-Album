import numpy as np
import matplotlib.pyplot as plt
import scipy as sci

release_time = 1
time = 1
sr = 100
sr2 = 10
nb_samples = time*sr
samples = np.zeros(time*sr)
x = np.arange(time*sr)
signal = np.sin(2*np.pi*x/20)


new_smp = np.linspace(0, 10, time*sr2)

data = np.interp(new_smp, x, signal)

plt.plot(x, signal)
plt.plot(new_smp, data)
plt.show()