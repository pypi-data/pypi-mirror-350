from line_solver.native.solvers.fluid.solver_fluid_odes import *
import numpy as np
from scipy.integrate import solve_ivp
from time import time

def solver_fluid_iteration(M, K, S, schedid, Mu, Phi, PH, P, xvec_it, ydefault, slowrate, Tstart, max_time, options):

    iter_max = options['iter_max']
    verbose = options['verbose']
    tol = options['tol']
    iter_tol = options['iter_tol']
    stiff = options['stiff']
    timespan = options['timespan']

    goon = True
    iter = 0
    allt = []
    ally = []
    lastmsg = ''
    t = []
    xvec_t = []

    nonZeroRates = slowrate.ravel()
    nonZeroRates = nonZeroRates[nonZeroRates > tol]
    nonZeroRates = nonZeroRates[np.isfinite(nonZeroRates)]
    rategap = np.log10(np.max(nonZeroRates) / np.min(nonZeroRates))

    # Get the ODE system from solver_fluid_odes
    ode_h, _ = solver_fluid_odes(M, K, S, schedid, Mu, Phi, PH, P, options)

    # Initialize time and solver options
    T0 = timespan[0]
    odeopt = {'atol': tol, 'rtol': tol, 'method': 'BDF' if stiff else 'RK45', 'vectorized': True}
    T = 0

    while (np.isfinite(timespan[1]) and T < timespan[1]) or (goon and iter < iter_max):
        iter += 1
        if time() - Tstart > max_time:
            goon = False
            break

        # Initialize state for current iteration
        y0 = xvec_it[iter - 1]
        y0 = np.array(y0).flatten()

        # Dynamically adjust the time range for the current iteration (based on slowest rates)
        if iter == 1:
            T = min(timespan[1], abs(10 / np.min(nonZeroRates)))
        else:
            T = min(timespan[1], abs(10 * iter / np.min(nonZeroRates)))

        trange = (T0, T)

        try:
            sol = solve_ivp(ode_h, trange, y0, **odeopt)
        except Exception as e:
            print(f"An error occurred during the ODE solving process: {e}")
            print("Attempting to solve with the default initialization.")
            sol = solve_ivp(ode_h, trange, ydefault, **odeopt)

        # Extract time points and state vectors from the solution
        t_iter = sol.t
        ymean_t_iter = sol.y.T # one state vector at each time point in the time range

        xvec_t.extend(ymean_t_iter) # extend -> adds each element of an iterable to the end of the list
        t.extend(t_iter)
        xvec_it.append(list(xvec_t[-1])) # append -> adds a single element to the end of the list


        # relative change in state vector between current and previous iteration
        movedMassRatio = np.linalg.norm(np.array(xvec_it[-1]) - np.array(xvec_it[-2]), 1) / 2 / np.sum(xvec_it[-2])

        T0 = T # start time of next iteration updated to the end of current time range

        # store time points across all iterations
        if len(allt) == 0:
            allt = t
        else:
            allt = np.concatenate((allt, allt[-1] + np.array(t)))

        # store state vectors all iterations
        ally.extend(xvec_t)

        if verbose > 0:
            llmsg = len(lastmsg)
            if llmsg > 0:
                for ib in range(llmsg):
                    print('\b')

        # stop when state vector converges
        if movedMassRatio < iter_tol:
            pass

        if T >= timespan[1]:
            goon = False

    # returns:
    # - xvec_it: stores the final state vector at each iteration -> depends on the number of iterations
    # - xvec_t: stores the state vector at each time point in the solving process -> depends on the number of time points t
    # - t: time points at which the state vector is evaluated during the integration process
    # - iter: total number of iterations performed
    return xvec_it, xvec_t, t, iter
