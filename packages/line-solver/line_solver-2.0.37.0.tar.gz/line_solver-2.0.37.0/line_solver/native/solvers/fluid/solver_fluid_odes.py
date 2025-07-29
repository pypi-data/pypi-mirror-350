from native.solvers.fluid.ode_jumps_new import *
import numpy as np

from native.solvers.fluid.ode_rate_base import ode_rate_base
from native.solvers.fluid.ode_rates_closing import ode_rates_closing


# Constructs the fluid ODE equations that govern the dynamics of the system
# i.e., the evolution in the number of jobs in different phases at each station

def solver_fluid_odes(M, K, S, schedid, Mu, phi, PH, P, options):

    # M = sn.nstations  # number of stations
    # K = sn.nclasses # number of classes
    # S = sn.nservers # number of servers
    w = np.ones((M, K)) # weight matrix for scheduling policies (initialized to 1)

    enabled = np.zeros((M, K), dtype=bool)  # boolean matrix indicated the classes served at each station
    q_indices = np.zeros((M, K), dtype=int) # maps each station-class pair to its position in the state vector
    Kic = np.zeros((M, K), dtype=int) # number of phases for each station-class pair
    cumsum = 0 # cumulative sum

    # Convert scheduling policies to numerical IDs for faster processing
    """
    schedid = [None] * M
    for i in range(M):
        java_schedi = SchedStrategy.fromLINEString(sched[i]) # From string to SchedStrategy Java object
        schedid[i] = SchedStrategy.toID(java_schedi) # From SchedStrategy Java to ID as int
        # NOTE: Keep below for DPS?
        if schedid[i] == 7: # DPS
            w[i, :] = schedparam[i, :]
    """

    # iterate over stations
    for i in range(M):
        # iterate over job classes
        for c in range(K):
            if np.all(np.isnan(Mu[i][c])):
                numphases = 0
                enabled[i, c] = False
                q_indices[i, c] = cumsum
            elif len(Mu[i][c]) == 0:
                enabled[i, c] = False
                numphases = 0
                q_indices[i, c] = cumsum
            else:
                numphases = len(Mu[i][c]) # get number of phases for processing job class c station i
                q_indices[i, c] = cumsum
                enabled[i, c] = True
            Kic[i, c] = numphases # log the number of phases
            cumsum += numphases

    # define ODE system to be returned
    if options['method'] == 'softmin':
        print("Solving with softmin method...")
        alpha = 20  # controls sharpness of min approx
        def ode_softmin_wrapper(t, x):
            return ode_softmin(x, phi, Mu, PH, M, K, enabled, q_indices, P, Kic, S, w, schedid, alpha)
        ode_h = ode_softmin_wrapper

    elif options['method'] == 'statedep':
        pass
        """
        def ode_statedep_wrapper(t, x):
            # computes derivatives of the state vector
            return ode_statedep(x, phi, Mu, PH, M, K, enabled, q_indices, P, Kic, nservers, w, schedid)
        ode_h = ode_statedep_wrapper
        """
    else:
        print("Solving with default method...")
        all_jumps = ode_jumps_new(M, K, enabled, q_indices, P, Kic) # all possible state transitions (each col gives the state change vector for each transition/event)
        all_jumps = np.array(all_jumps) # convert to np array
        rateBase, eventIdx = ode_rate_base(phi, Mu, PH, M, K, enabled, q_indices, P, Kic, all_jumps) # base rates for all possible transitions (constant/state independent rate at which each events occurs)

        # print(f"all_jumps:\n{all_jumps.T}")
        # print(f"rateBase:\n{rateBase}")

        # baseline_derivate = all_jumps.T @ rateBase # baseline dx/dt = Ax (provided rates are constant)
        # print("Baseline derivative (all_jumps @ rateBase):")
        # print(baseline_derivate)

        # The ODE is generally non-linear and depends on the current state (queue lengths, server capacities, scheduling policies etc.)
        # Below we solve for the non linear ODE dx/dt = f(x) = all_jumps * ode_rates_closing(x) (transition rates are re-computed based on current state)
        # The coef matrix changes over time, hence we can only get an approximation of it by linearilizing the system (e.g., by computing the Jacobian of f(x) at a fixed state x)
        def ode_closing_wrapper(t, x):
            # computes derivatives of the state vector
            rates = np.array(ode_rates_closing(x, M, K, enabled, q_indices, Kic, S, w, schedid, rateBase, eventIdx))
            return all_jumps.T @ rates
        ode_h = ode_closing_wrapper

    return ode_h, q_indices
