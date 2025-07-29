from numpy import *
from line_solver.util import factln
def multinomialln(n = None):
    # MLN=MULTINOMIALLN(N)

    mln = factln(sum(n)) - sum(factln(n))
    return mln