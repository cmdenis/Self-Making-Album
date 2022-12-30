import numpy as np
import matplotlib.pyplot as plt
import scipy as sci


x = sci.stats.truncnorm.rvs((20-35)/20, (20000-35)/20, size = 100000)*20 + 35
plt.hist(x)
plt.show()
