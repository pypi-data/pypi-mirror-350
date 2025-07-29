import warnings

import numpy as np
from numpy.linalg import det

from line_solver.api.line_warning import line_warning
from line_solver.api.mfilename import mfilename
from line_solver.lib.num_hess import num_hess

def laplaceapprox(h, x0):
    # I = laplaceapprox(f,x0)
    # approximates I=int f(x)dx by Laplace approximation at x0
    # example:  I = laplaceapprox(@(x) prod(x),[0.5,0.5])
    d = len(x0)

    tol = 1e-05
    H = num_hess(lambda x: np.log(h(x)), x0, tol)
    detnH = det(-H)

    if detnH < 0:
        tol = 0.0001
        H = num_hess(lambda x: np.log(h(x)), x0, tol)
        detnH = det(-H)

    if detnH < 0:
        tol = 0.001
        H = num_hess(lambda x: np.log(h(x)), x0, tol)
        detnH = det(-H)

    if detnH < 0:
        line_warning(mfilename(),'laplaceapprox: det(-H)<0')

    I = h(x0) * np.sqrt((2 * np.pi) ** d / detnH)
    logI = np.log(h(x0)) + (d / 2) * np.log(2 * np.pi) - np.log(detnH)

    return I, H, logI
