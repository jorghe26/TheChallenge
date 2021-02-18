def randomWalk(fuel_consumption):
    
    import random 
    import numpy as np 
    import matplotlib.pyplot as plt

    from itertools import cycle
    from mpl_toolkits.mplot3d import Axes3D
    dims = 1
    step_n = 10000
    step_set = [-1, 0, 1]
    origin = np.zeros((1,dims))

    # Simulate steps in 1D
    step_shape = (step_n,dims)
    steps = np.random.choice(a=step_set, size=step_shape)
    path = np.concatenate([origin + fuel_consumption, steps]).cumsum(0)

    return path

randomWalk(180)