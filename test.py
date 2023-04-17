import numpy as np
x = np.array([[4, 3], [2, 2]])
print(x)
print(np.argsort(x, axis=0) )
print(np.argsort(x, axis=1) )
print(np.argsort(x) )