import numpy as np
a = np.outer(
    np.array([1, 2, 3]),
    np.outer(np.ones(3), np.arange(10))*12
)

print(a)