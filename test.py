import numpy as np
import matplotlib.pyplot as plt
import scipy as sci

x = np.linspace(0, 10, 100)
saw = sci.signal.sawtooth(x + np.pi)
sine = np.sin(x)

plt.plot(x, saw)
plt.plot(x, sine)
plt.show()

