import random
import numpy as np


def randomWalk(fuel_consumption, steps):

    dims = 1
    step_n = steps
    step_set = [-1, 0, 1]
    origin = np.zeros((1, dims))

    # Simulate steps in 1D
    step_shape = (step_n, dims)
    steps = np.random.choice(a=step_set, size=step_shape)
    path = np.concatenate([origin + fuel_consumption, steps]).cumsum(0)

    new_path=[]
    for p in path:
        new_path.append(p[0])

    return new_path
