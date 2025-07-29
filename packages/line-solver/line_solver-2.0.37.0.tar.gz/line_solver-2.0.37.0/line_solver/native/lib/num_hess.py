import numpy as np
from numpy import ndarray, dtype, float64

from line_solver.lib.num_grad import num_grad

def num_hess(func, X, h):
    H = np.zeros((len(X), len(X)))

    # for each dimension of objective function
    for i in range(len(X)):
        # derivative at first point (left)
        x1 = X.copy()
        x1[i] = X[i] - h
        df1 = num_grad(func, x1, h)

        # derivative at second point (right)
        x2 = X.copy()
        x2[i] = X[i] + h
        df2 = num_grad(func, x2, h)

        # differentiate between the two derivatives
        d2f = (df2 - df1) / (2 * h)

        # assign as row i of Hessian
        H[i, :] = d2f

    return H