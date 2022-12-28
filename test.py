import numpy as np
import matplotlib.pyplot as plt
import scipy as sci

x = np.linspace(-1, 1, 100)

y = np.arctan(x*4)/(np.pi/2)

plt.plot(x, y)
plt.show()
