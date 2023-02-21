import numpy as np
inc = 2.1
final = 5
a = np.diff(np.append(np.arange(0, final, inc), final))

print(a)