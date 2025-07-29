from line_solver.constants import SchedStrategy
import numpy as np
import time
import traceback

from native.solvers.fluid.solver_fluid_initsol import solver_fluid_initsol
from native.solvers.fluid.solver_fluid_iterations import solver_fluid_iteration


def solver_fluid(sn, schedid, options):
    # sn input refers to the structured network object from which model params are extracted
    M = sn.nstations  # number of stations
    K = sn.nclasses # number of classes
    N = sn.nclosedjobs  # population size
    Mu = sn.mu # service rates
    Phi = sn.phi # phase-type distributions
    PH = sn.proc # process-related parameters
    P = sn.rt # routing probabilities
    S = sn.nservers # number of servers at each station
    NK = sn.njobs  # initial population

    # Initialize the enable Boolean matrix that specifies which job classes are served at each station
    enable = np.zeros((M, K))
    for ist in range(M):
        for k in range(K):
            if np.all(np.isnan(Mu[ist][k])):
                Mu[ist][k] = []
                Phi[ist][k] = []
            enable[ist, k] = np.sum(P[:, ist * K + k]) > 0
        # if a station has infinite servers (e.g., delay), its server count is set to the population size
        if np.isinf(S[ist]):
            S[ist] = N

    #print('Number of servers:')
    #print(sn.nservers)

    max_time = np.inf
    Tstart = time.time()

    # Initialize the phases matrix to store the phases of each job class at each station
    phases = np.zeros((M, K))
    for ist in range(M):
        for k in range(K):
            phases[ist, k] = len(Mu[ist][k])

    # Initialize the matrix to store the slowest service rate for each job class at each station
    slowrate = np.zeros((M, K))
    for ist in range(M):
        for k in range(K):
            if np.all(Mu[ist][k]):
                slowrate[ist][k] = min(Mu[ist][k])
            else:
                slowrate[ist][k] = np.inf

    iters = 0 # iterations
    xvec_it = [] # state vectors at each iteration
    y0 = [] # default initial state
    assigned = np.zeros(K)

    # Construct default initial state vector (static or state-based)
    #use_existing_state = sn.state is not None
    use_existing_state = True

    # State-based initialization
    if use_existing_state:
        try:
            y0, _ = solver_fluid_initsol(sn, options)
        except Exception as e:
            print(f"[solver_fluid] Warning: Failed to initialize from sn.state, falling back to synthetic init.\n")
            print(f"Error: {e}")
            traceback.print_exc()
            use_existing_state = False

    # Static initialization
    if not use_existing_state:
        # If a class is served at a station, the initial population for that class is assigned to the first phase and the remaining phases are set to 0
        for ist in range(M):
            for k in range(K):
                if enable[ist, k] > 0:
                    if np.isinf(NK[k]): # infinite population
                        if schedid[ist] == SchedStrategy.EXT: # EXT
                            toAssign = 1
                        else:
                            toAssign = 0
                    else:
                        toAssign = NK[k] // np.sum(enable[:, k]) # even assignment of jobs to stations
                        if np.sum(enable[ist + 1:, k]) == 0:
                            toAssign = NK[k] - assigned[k] # add remaining jobs to last station
                    y0.extend([toAssign] + [0] * (int(phases[ist, k]) - 1)) # all other phases are set to 0
                    assigned[k] += toAssign
                else:
                    y0.extend([0] * int(phases[ist, k]))

    ydefault = np.array(y0).flatten() # default initial state vector

    # Pre process the passed initial state vector
    if options["init_sol"] is not None:
        try:
            if len(options['init_sol']) == len(ydefault):
                print("Using the provided initial state vector")
                init_sol = options["init_sol"]
            else:
                print("Flattening the initial state vector")
                # Flatten the initial state vector if it is nested
                init_sol = np.array([float(item) for sublist in options["init_sol"][0] for item in sublist]).flatten()
        except Exception as e:
            print(f"[solver_fluid] Warning: Failed to process the provided initial state vector. Using default initialization.\nError: {e}")
            init_sol = ydefault
    else:
        print("Using default initial solution")
        init_sol = ydefault  # Use the default initialization if no init_sol is provided

    """
    if options['init_sol'] is not None and len(options['init_sol']) == len(ydefault):
        init_sol = options['init_sol']
    else:
        print('using default initial solution')
        init_sol = ydefault   # Use the default initialization if no init_sol is provided
    """

    print(f"Initial solution: {init_sol}\n")

    # Append initial solution to the list of state vectors
    xvec_it.append(np.array(init_sol))

    # Run the fluid solver
    xvec_it, xvec_t, t, iters = solver_fluid_iteration(M, K, S, schedid, Mu, Phi, PH, P, xvec_it, init_sol, slowrate, Tstart, max_time, options)

    # print(len(xvec_it)) # number of iterations
    # print(len(t)) # number of time points during solving process

    xvec_t = np.array(xvec_t)
    runtime = time.time() - Tstart

    QN = np.zeros((M, K))

    QNt = [[None for _ in range(K)] for _ in range(M)] # transient avg queue length for each job class at each station
    Qt = [None for _ in range(M)] # transient avg queue length at each station
    UNt = [[None for _ in range(K)] for _ in range(M)] # transient utilisation for each job class at each station

    for ist in range(M):
        Qt[ist] = 0
        for k in range(K):
            shift = int(np.sum(phases[:ist]) + np.sum(phases[ist, :k]))
            QN[ist, k] = np.sum(xvec_it[-1][shift:shift + int(phases[ist, k])])
            QNt[ist][k] = np.sum(xvec_t[:, shift:shift + int(phases[ist, k])], axis=1)
            Qt[ist] += QNt[ist][k]

    for ist in range(M):
        if S[ist] > 0:
            for k in range(K):
                # NOTE: fails when Qt[ist] is 0 (e.g., in an initial state)
                # UNt[ist][k] = np.minimum(QNt[ist][k] / S[ist], QNt[ist][k] / Qt[ist])
                # UNt[ist][k][np.isnan(UNt[ist][k])] = 0

                # add a condition to avoid division by zero
                if all(Qt[ist]) > 0:
                    UNt[ist][k] = np.minimum(QNt[ist][k] / S[ist], QNt[ist][k] / Qt[ist])
                else:
                    UNt[ist][k] = QNt[ist][k] / S[ist]  # Use only the server count for utilization
                UNt[ist][k][np.isnan(UNt[ist][k])] = 0
        else:
            for k in range(K):
                UNt[ist][k] = QNt[ist][k]

    return QN, xvec_it, QNt, UNt, xvec_t, t, iters, runtime
