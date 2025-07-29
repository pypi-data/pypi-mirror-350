import numpy as np

from line_solver import SchedStrategy, GlobalConstants, map_mean
from native.solvers.fluid.solver_fluid import solver_fluid


def solver_fluid_closing(sn, schedid, options):

    M = sn.nstations
    K = sn.nclasses
    refstat = sn.refstat
    Lambda = sn.mu
    phi = sn.phi
    phases = sn.phases

    # Run initial fluid solver
    # modifies sn.nservers ??
    Q, xvec_it, QNt, UNt, xvec_t, t, iters, runtime = solver_fluid(sn, schedid, options)

    chains = sn.chains

    # Assumes the existence of a delay node through which all classes pass
    delayNodes = np.zeros(M)
    delayrefstat = np.zeros(M)

    # Identify delay nodes
    for i in range(M):
        if schedid[i] == SchedStrategy.INF: # INF
            delayNodes[i] = 1

    # Identify reference stations
    for k in range(K):
        refstat_id = int(refstat[k]) # convert from list to int
        if refstat_id >= 0:
            delayrefstat[refstat_id] = 1

    # Qlength for all stations, classes,
    QN = xvec_it[-1]

    # Tput for all classes in each station
    Rlittle = np.zeros((M, K))
    TN = np.zeros((M, K))
    TNt = [[0 for _ in range(K)] for _ in range(M)]

    Xservice = [[np.zeros(int(phases[i, k])) for k in range(K)] for i in range(M)]

    # Compute throughputs per class (TN) and per class-phase (Xservice)
    for i in range(M):
        if delayNodes[i] == 1:
            for k in range(K): # class
                idx = int(np.sum(phases[:i,:]) + np.sum(phases[i,:k]))
                for f in range(int(phases[i, k])): # phase
                    TN[i, k] += QN[idx + f] * Lambda[i][k][f] * phi[i][k][f] # sum of the service rates across all phases
                    TNt[i][k] += QNt[i][k] * Lambda[i][k][f] * phi[i][k][f]
                    Xservice[i][k][f] = QN[idx + f] * Lambda[i][k][f]
        # For non-delay nodes
        else:
            xi = np.sum(Q[i, :])
            xi_t = sum(QNt[i])

            # If queue length non-empty or subject to external arrivals
            if xi > 0 or schedid[i] == SchedStrategy.EXT: # EXT
                if schedid[i] == SchedStrategy.FCFS: # FCFS
                    wni = GlobalConstants.CoarseTol # store queue lengths for current class
                    wi = np.zeros(K)  # store weights for each class

                    for k in range(K):
                        # Compute the index for the current class and station
                        idx = int(np.sum(phases[:i, :]) + np.sum(phases[i, :k]))
                        # Compute the mean of the MAP process for the current class
                        wi[k] = map_mean(sn.proc[i][k])
                        # Update wni with the weighted sum of queue lengths for the current class
                        wni += wi[k] * np.sum(QN[idx:idx + int(phases[i, k])])

                    wni_t = np.zeros_like(QNt[i][0])
                    for r in range(K):
                        # Update wni_t with the weighted sum of QNt for each class
                        wni_t += wi[r] * QNt[i][r]

                # Added from MATLAB (lines 81-134)
                for k in range(K):  # Iterate over all classes
                    idx = int(np.sum(phases[:i, :]) + np.sum(phases[i, :k]))
                    Xservice[i][k] = np.zeros(int(phases[i, k]))

                    for f in range(int(phases[i, k])):  # Iterate over all phases
                        if schedid[i] == SchedStrategy.EXT: # EXT
                            if f == 0:
                                TN[i, k] += (1 - np.sum(QN[idx + 1:idx + phases[i, k]])) * Lambda[i][k][f] * phi[i][k][f]
                                TNt[i][k] += (1 - np.sum(xvec_t[:, idx + 1:idx + phases[i, k]], axis=1)) * Lambda[i][k][f] * phi[i][k][f]
                                Xservice[i][k][f] = (1 - np.sum(QN[idx + 1:idx + phases[i, k]])) * Lambda[i][k][f]
                            else:
                                TN[i, k] += QN[idx + f] * Lambda[i][k][f] * phi[i][k][f]
                                TNt[i][k] += xvec_t[:, idx + f] * Lambda[i][k][f] * phi[i][k][f]
                                Xservice[i][k][f] = QN[idx + f] * Lambda[i][k][f]

                        elif schedid[i] == SchedStrategy.INF or schedid[i] == SchedStrategy.PS: # INF, PS
                            TN[i, k] += QN[idx + f] * Lambda[i][k][f] * phi[i][k][f] / xi * min(xi, sn.nservers[i])
                            # NOTE: fails if xi_t is 0
                            # TNt[i][k] += xvec_t[:, idx + f] * Lambda[i][k][f] * phi[i][k][f] / xi_t * np.minimum(xi_t, S[i])
                            # so add a condition to avoid division by zero
                            if all(xi_t) > 0:
                                TNt[i][k] += xvec_t[:, idx + f] * Lambda[i][k][f] * phi[i][k][f] / xi_t * np.minimum(xi_t, sn.nservers[i])
                            else:
                                TNt[i][k] += 0  # No throughput contribution when xi_t is zero
                            Xservice[i][k][f] = QN[idx + f] * Lambda[i][k][f] / xi * min(xi, sn.nservers[i])

                        elif schedid[i] == SchedStrategy.DPS: # DPS
                            w = sn.schedparam[i, :]
                            wxi = np.dot(w, Q[i, :])  # Weighted number of jobs in the station
                            wxi_t = w[0] * QNt[i][0]
                            for r in range(1, len(QNt[i])):
                                wxi_t += w[r] * QNt[i][r]
                            TN[i, k] += QN[idx + f] * Lambda[i][k][f] * phi[i][k][f] * w[k] / wxi * min(xi, sn.nservers[i])
                            #TNt[i][k] += xvec_t[:, idx + f] * Lambda[i][k][f] * phi[i][k][f] * w[k] / wxi_t * np.minimum(xi_t, S[i])
                            # added condition to avoid division by zero
                            if all(xi_t) > 0:
                                TNt[i][k] += xvec_t[:, idx + f] * Lambda[i][k][f] * phi[i][k][f] / xi_t * np.minimum(xi_t, sn.nservers[i])
                            else:
                                TNt[i][k] += 0  # No throughput contribution when xi_t is zero
                            Xservice[i][k][f] = QN[idx + f] * Lambda[i][k][f] * w[k] / wxi * min(xi, sn.nservers[i])

                        elif schedid[i] == SchedStrategy.FCFS or sched[i] == SchedStrategy.SIRO: # FCFS, SIRO
                            if options['method'] in ['default', 'closing']:
                                TN[i, k] += QN[idx + f] * Lambda[i][k][f] * phi[i][k][f] / xi * min(xi, sn.nservers[i])
                                #TNt[i][k] += xvec_t[:, idx + f] * Lambda[i][k][f] * phi[i][k][f] / xi_t * np.minimum(xi_t, S[i])
                                # added condition to avoid division by zero
                                if all(xi_t) > 0:
                                    TNt[i][k] += xvec_t[:, idx + f] * Lambda[i][k][f] * phi[i][k][f] / xi_t * np.minimum(xi_t, sn.nservers[i])
                                else:
                                    TNt[i][k] += 0  # No throughput contribution when xi_t is zero
                                Xservice[i][k][f] = QN[idx + f] * Lambda[i][k][f] / xi * min(xi, sn.nservers[i])
                            elif options['method'] == 'statedep':
                                TN[i, k] += QN[idx + f] * Lambda[i][k][f] * phi[i][k][f] * wi[k] / wni * min(xi, sn.nservers[i])
                                #TNt[i][k] += xvec_t[:, idx + f] * Lambda[i][k][f] * phi[i][k][f] / xi_t * np.minimum(xi_t, S[i])
                                # added condition to avoid division by zero
                                if all(xi_t) > 0:
                                    TNt[i][k] += xvec_t[:, idx + f] * Lambda[i][k][f] * phi[i][k][f] / xi_t * np.minimum(xi_t, sn.nservers[i])
                                else:
                                    TNt[i][k] += 0  # No throughput contribution when xi_t is zero
                                Xservice[i][k][f] = QN[idx + f] * Lambda[i][k][f] * wi[k] / wni * min(xi, sn.nservers[i])
                        else:
                            raise ValueError(f"Unsupported scheduling policy: {schedid[i]}")


    # Fill TNt with ones where TNt is single valued
    for i in range(len(TNt)):
        for j in range(len(TNt[0])):
            if np.isscalar(TNt[i][j]):
                TNt[i][j] = np.ones(len(xvec_t[:, 0])) * TNt[i][j]

    # Response times
    origK = chains.shape[0]
    R = np.zeros((M, K))

    for i in range(M):
        mask = TN[i, :] > 0  # mask for elements where TN > 0
        R[i, mask] = Q[i, mask] / TN[i, mask]  # Compute response times for valid elements

    newR = np.zeros((M, origK))
    X = np.zeros(origK)
    newQ = np.zeros((M, origK))

    #determine eventual probability of visiting each station in each class (expected number of visits)
    #weight response time of each original class with the expected number of
    #visits to each station in each associated artificial class
    idxNR = np.arange(0, M * K).reshape((K, M), order='F')
    idxNR = idxNR[:, delayrefstat == 0].ravel(order='F')
    rtTrans = sn.rt[np.ix_(idxNR, idxNR)] # transient transition matrix for non-reference nodes
    eventualVisit = np.linalg.inv(np.eye(len(rtTrans)) - rtTrans) # pseudo-inverse instead of inverse?
    idxOrigClasses = np.zeros(origK, dtype=int)

    for k in range(origK):
        idxOrigClasses[k] = np.argmax(chains[k])
        refNode = refstat[idxOrigClasses[k]]
        refNode = int(refNode)

        eventualVisitProb = (sn.rt[refNode * K + k, idxNR] @ eventualVisit).reshape(M - sum(delayrefstat > 0), K).T

        # Handle the case where there is only one chain and class
        if chains.shape == (1, 1):
            if chains[k, 0] == 1:
                eventualVisitProb = eventualVisitProb
            else:
                eventualVisitProb = np.zeros_like(eventualVisitProb)  # set to zero
        else:
            # General case for larger chains
            eventualVisitProb = eventualVisitProb[:, chains[k, :] == 1]

        newR[refNode, k] = np.sum(R[refNode, chains[k] == 1]) # update newR for the reference node
        newR[delayrefstat == 0, k] = np.sum(R[delayrefstat == 0, :][:, chains[k] == 1] * eventualVisitProb, axis=1) # update newR for the non-reference nodes
        # update newR for the reference node and chain
        newR[refNode, chains[k] == 1] = R[refNode, chains[k] == 1]
        newR[delayrefstat == 0, chains[k] == 1] = R[delayrefstat == 0, chains[k] == 1] * eventualVisitProb

        X[k] = np.sum(TN[refNode, chains[k] == 1])
        newQ[:, k] = np.sum(Q[:, chains[k] == 1], axis=1)

    QN = Q
    RN = R

    # Utilization
    UN = np.zeros((M, K))
    for i in range(M):
        for k in range(K):
            idx = Xservice[i][k] > 0
            UN[i, k] = np.sum(Xservice[i][k][idx] / np.array(Lambda[i][k])[idx])
            if schedid[i] == SchedStrategy.FCFS and options['method'] == 'statedep': # FCFS
                TN[i, k] = np.sum(Xservice[i][k][idx])


    sn.nservers = sn.nservers.flatten()

    UN[delayNodes == 0, :] /= sn.nservers[delayNodes == 0][:, None]

    return QN, UN, RN, TN, xvec_it, QNt, UNt, TNt, xvec_t, t, iters, runtime
