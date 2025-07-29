import numpy as np
from line_solver.api import map_pie
from line_solver.api import jlineMatrixToArray

# Computes the base rates for all possible state changes (jumps)
def ode_rate_base(phi, Mu, PH, M, K, enabled, q_indices, rt, Kic, all_jumps):
    #rateBase = np.zeros((all_jumps.shape[1], 1)) # vector of rates corresponding to each state change
    #eventIdx = np.zeros((all_jumps.shape[1], 1)) # vector of indices indicating which state variable has triggered event

    rateBase = np.zeros((len(all_jumps), 1))
    eventIdx = np.zeros((len(all_jumps), 1))
    rateIdx = 0

    # Identify disabled nodes based on the routing matrix
    disabled_nodes = [i for i in range(M) if np.all(rt[i * K:(i + 1) * K, :] == 0)]

    # state changes due to completions
    for i in range(M): # source station
        if i in disabled_nodes:
            for l in range(K):
                for _ in range(Kic[i][c]):
                    rateIdx += 1

                    rateBase[rateIdx-1] = 0
                    eventIdx[rateIdx-1] = 0
        else:
            for c in range(K): # source class
                if enabled[i, c]:
                    for j in range(M): # destination station
                        for l in range(K): # destination class
                            if len(PH[j][l]) == 0: # ph distribution of destination is empty -> no phases
                                pie = 1
                            else:
                                pie = map_pie(PH[j][l]) # steady-state probabilities over the phases at the destination station computed at the instants of completion at the source
                                # print(pie)
                            # if rt[(i-1)*K+c, (j-1)*K+l] > 0:
                            if rt[i*K+c, j*K+l] > 0:
                                for kic in range(Kic[i, c]): # source phases
                                    for kjl in range(Kic[j, l]): # destination phases
                                        #print(f"event from station {i} phase {kic} to station {j} phase {kjl}")
                                        rateIdx += 1

                                        # Extract scalar values from arrays
                                        phi_value = phi[i][c][kic][0] if isinstance(phi[i][c][kic], np.ndarray) else phi[i][c][kic]
                                        mu_value = Mu[i][c][kic][0] if isinstance(Mu[i][c][kic], np.ndarray) else Mu[i][c][kic]
                                        rt_value = rt[i*K+c, j*K+l]

                                        # Handle pie as a nested array
                                        if isinstance(pie, np.ndarray):
                                            pie_value = pie[0][kjl] if pie.ndim == 2 else pie.flatten()[kjl]
                                        else:
                                            pie_value = pie  # Use directly if it's already a scalar

                                        # Compute the rate
                                        rateBase[rateIdx-1] = phi_value * mu_value * rt_value * pie_value
                                        eventIdx[rateIdx-1] = q_indices[i, c] + kic # record index of source variable

    # state changes due to phase transitions
    for i in range(M): # current station
        for c in range(K): # current class
            if enabled[i, c]:
                for kic in range(Kic[i, c]): # source phase
                    for kicp in range(Kic[i, c]): # destination phase within same station
                        if kicp > kic: # destination phase must be greater than source phase in the same station
                            rateIdx += 1
                            # print(f"event from station {i} phase {kic} to station {i} phase {kicp}")

                            # NOTE: below fails if PH[i][c][1] is a jline matrix cell object
                            """
                            if not isinstance(PH[i][c][0], np.ndarray):
                                ph_numpy = []
                                for k in range(PH[i][c][0].size()):
                                    ph_numpy.append(jlineMatrixToArray(PH[i][c][0].get(k)))
                                ph_numpy_combined = np.block(ph_numpy)
                                rateBase[rateIdx-1] = ph_numpy_combined[kic, kicp]
                                eventIdx[rateIdx-1] = q_indices[i, c] + kic
                            """
                            rateBase[rateIdx-1] = PH[i][c][0][kic, kicp]
                            eventIdx[rateIdx-1] = q_indices[i, c] + kic # record index of source variable

    return rateBase, eventIdx
