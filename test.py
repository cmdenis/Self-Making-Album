import numpy as np
a = [1, 2, 3, 4, 5, 6, 7]
a = np.append(0, np.delete(a, -1))


print(a)