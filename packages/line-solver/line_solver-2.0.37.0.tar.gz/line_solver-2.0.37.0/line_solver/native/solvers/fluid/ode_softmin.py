from line_solver.api import map_pie
from line_solver.constants import SchedStrategy, GlobalConstants
import numpy as np


# Constructs the fluid ODE system for a queuing network using the softmin approximation.
def ode_softmin(x, Phi, Mu, PH, M, K, enabled, q_indices, rt, Kic, nservers, w, schedid, alpha):

    x = x.flatten() # flatten the state vector
    #print('x:')
    #print(x)

    # derivative of the state vector
    # rate of chasge in the number of jobs in each phase at each station
    dx = 0 * x

    # instead of using the weight matrix passed as argument, we initialise it here with the appropriate structure station-class-phase
    w = [[np.zeros(Kic[i][c]) if Kic[i][c] > 0 else [] for c in range(K)] for i in range(M)]

    # iterate over all stations
    for i in range(M):
        # the behaviour of the ODE depends on the scheduling policy at each station (transition rates are scaled appropriately)

        if schedid[i] == SchedStrategy.INF: # SchedStrategy.INF
            # jobs change phases within the same station
            for c in range(K):
                if enabled[i][c]:
                    xic = q_indices[i][c] # first index of station-class pair in state vector
                    # iterate over phases
                    for kic in range(Kic[i][c]):
                        for kic_p in range(Kic[i][c]):
                            if kic != kic_p:
                                rate = PH[i][c][0][kic][kic_p]
                                dx[xic+kic] -= x[xic+kic] * rate # jobs currently in this phase leave at rate given by the PH
                                dx[xic+kic_p] += x[xic+kic] * rate # jobs in the previous phase enter the current phase at rate given by PH

            # jobs complete service and are routed to other stations
            for c in range(K):
                if enabled[i][c]:
                    xic = q_indices[i][c]
                    for j in range(M):
                        for l in range(K):
                            xjl = q_indices[j][l] # first index of destination station-class pair in state vector
                            if enabled[j][l]:
                                pie = map_pie(PH[j][l]) # steady-state probabilities for phases
                                if rt[(i*K)+c][(j*K)+l] > 0:
                                    for kic in range(Kic[i][c]): # phases of job class c at station i
                                        for kjl in range(Kic[j][l]): # phases of job class l at station j
                                            if j != i: # exclude self routing
                                                # (probability of a job of class c being at station i in phase kic) x (routing probability of being directed to station j under class l) x (steady state probability of entering destination phase)
                                                rate = Phi[i][c][kic] * Mu[i][c][kic] * rt[(i*K)+c][(j*K)+l] * (pie[kjl] if isinstance(pie, list) else pie)
                                                rate = float(rate[0, 0]) # ensure rate is a float
                                                dx[xic+kic] -= x[xic+kic] * rate # outflow of jobs from source
                                                dx[xjl+kjl] += x[xic+kic] * rate # inflow of jobs to destination


        # open models (with external arrivals) not supported
        elif schedid[i] == SchedStrategy.EXT: # SchedStrategy.EXT:
            raise ValueError('State dependent ODE method does not support open models. Try with default method.')

        # PS
        # Jobs are served simultaneously with service rates shared equally among all jobs
        elif schedid[i] == SchedStrategy.PS: # SchedStrategy.PS
            # index range for station i in the state vector
            idxIni = q_indices[i][0]
            idxEnd = q_indices[i][K-1] + Kic[i][K-1] - 1

            # total number of jobs at station i (sum across all phases and classes)
            ni = sum(x[idxIni:idxEnd + 1])

            # phase changes
            for c in range(K):
                if enabled[i][c]:
                    xic = q_indices[i][c]
                    for kic in range(Kic[i][c]): # current phase
                        for kic_p in range(Kic[i][c]): # destination phase
                            if kic != kic_p:
                                rate = PH[i][c][0][kic][kic_p] # transition rate from phase kic to phase kic_p
                                if ni > nservers[i]: # if number of jobs exceeds number of servers
                                    rate *= nservers[i] / ni # scale the phase transition rate
                                dx[xic+kic] -= x[xic+kic] * rate # outflow from current phase
                                dx[xic+kic_p] += x[xic+kic] * rate # inflow to destination phase

            # service completions
            for c in range(K): # current class
                if enabled[i][c]:
                    xic = q_indices[i][c]
                    for j in range(M): # destination station
                        for l in range(K): # destination class
                            xjl = q_indices[j][l]
                            if enabled[j][l]:
                                pie = map_pie(PH[j][l]) # equilibrium distribution over phases at time of completion
                                if rt[(i*K)+c][(j*K)+l] > 0:

                                    # iterate over phases
                                    for kic in range(Kic[i][c]): # current phase
                                        for kjl in range(Kic[j][l]): # destination phase
                                            # phase transition
                                            rate = Phi[i][c][kic] * Mu[i][c][kic] * rt[(i*K)+c][(j*K)+l] * (pie[kjl] if isinstance(pie, list) else pie)
                                            if ni > nservers[i]:
                                                rate *= nservers[i] / ni # scale service rate
                                            dx[xic+kic] -= x[xic+kic] * rate # outlfow from current station
                                            dx[xjl+kjl] += x[xic+kic] * rate # inflow to destination station

        # FCFS
        # Jobs are served in the order they arrive to the station
        elif schedid[i] == SchedStrategy.FCFS: # SchedStrategy.FCFS
            # index range for the current station in the state vector
            idxIni = q_indices[i][0]
            idxEnd = q_indices[i][K-1] + Kic[i][K-1] - 1

            # total number of jobs at station i (across all classes and phases)
            ni = sum(x[idxIni:idxEnd+1]) # add + 1 to include idxEnd but gives a greater discrepancy ?

            # total number of jobs weighted by their phase
            wni = GlobalConstants.CoarseTol

            for c in range(K): # classes
                for kic in range(Kic[i][c]): # phases
                    if enabled[i][c]:
                        xic = q_indices[i][c]
                        if PH[i][c][0][kic][kic] != 0:
                            w[i][c][kic] = -1 / PH[i][c][0][kic][kic] # weight for phase kic derived from diagonal of phase type distribution (total rate at which jobs leave each phase)
                        else:
                            w[i][c][kic] = 0  # Set weight to 0 for disabled phases
                        wni += w[i][c][kic] * x[xic + kic] # phase weight x number of jobs in this phase

            # phase changes
            # jobs transition between different phases at the same station
            for c in range(K): # current class
                if enabled[i][c]:
                    xic = q_indices[i][c]
                    for kic in range(Kic[i][c]): # current phase
                        for kic_p in range(Kic[i][c]): # destination phase
                            if kic != kic_p:
                                rate = PH[i][c][0][kic][kic_p] # transition rate given by PH
                                rate *= softmin(ni, nservers[i], alpha) * w[i][c][kic] / wni # rate scaled by min(num jobs, num servers) and weight for curent phase relative to the total weighted jobs
                                dx[xic+kic] -= x[xic+kic] * rate # outflow from current phase
                                dx[xic+kic_p] += x[xic+kic] * rate # inflow to destination phase

            # service completions
            # jobs complete service at current station and transition to the next station
            for c in range(K): # current class
                if enabled[i][c]:
                    xic = q_indices[i][c]
                    for j in range(M): # destination station
                        for l in range(K): # destination class
                            xjl = q_indices[j][l]
                            if enabled[j][l]:
                                pie = map_pie(PH[j][l]) # equilibrium distribution over phases at time of completion
                                if rt[(i*K)+c][(j*K)+l] > 0:
                                    for kic in range(Kic[i][c]): # current phase
                                        for kjl in range(Kic[j][l]): # destination phase
                                            # transition rate = prob of being in current phase kic x prob of completing service x prob of routing x prob of entering phase kjl at destination
                                            rate = Phi[i][c][kic] * Mu[i][c][kic] * rt[(i*K)+c][(j*K)+l] * (pie[kjl] if isinstance(pie, list) else pie)
                                            rate *= softmin(ni, nservers[i], alpha) * w[i][c][kic] / wni # scale the rate
                                            dx[xic+kic] -= x[xic+kic] * rate
                                            dx[xjl+kjl] += x[xic+kic] * rate

        # DPS
        # Jobs are served simulatenously with service rates weighted based on the job classes
        elif schedid[i] == SchedStrategy.DPS: # SchedStrategy.DPS
            w[i] = [val / sum(w[i]) for val in w[i]] # normalize the weights for all classes

            wni = np.mean(w[i]) # average weight across all classes ??

            for k in range(K): # classes
                # index range for current station-class pair in state vector (across all phases)
                idxIni = q_indices[i][k]
                idxEnd = q_indices[i][k] + Kic[i][k] - 1
                wni += sum(w[i][k] * x[idxIni:idxEnd+1]) # number of jobs in each phase multiplied by the corresponding class weight

            # index range for current station in state vector (across all classes and phases)
            idxIni = q_indices[i][0]
            idxEnd = q_indices[i][K-1] + Kic[i][K-1] - 1

            # wni overwritten as the unweighted total number of jobs at station i ??
            wni = sum(x[idxIni:idxEnd+1])

            # phase changes
            for c in range(K): # classes
                if enabled[i][c]:
                    xic = q_indices[i][c]
                    for kic in range(Kic[i][c]): # current phase
                        for kic_p in range(Kic[i][c]): # destination phase
                            if kic != kic_p:
                                rate = PH[i][c][0][kic][kic_p] # rate of transitioning from current phase to destination phase
                                if wni > nservers[i]:
                                    rate *= nservers[i] * w[i][c][kic] / wni # scale by (num servers/weighted sum of all jobs) * weight for phase kic of current class
                                dx[xic+kic] -= x[xic+kic] * rate # outflow from current phase
                                dx[xic+kic_p] += x[xic+kic] * rate # inflow to destination phase

            # service completions
            for c in range(K): # current class
                if enabled[i][c]:
                    xic = q_indices[i][c]
                    for j in range(M): # destination station
                        for l in range(K): # destination class
                            xjl = q_indices[j][l]
                            if enabled[j][l]:
                                pie = map_pie(PH[j][l]) # equilibrium distribution over phases at time of completion
                                if rt[(i*K)+c][(j*K)+l] > 0:
                                    for kic in range(Kic[i][c]): # current phase
                                        for kjl in range(Kic[j][l]): # destination phases
                                            # compute transition rates
                                            rate = Phi[i][c][kic] * Mu[i][c][kic] * rt[(i*K)+c][(j*K)+l] * (pie[kjl] if isinstance(pie, list) else pie)
                                            if wni > nservers[i]:
                                                rate *= w[i][c][kic] / wni * nservers[i] # scale rate
                                            dx[xic+kic] -= x[xic+kic] * rate # outflow from current station
                                            dx[xjl+kjl] += x[xic+kic] * rate # inflow into destination station
    return dx

