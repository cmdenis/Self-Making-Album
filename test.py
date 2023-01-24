import numpy as np
a = np.array([1, 2, 3, 4])
b = np.array([4, 3, 2])

for i, j in zip(a, b):
    print(i, j)
