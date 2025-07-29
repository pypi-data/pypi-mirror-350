from line_solver.constants import SchedStrategy
# Transforms the base rates corresponding to possible state changes based on the scheduling discipline of the source station
def ode_rates_closing(x, M, K, enabled, q_indices, Kic, nservers, w, schedid, rateBase, eventIdx):
    # RATES = ODE_RATES_BOTTQ(X, M, K, Q_INDICES, KIC, NSERVERS, W, STRATEGY, RATEBASE, EVENTIDX)

    # - x: current state vector
    # - M: number of stations
    # - K: number of job classes
    # - enabled: matrix indicating whether each station-class pair is enabled
    # - q_indices: matrix mapping each station-class pair to its starting index in the state vector
    # - Kic: matrix storing the number of phases for each station-class pair
    # - nservers: array storing the number of servers in each station
    # - w: matrix storing weights for each job class and phase
    # - schedid: array indicating the scheduling policy at each station
    # - rateBase: array of base rates for each possible state change
    # - eventIdx: array of indices in the state vector indicating the corresponding source state variable that led to each state change

    # rates initialised to the state vector
    rates = list(x)  # basic vector valid for INF and PS case min(ni,nservers(i))=ni

    eventIdx = eventIdx.flatten()
    eventIdx = eventIdx.astype(int)

    # print(f"q_indices: {q_indices}") # q_indices: [[0], [1], [3], [4]]
    # print(f"Kic: {Kic}") # Kic: [[1], [2], [1], [1]]
    # print(eventIdx) # contains 4 as dependents on q_indces...

    for i in range(M): # station

        if schedid[i] == SchedStrategy.INF: # SchedStrategy.INF
            pass  # do nothing - rate remains the same

        elif schedid[i] == SchedStrategy.EXT:  # SchedStrategy.EXT external arrival station
            for k in range(K): # job class
                # index range in state vector for station-class pair
                idxIni = q_indices[i, k]
                idxEnd = q_indices[i, k] + Kic[i, k] - 1
                if enabled[i, k]:
                    # ensure mass conservation at the EXT station
                    # ensures that the arrival rate decreases as the number of jobs in later phases increases to prevent system overload (no equivalent logic for the sofmin approximation)
                    rates[idxIni] = 1 - sum(x[idxIni + 1 : idxEnd + 1]) # 1 - total number of jobs in phases 2 and beyond

        # PS or FCFS
        elif schedid[i] == SchedStrategy.PS or  schedid[i] == SchedStrategy.FCFS: # SchedStrategy.PS or SchedStrategy.FCFS
            # index range in state vector for station
            idxIni = q_indices[i, 0]
            idxEnd = q_indices[i, K - 1] + Kic[i, K - 1] - 1
            # total number of jobs at station i across all classes and phases
            ni = sum(x[idxIni : idxEnd + 1])
            if ni > nservers[i]:
                rates[idxIni:idxEnd + 1] = [xi / ni * nservers[i] for xi in x[idxIni:idxEnd + 1]]

        # DPS
        elif schedid[i] == SchedStrategy.DPS: # SchedStrategy.DPS
            w[i, :] = w[i, :] / sum(w[i, :]) # weights for all classes are normalized so that they sum to 1
            ni = sum(w[i, :]) # initialisation choice: sum of weights for all classes in station i ??
            for k in range(K): # class
                # index range in the state vector the station-class pair
                idxIni = q_indices[i, k]
                idxEnd = q_indices[i, k] + Kic[i, k] - 1
                if enabled[i, k]:
                    ni = ni + sum(w[i, k] * x[idxIni:idxEnd + 1]) # total weighted number of jobs in station i (multiplify job count in each phase by the class weight)
            for k in range(K): # class
                # index range in the state vector the station-class pair
                idxIni = q_indices[i, k]
                idxEnd = q_indices[i, k] + Kic[i, k] - 1
                if enabled[i, k]:
                    # scale rates at each phase
                    rates[idxIni:idxEnd + 1] = [w[i, k] * xi / ni * nservers[i] for xi in x[idxIni:idxEnd + 1]]

    # rates list contain the adjustment for all state variables. However, not all state variables are associated with state changes
    # rates filtered to include only the rates corresponding to the source state variables that trigger each possible state change.
    # This makes the rates list align with the baseRate list
    rates = [rates[i] for i in eventIdx]

    # adjust the base rate of all possible state transitions (jumps)
    rates = [rateBase[i] * rate for i, rate in enumerate(rates)]
    return rates

# THIS PART TO BE KEPT AS IT ALLOWS TO MAKE RATES STATE-DEPENDENT
# def get_index(j, k):
#     # XJ = GET_INDEX(J,K)
#     # n is the state vector
#     # j is the queue station index
#     # k is the class index
#     # RETURNS THE INDEX of the queue-length element xi! # in the state description
#     xj = 1
#     for z in range(j - 1):
#         for y in range(K):
#             xj = xj + Kic[z, y]
#     for y in range(k - 1):
#         xj = xj + Kic[j, y]
#     return xj

# def ode_rates(x):
#     rates = []
#     n = [0] * M  # total number of jobs in each station
#     for i in range(M):
#         for c in range(K):
#             xic = q_indices[i, c]
#             n[i] += sum(x[xic:xic + Kic[i, c]])
#         if S[i] == sum(N):
#             n[i] = 1

#     for i in range(M):  # transition rates for departures from any station to any other station
#         for c in range(K):  # considers only transitions from the first service phase (enough for exp servers)
#             if match[i, c] > 0:
#                 xic = q_indices[i, c]
#                 for j in range(M):
#                     for l in range(K):
#                         if P[(i - 1) * K + c, (j - 1) * K + l] > 0:
#                             for k in range(Kic[i, c]):
#                                 if x[xic + k - 1] > 0 and n[i] > S[i]:
#                                     rates.append(Phi[i][c][k] * P[(i - 1) * K + c, (j - 1) * K + l] * Mu[i][c][k] * x[xic + k - 1] / n[i] * S[i])
#                                 elif x[xic + k - 1] > 0:
#                                     rates.append(Phi[i][c][k] * P[(i - 1) * K + c, (j - 1) * K + l] * Mu[i][c][k] * x[xic + k - 1])
#                                 else:
#                                     rates.append(0)

#     for i in range(M):  # transition rates for "next service phase" (phases 2...)
#         for c in range(K):
#             if match[i, c] > 0:
#                 xic = q_indices[i, c]
#                 for k in range(Kic[i, c] - 1):
#                     if x[xic + k - 1] > 0:
#                         rates.append((1 - Phi[i][c][k]) * Mu[i][c][k] * x[xic + k - 1] / n[i])
#                     else:
#                         rates.append(0)
#     return rates

# def ode_jumps(x):
#     d = []  # returns state changes triggered by all the events
#     for i in range(M):  # state changes from departures in service phases 2...
#         for c in range(K):
#             if match[i, c] > 0:
#                 xic = q_indices[i, c]
#                 for j in range(M):
#                     for l in range(K):
#                         if P[(i - 1) * K + c, (j - 1) * K + l] > 0:
#                             xjl = q_indices[j, l]
#                             for k in range(Kic[i, c]):
#                                 jump = [0] * len(x)
#                                 jump[xic] -= 1  # type c in stat i completes service
#                                 jump[xjl] += 1  # type c job starts in stat j
#                                 d.append(jump)

#     for i in range(M):  # state changes from "next service phase" transition in phases 2...
#         for c in range(K):
#             if match[i, c] > 0:
#                 xic = q_indices[i, c]
#                 for k in range(Kic[i, c] - 1):
#                     jump = [0] * len(x)
#                     jump[xic + k - 1] -= 1
#                     jump[xic + k] += 1
#                     d.append(jump)
#     return d
