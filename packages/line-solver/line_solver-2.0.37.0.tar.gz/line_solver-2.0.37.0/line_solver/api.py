import jpype
import jpype.imports
import numpy as np
from jpype import JInt

from line_solver import jlineMatrixToArray, jlineMatrixFromArray

"""
Defines Python wrappers for JLINE methods.
Handles appropriate conversions between Java and Python data types.
"""
# Performs Mean Value Analysis (MVA) for cache models
def cache_mva(gamma, m):
    ret = jpype.JPackage('jline').api.CACHE.cache_mva(jlineMatrixFromArray(gamma), jlineMatrixFromArray(m))
    pi = jlineMatrixToArray(ret.pi)
    pi0 = jlineMatrixToArray(ret.pi0)
    pij = jlineMatrixToArray(ret.pij)
    x = jlineMatrixToArray(ret.x)
    u = jlineMatrixToArray(ret.u)
    E = jlineMatrixToArray(ret.E)
    return pi, pi0, pij, x, u, E

# Computes asymptotic probabilities for cache models
def cache_prob_asy(gamma, m):
    return jpype.JPackage('jline').api.CACHE.cache_prob_asy(jlineMatrixFromArray(gamma), jlineMatrixFromArray(m))

# Solves a CTMC using the uniformization method
def ctmc_uniformization(pi0, Q, t):
    return jlineMatrixToArray(
        jpype.JPackage('jline').api.CTMC.ctmc_uniformization(jlineMatrixFromArray(pi0), jlineMatrixFromArray(Q), t))

# Computes time-reversed CTMC for a given transition matrix
def ctmc_timereverse(matrix):
    return jlineMatrixToArray(jpype.JPackage('jline').api.CTMC.ctmc_timereverse(jlineMatrixFromArray(matrix)))

# Converts a transition probability matrix into an infinitesimal generator
def ctmc_makeinfgen(matrix):
    return jlineMatrixToArray(jpype.JPackage('jline').api.CTMC.ctmc_makeinfgen(jlineMatrixFromArray(matrix)))

# Solves steady-state probabilities for a CTMC
def ctmc_solve(matrix):
    return jlineMatrixToArray(jpype.JPackage('jline').api.CTMC.ctmc_solve(jlineMatrixFromArray(matrix)))

# Solves the steady-state probabilities for a DTMC
def dtmc_solve(matrix):
    return jlineMatrixToArray(jpype.JPackage('jline').api.DTMC.dtmc_solve(jlineMatrixFromArray(matrix)))

# Performs stochastic comparison of two DTMCs
def dtmc_stochcomp(matrix, indexes):
    ind = jpype.java.util.ArrayList()
    for i in range(len(indexes)):
        ind.add(JInt(indexes[i]))
    return jlineMatrixToArray(jpype.JPackage('jline').api.DTMC.dtmc_stochcomp(jlineMatrixFromArray(matrix), ind))

# Computes time-reversed DTMC for a given transition matrix
def dtmc_timereverse(matrix):
    return jlineMatrixToArray(jpype.JPackage('jline').api.DTMC.dtmc_timereverse(jlineMatrixFromArray(matrix)))

# Solves a closed queuing network using the Convolution Algorithm (CA)
def pfqn_ca(L, N, Z):
    pfqnNcReturn = jpype.JPackage('jline').api.PFQN.pfqn_ca(jlineMatrixFromArray(L), jlineMatrixFromArray(N),
                                                            jlineMatrixFromArray(Z))
    return pfqnNcReturn.G, pfqnNcReturn.lG

# Solves a closed queuing network using the Panacea algorithm
def pfqn_panacea(L, N, Z):
    pfqnNcReturn = jpype.JPackage('jline').api.PFQN.pfqn_panacea(jlineMatrixFromArray(L), jlineMatrixFromArray(N),
                                                            jlineMatrixFromArray(Z))
    return pfqnNcReturn.G, pfqnNcReturn.lG

# Solves a closed queueing network using the Bard-Schweitzer approximation
def pfqn_bs(N, L, Z):
    pfqnAMVAReturn = jpype.JPackage('jline').api.PFQN.pfqn_bs(jlineMatrixFromArray(L), jlineMatrixFromArray(N),
                                                            jlineMatrixFromArray(Z))
    XN = jlineMatrixToArray(pfqnAMVAReturn.X)
    QN = jlineMatrixToArray(pfqnAMVAReturn.Q)
    UN = jlineMatrixToArray(pfqnAMVAReturn.U)
    RN = jlineMatrixToArray(pfqnAMVAReturn.R)
    TN = jlineMatrixToArray(pfqnAMVAReturn.R)
    AN = jlineMatrixToArray(pfqnAMVAReturn.R)

    XN = XN[0]
    CN = np.zeros_like(XN)

    for r in range(len(XN)):
        CN[r] = N[r] / XN[r]

    for i in range(len(QN)):
        for r in range(len(XN)):
            TN[i,r] = XN[r] # since visits are not known, we assume a cyclic topology
            AN[i,r] = XN[r] # since visits are not known, we assume a cyclic topology

    return XN, CN, QN, UN, RN, TN, AN

# Solves a closed queueing network using Mean Value Analysis (MVA)
def pfqn_mva(N, L, Z):
    pfqnMVAReturn = jpype.JPackage('jline').api.PFQN.pfqn_mva(jlineMatrixFromArray(L), jlineMatrixFromArray(N),
                                                            jlineMatrixFromArray(Z))
    XN = jlineMatrixToArray(pfqnMVAReturn.X)
    QN = jlineMatrixToArray(pfqnMVAReturn.Q)
    UN = jlineMatrixToArray(pfqnMVAReturn.U)
    RN = jlineMatrixToArray(pfqnMVAReturn.R)
    TN = jlineMatrixToArray(pfqnMVAReturn.R)
    AN = jlineMatrixToArray(pfqnMVAReturn.R)

    XN = XN[0]
    CN = np.zeros_like(XN)

    for r in range(len(XN)):
        CN[r] = N[r] / XN[r]

    for i in range(len(QN)):
        for r in range(len(XN)):
            TN[i,r] = XN[r] # since visits are not known, we assume a cyclic topology
            AN[i,r] = XN[r] # since visits are not known, we assume a cyclic topology

    return XN, CN, QN, UN, RN, TN, AN

# Solves a closed queueing network using Approximate Queue Lengths (AQL)
def pfqn_aql(N, L, Z):
    pfqnAMVAReturn = jpype.JPackage('jline').api.PFQN.pfqn_aql(jlineMatrixFromArray(L), jlineMatrixFromArray(N),
                                                              jlineMatrixFromArray(Z))
    XN = jlineMatrixToArray(pfqnAMVAReturn.X)
    QN = jlineMatrixToArray(pfqnAMVAReturn.Q)
    UN = jlineMatrixToArray(pfqnAMVAReturn.U)
    RN = jlineMatrixToArray(pfqnAMVAReturn.R)
    TN = jlineMatrixToArray(pfqnAMVAReturn.R)
    AN = jlineMatrixToArray(pfqnAMVAReturn.R)

    XN = XN[0]
    CN = np.zeros_like(XN)

    for r in range(len(XN)):
        CN[r] = N[r] / XN[r]

    for i in range(len(QN)):
        for r in range(len(XN)):
            TN[i,r] = XN[r] # since visits are not known, we assume a cyclic topology
            AN[i,r] = XN[r] # since visits are not known, we assume a cyclic topology

    return XN, CN, QN, UN, RN, TN, AN

# Added a wrapper for the map_pie method
# Computes the steady-state probabilities of the embedded MC in a given MAP
def map_pie(D0, D1=None):

    # D0 is an array of MatrixCells
    if isinstance(D0, (list, np.ndarray)) and all(isinstance(item, jpype.JPackage('jline').util.MatrixCell) for item in D0):
        java_result = jpype.JPackage('jline').api.MAM.map_pie(D0[0])
    # D0 is a single MatrixCell
    elif isinstance(D0, jpype.JPackage('jline').util.MatrixCell):
        if D1 is None:
            java_result = jpype.JPackage('jline').api.MAM.map_pie(D0)
        else:
            raise ValueError("D1 should not be provided when D0 is already a MatrixCell.")
    # D0 is an array
    else:
        if not isinstance(D0, np.ndarray):
            D0 = np.array(D0)

        if D1 is None:
            # Assume D0 is a MatrixCell containing both D0 and D1
            java_D0 = jlineMatrixFromArray(D0[0])
            java_D1 = jlineMatrixFromArray(D0[1])
            matrix_cell = jpype.JPackage('jline').util.MatrixCell(java_D0, java_D1)
            java_result = jpype.JPackage('jline').api.MAM.map_pie(matrix_cell)
        else:
            # Ensure D1 is a numpy array
            if not isinstance(D1, np.ndarray):
                D1 = np.array(D1)
            java_D0 = jlineMatrixFromArray(D0)
            java_D1 = jlineMatrixFromArray(D1)
            java_result = jpype.JPackage('jline').api.MAM.map_pie(java_D0, java_D1)

    return jlineMatrixToArray(java_result)

# Added a wrapper for the npfqn_nonexp_approx method
# Computes a non-exponential approx. for the service time distribution in non-product form queueing networks
def npfqn_nonexp_approx(method, sn, ST, V, SCV, Tin, Uin, gamma, nservers):

    # method: default, none, hmva, interp

    java_method = jpype.JString(method)
    java_sn = sn.obj
    java_ST = jlineMatrixFromArray(ST)
    java_V = jlineMatrixFromArray(V)
    java_SCV = jlineMatrixFromArray(SCV)
    java_Tin = jlineMatrixFromArray(Tin)
    java_Uin = jlineMatrixFromArray(Uin)
    java_gamma = jlineMatrixFromArray(gamma)
    java_nservers = jlineMatrixFromArray(nservers)

    result = jpype.JPackage('jline').api.NPFQN.npfqn_nonexp_approx(
        java_method, java_sn, java_ST, java_V, java_SCV, java_Tin, java_Uin, java_gamma, java_nservers
    )

    python_result = [
        jlineMatrixToArray(result.ST),
        jlineMatrixToArray(result.gamma),
        jlineMatrixToArray(result.nservers),
        jlineMatrixToArray(result.rho),
        jlineMatrixToArray(result.scva),
        jlineMatrixToArray(result.scvs),
        jlineMatrixToArray(result.eta),
    ]

    return python_result

# Added a wrapper for the map_mean method
# Computes the mean inter-arrival time of a MAP
def map_mean(D0, D1=None):

    # D0 is an array of MatrixCells
    if isinstance(D0, (list, np.ndarray)) and all(isinstance(item, jpype.JPackage('jline').util.MatrixCell) for item in D0):
        java_D0 = D0[0].get(0)
        java_D1 = D0[1].get(0)

    # D0 is a single MatrixCell
    elif isinstance(D0, jpype.JPackage('jline').util.MatrixCell):
        if D1 is None:
            return jpype.JPackage('jline').api.MAM.map_mean(D0)
        else:
            raise ValueError("D1 should not be provided when D0 is already a MatrixCell.")

    else:
        # Ensure D0 is a numpy array
        if not isinstance(D0, np.ndarray):
            D0 = np.array(D0)

        if D1 is None:
            # Assume D0 is a container with both D0 and D1
            java_D0 = jlineMatrixFromArray(D0[0])
            java_D1 = jlineMatrixFromArray(D0[1])
        else:
            # Ensure D1 is a numpy array
            if not isinstance(D1, np.ndarray):
                D1 = np.array(D1)
            java_D0 = jlineMatrixFromArray(D0)
            java_D1 = jlineMatrixFromArray(D1)

    mean = jpype.JPackage('jline').api.MAM.map_mean(java_D0, java_D1)

    return mean

