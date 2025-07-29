import numpy as np

def ode_jumps_new(M, K, enabled, q_indices, P, Kic):
    #print(M) # 4
    #print(K) # 1
    #print(Kic) # num of phases for each class at each station (4x1 vector)

    jumps = []  # list of state changes trigerred by events

    # sum(Kic) row-wise sum: returns total number of phases for each class among all stations
    # sum(sum(Kic)) column-wise sum: returns total number of phases across all jobs and stations (matches dimensions of state vector)


    # Identify disabled nodes based on the routing matrix
    disabled_nodes = [i for i in range(M) if np.all(P[i * K:(i + 1) * K, :] == 0)]

    # state changes due to service completion
    for i in range(M): # source station
        if i in disabled_nodes:
            for c in range(K):
                for _ in range(Kic[i][c]):
                    jumps.append([0] * sum(sum(Kic)))
        else:
            for c in range(K): # source class
                if enabled[i][c]:
                    xic = q_indices[i][c]  # index of source station-class pair in state vector
                    for j in range(M): # destination station
                        for l in range(K): # destination class
                            if P[i * K + c][j * K + l] > 0:
                                xjl = q_indices[j][l]  # index of destination station-class pair in state vector
                                for ki in range(Kic[i][c]):  # source phase
                                    for kj in range(Kic[j][l]):  # destination phase
                                        jump = [0] * sum(sum(Kic))
                                        jump[xic+ki] = jump[xic+ki] - 1  # class c job completes service in station i at phase ki
                                        jump[xjl+kj] = jump[xjl+kj] + 1  # the same job starts service at station j in phase kj under class l
                                        jumps.append(jump)

    # state changes due to phase transitions
    for i in range(M): # current station
        for c in range(K): # current job class
            if enabled[i][c]:
                xic = q_indices[i][c]
                for ki in range(Kic[i][c] - 1): # source phase
                    for kip in range(Kic[i][c]): # destination phase
                        if ki != kip:
                            jump = [0] * sum(sum(Kic)) # new jump vector
                            jump[xic+ki] = jump[xic+ki] - 1 # job c completes service in phase ki
                            jump[xic+kip] = jump[xic+kip] + 1 # job c starts service in phase kip
                            jumps.append(jump)

    return jumps # all possible state changes

# NOTE: Keep all data structures as lists and convert when needed as np arrays don't support dynamic resizing
