import numpy as np
import time
from line_solver import *
from line_solver.constants import *
from line_solver import jlineMatrixToArray, Coxian

from line_solver.native.api.npfqn_nonexp_approx import npfqn_nonexp_approx
from line_solver.native.solvers.fluid.solver_fluid_closing import solver_fluid_closing
from line_solver.native.solvers.fluid.solver_fluid_initsol import solver_fluid_initsol


def solver_fluid_analyzer(sn, options):
    M = sn.nstations # number of stations
    K = sn.nclasses # number of classes
    S = sn.nservers # number of servers
    SCV = sn.scv # coef of variation
    V = np.sum(list(sn.visits.values()), axis=0) # total visits across all stations and classes ?
    gamma = np.zeros(M)
    sched = sn.sched # scheduling policies
    phases = sn.phases.copy() # phases
    phases_last = sn.phases.copy()
    rates0 = sn.rates # service rates

    solver_type = options.get('type', None) # provisionally to test analysis with/without iterative refinement on FCFS queues
    solver_method = options.get('method', None)

    # Convert scheduling policies from string to Python enum
    schedid = [None] * M
    for i in range(M):
        schedid[i] = SchedStrategy.fromString(sched[i])

    """
    for i in range(M):
        java_schedi = SchedStrategy.fromLINEString(sched[i]) # From string to SchedStrategy Java object
        schedid[i] = SchedStrategy.toID(java_schedi) # From SchedStrategy Java to ID as int
    """

    if options.get('init_sol') is None:
        options['init_sol'] = solver_fluid_initsol(sn, options)


    outer_iters = 1
    outer_runtime = time.time()
    """
    NOTE: The matrix method has not been re-implemented. Instead, it may be called from JLINE directly in line_solver.
    if options["method"] in ['matrix', 'fluid.matrix', 'default']:
        QN, UN, RN, TN, xvec_iter, QNt, UNt, TNt, _, t = solver_fluid_matrix(sn, options)

    NOTE: The statedep method has not been re-implemented. Instead, it may be called from JLINE directly in line_solver.
    """
    if solver_method in ['softmin', 'default']:
        QN, UN, RN, TN, xvec_iter, QNt, UNt, TNt, _, t, _, _ = solver_fluid_closing(sn, schedid, options)
    else:
        print(f"The '{options['method']}' method is unsupported by this solver.")

    outer_runtime = time.time() - outer_runtime

    # if options["method"] in ['closing', 'default', 'softmin']:
    if solver_type == 'closing':
        # ODEs support only PS, INF (delay) and single-class FCFS queues
        # The state vector of ODEs track the aggregate number of jobs in a queue.
        # In FCFS queues, we require to track the position of individual jobs in the queue.
        # Hence, we need to update the service times.
        if schedid == SchedStrategy.FCFS: # FCFS
            iter = 0
            eta_1 = np.zeros(M)
            eta = np.inf * np.ones(M)
            tol = GlobalConstants.CoarseTol

            # Fixed-point iteration for service time estimates
            # any or all
            while np.max((np.abs(1 - eta / eta_1))) > tol and iter <= options["iter_max"]:
                iter += 1
                eta_1 = eta
                for ist in range(M):
                    sd = rates0[ist, :] > 0
                    UN[ist, sd] = TN[ist, sd] / rates0[ist, sd]
                ST0 = 1 / rates0
                ST0[np.isinf(ST0)] = GlobalConstants.Immediate
                ST0[np.isnan(ST0)] = GlobalConstants.FineTol

                XN = np.zeros(K)
                for k in range(K):
                    if sn.refstat[k] > 0:
                        XN[k] = TN[sn.refstat[k], k]

                ST, gamma, _, _, _, _, eta = npfqn_nonexp_approx(options.get("config"), sn, ST0, V, SCV, TN, UN, gamma, S) # NOTE: non-exp approximation required for multi-class FCFS queues due to class interference
                rates = 1 / ST # update to effective service rates
                rates[np.isinf(rates)] = GlobalConstants.Immediate
                rates[np.isnan(rates)] = GlobalConstants.FineTol

                for ist in range(M):
                    if schedid == SchedStrategy.FCFS: # FCFS
                        for k in range(K):
                            if rates[ist, k] > 0 and SCV[ist, k] > 0:
                                # fit Coxian distribution to match new rates and SCV
                                # NOTE: Temporarily replaced with Coxian fit instead of Cox2
                                # returns a cox2 object
                                cx = Coxian.fitMeanAndSCV(1 / rates[ist, k], SCV[ist, k]) # NOTE: closing and state-dep methods don't work with general PH, only Coxian.
                                muik = jlineMatrixToArray(Coxian.getMu(cx))
                                phiik = jlineMatrixToArray(Coxian.getPhi(cx))
                                phases[ist, k] = len(muik) # new number of phases
                                if phases[ist, k] != phases_last[ist, k]:
                                    isf = sn.stationToStateful(ist)
                                    _, nir, sir = State.toMarginal(sn, ist, sn.state[isf], options) # obtain node-level marginal statistics

                                # Update the network state
                                sn.proc[ist][k] = cx.obj.getProcess()
                                sn.mu[ist][k] = muik
                                sn.phi[ist][k] = phiik
                                sn.phases = phases
                                sn.phasessz = np.maximum(sn.phases, np.ones_like(sn.phases))
                                sn.phaseshift = np.hstack([np.zeros((phases.shape[0], 1)), np.cumsum(sn.phasessz, axis=1)])
                                if phases[ist, k] != phases_last[ist, k]:
                                    isf = sn.stationToStateful(ist)
                                    sn.state[isf] = State.fromMarginalAndStarted(sn, ist, nir, sir, options)
                                    sn.state[isf] = sn.state[isf][0, :]

                    # Access the last state vector
                    options['init_sol'] = xvec_iter[-1]

                    # Recompute the fluid initial solution if there are changes in phases
                    if np.any(phases_last - phases != 0):
                        print("Recomputing fluid initial solution due to phase changes...")
                        options['init_sol'] = solver_fluid_initsol(sn)

                sn.phases = phases

                """
                if options["method"] == 'matrix':
                    _, UN, _, TN, xvec_iter, _, _, _, _, _, inner_iters, inner_runtime = solver_fluid_matrix(sn, options)
                """
                print("Running solver with updated service times...")
                QN, UN, RN, TN, xvec_iter, QNt, UNt, TNt, _, t, inner_iters, inner_runtime = solver_fluid_closing(sn, options)

                phases_last = phases
                outer_iters += inner_iters
                outer_runtime += inner_runtime

            # Compute the true initial point when the service times have converged
            print("Re-computing the true initial point after convergence in service times...")
            options['init_sol'] = solver_fluid_initsol(sn, options)

            # Run solver from the true initial point
            """
            if options["method"] == 'matrix':
                QN, UN, RN, TN, xvec_iter, QNt, UNt, TNt, _, t = solver_fluid_matrix(sn, options)
            """
            print("Running solver from the true initial point...")
            QN, UN, RN, TN, xvec_iter, QNt, UNt, TNt, _, t, inner_iters, inner_runtime = solver_fluid_closing(sn, options)

    if t[0] == 0:
        t[0] = GlobalConstants.FineTol

    for ist in range(M):
        for k in range(K):
            pass

    Ufull0 = UN.copy()
    for ist in range(M):
        sd = np.where(QN[ist, :] > 0)[0]
        UN[ist, QN[ist, :] == 0] = 0
        if schedid == SchedStrategy.INF: # INF
            for k in sd:
                UN[ist, k] = QN[ist, k]
                UNt[ist][k] = QNt[ist][k]
                TNt[ist][k] = UNt[ist][k] * sn.rates[ist, k]
        elif schedid == SchedStrategy.DPS: # DPS
            for k in sd:
                UN[ist, k] = min([1, QN[ist, k] / S[ist], sum(Ufull0[ist, sd]) * (TN[ist, k] / rates0[ist, k]) / sum(TN[ist, sd] / rates0[ist, sd])])
                TNt[ist][k] = UNt[ist][k] * sn.rates[ist, k] * S[ist]
        else:
            for k in sd:
                UN[ist, k] = min([1, QN[ist, k] / S[ist], sum(Ufull0[ist, sd]) * (TN[ist, k] / rates0[ist, k]) / sum(TN[ist, sd] / rates0[ist, sd])])
                TNt[ist][k] = UNt[ist][k] * sn.rates[ist, k] * S[ist]

    UN[np.isnan(UN)] = 0

    for ist in range(M):
        sd = np.where(QN[ist, :] > 0)[0]
        RN[ist, QN[ist, :] == 0] = 0
        for k in sd:
            if schedid != SchedStrategy.INF: # not INF
                RN[ist, k] = QN[ist, k] / TN[ist, k]

    RN[np.isnan(RN)] = 0

    XN = np.zeros(K)
    CN = np.zeros(K)
    for k in range(K):
        if sn.refstat[k] > 0:
            XN[k] = TN[sn.refstat[k], k]
            CN[k] = sn.njobs[k] / XN[k]

    """
    xvec = {
        "odeStateVec": xvec_iter[-1], # last state vector
        "sn": sn # network structure
    }
    """
    iter = outer_iters
    return QN, UN, RN, TN, CN, XN, t, QNt, UNt, TNt, xvec_iter, iter
