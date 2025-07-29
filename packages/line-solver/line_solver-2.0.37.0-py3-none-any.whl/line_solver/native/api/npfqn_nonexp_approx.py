import numpy as np
from line_solver import SchedStrategy, GlobalConstants


def npfqn_nonexp_approx(method, sn, ST, V, SCV, T, U, gamma, nservers):
    M = sn.nstations
    rho = np.zeros(M)
    scva = np.ones(M)
    scvs = np.ones(M)
    eta = np.ones(M)
    for ist in range(M):
        nnzClasses = np.isfinite(ST[ist]) & np.isfinite(SCV[ist])
        rho[ist] = np.sum(U[ist, nnzClasses])
        if np.any(nnzClasses):
            if np.all(sn.schedid[ist] == SchedStrategy.ID_FCFS):
                if np.ptp(ST[ist, nnzClasses]) > 0 or (
                        np.max(SCV[ist, nnzClasses]) > 1 + GlobalConstants.FineTol or np.min(
                        SCV[ist, nnzClasses]) < 1 - GlobalConstants.FineTol):
                    scva[ist] = 1
                    scvs[ist] = (SCV[ist, nnzClasses] * T[ist, nnzClasses].T) / np.sum(T[ist, nnzClasses])
                    gamma[ist] = (rho[ist] ** nservers[ist] + rho[ist]) / 2

                    if np.isclose(scvs[ist], 1, atol=1e-6) and nservers[ist] == 1:
                        eta[ist] = rho[ist]
                    else:
                        eta[ist] = np.exp(-2 * (1 - rho[ist]) / (scvs[ist] + scva[ist] * rho[ist]))

                    order = 8
                    ai = rho[ist] ** order
                    bi = rho[ist] ** order
                    for k in np.where(nnzClasses)[0]:
                        if sn.rates[ist, k] > 0:
                            ST[ist, k] = np.maximum(0, 1 - ai) * ST[ist, k] + ai * (
                                        bi * eta[ist] + np.maximum(0, 1 - bi) * gamma[ist]) * (
                                                     nservers[ist] / np.sum(T[ist, nnzClasses]))

                    nservers[ist] = 1

    return ST, gamma, nservers, rho, scva, scvs, eta