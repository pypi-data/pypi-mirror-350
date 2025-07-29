import jpype

from line_solver import SchedStrategy, jlineMatrixFromArray, jlineMatrixToArray
from line_solver import State
from line_solver import *
import numpy as np

# Constructs the initial solution for the fluid solver based on the network state (sn)

def solver_fluid_initsol(sn, options=None):

    """
    if options is None:
        options = Solver.defaultOptions

    # AttributeError: type object 'Solver' has no attribute 'defaultOptions'
    """

    init_sol = []
    state = {}

    M = sn.nstations
    sched = sn.sched

    # print(sn)

    # Convert scheduling policies to numerical IDs for faster processing
    schedid = [None] * M
    for i in range(M):
        java_schedi = SchedStrategy.fromLINEString(sched[i]) # From string to SchedStrategy Java object
        schedid[i] = SchedStrategy.toID(java_schedi) # From SchedStrategy Java to ID as int

    # iterate over all nodes
    for ind in range(sn.nnodes):
        # only consider stateful nodes
        if sn.isstateful[ind]:

            isf = int(sn.nodeToStateful[0, ind]) # assumes that nodeToStateful is a 1-row matrix
            ist = int(sn.nodeToStation[0, ind]) # assumes that nodeToStation is a 1-row matrix

            state_i = [] # tracks the detailed state of node i
            init_sol_i = []  # initial solution for node i (does not track disabled classes, removes Inf entries)

            state_matrix = jlineMatrixFromArray(sn.state[isf])
            stats = State.toMarginal(sn.obj, ind, state_matrix, None, None, None, None, None) # gets marginal statistics from state of network

            nir = stats.nir # number of jobs at station i for each class r
            nir_numpy = jlineMatrixToArray(nir) # convert from jline.util.Matrix to numpy array
            kir_i = stats.kir # number of jobs at station i in each phase (k) of each class (r)

            # NOTE: kir_i is a list of arrays, where each array corresponds to a phase
            # Currently, it is assumed that each entry in kir_i corresponds to a class

            kir_i_numpy = [jlineMatrixToArray(matrix) for matrix in list(kir_i)]
            #print(f'kir_i: {kir_i}')
            #print(f'kir_i_numpy: {kir_i_numpy}')

            # if node represents an external arrival process
            if schedid[ist] == 13: # SchedStrategy.EXT
                state_i.append([float('Inf')])  # fluid does not model infinite buffer?
                # iterates over classes
                for r in range(len(kir_i_numpy)):
                    print(kir_i_numpy[r])
                    # iterates over phases
                    for k in range(len(kir_i_numpy[r])):
                        value = kir_i_numpy[r][k] # number of jobs in phase k of class r
                        state_i.append([value])
                        if not np.isnan(sn.rates[ist][r]):
                            init_sol_i.append([value])


            elif schedid[ist] in [1, 3, 6, 0, 7, 11]:
                """
                SchedStrategy.FCFS,
                SchedStrategy.SIRO,
                SchedStrategy.PS,
                SchedStrategy.INF,
                SchedStrategy.DPS,
                SchedStrategy.HOL
                """
                """
                # iterate over classes
                # assumes each entry in kir_i_numpy corresponds to a class - wrong
                for r in range(len(nir_numpy)):
                    #print(f'class {r} has {len(kir_i_numpy[r])} phases at station {ist}')
                    # iterate over phases
                    for k in range(len(kir_i_numpy[r])):
                        # if first phase (0 or 1?)
                        if k == 0:
                            # wait buffer = total number of class r jobs - number of class r jobs in service phases
                            # sum across all phases (except phase 1)
                            wait_buffer = nir_numpy[r] - sum(kir_i_numpy[r][phase] for phase in range(1, len(kir_i_numpy[r])))
                            state_i.append([wait_buffer])  # jobs in waiting buffer are re-started in phase 1 so they are added to the detailed state of the node
                            if not np.isnan(sn.rates[ist][r]):
                                init_sol_i.append([wait_buffer])  # jobs in waiting buffer are re-started in phase 1 so they are added to the initial condition
                        else:
                            value = kir_i_numpy[r][k]  # number of jobs in phase k of class r
                            state_i.append([value])
                            if not np.isnan(sn.rates[ist][r]):
                                init_sol_i.append([value])
                """
                # iterate over phases
                for k, phase_values in enumerate(kir_i_numpy):
                    # print(f"Phase {k}: {phase_values}")
                    # # iterate over classes within current phase
                    for r, value in enumerate(phase_values):
                        if k == 0:
                            wait_buffer = nir_numpy[r] - sum(kir_i_numpy[r][k] for i in range(1, len(kir_i_numpy[r])))
                            state_i.append([wait_buffer])
                            if not np.isnan(sn.rates[ist][r]):
                                init_sol_i.append([wait_buffer])
                        else:
                            state_i.append([value])
                            if not np.isnan(sn.rates[ist][r]):
                                init_sol_i.append([value])

            else:
                print(f'Unsupported scheduling policy at station {ist}')
                return

            init_sol.extend([x[0] for x in init_sol_i])  # flatten to 1D

            state[isf] = state_i

    #print(f'init_sol: {init_sol}')
    return init_sol, state


# nodeToStation: map between nodes and their corresponding stateful nodes (matrix)
# nodeToStateful: map betwee nodes and their corresponding stations (matrix)
