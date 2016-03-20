# I think having the variable names match up with what
# cvxopt uses in their docs is nicer
# pylint: disable=invalid-name
"""Mean Absolute Deviation (MAD) Model"""

import numpy as np
from cvxopt import solvers, matrix

solvers.options["show_progress"] = False

def optimize_mad(returns, target_return, short_sales=False):
    """
    Solves:
        min (1/T)*sum(y_t)
        s.t. mu'*x >= target_return
             e'x = 1
             y_t >= r_t-mu, for all t
             y_t >= mu-r_t, for all t
             {x >= 0} - Short selling constraint
    where:
        r_t is the return at time t
        mu is the vector of expected returns of the stocks
        x is the optimal allocation

    cvxopt's lp solver solves:
        min c'x
        s.t. Gx <= h
             Ax = b
    """

    returns = np.asmatrix(returns)
    means = np.mean(returns, axis=1)

    num_stocks, num_samples = returns.shape

    c = np.zeros((num_samples + num_stocks, 1))
    c[0:num_samples, 0] = 1.0/num_samples
    c[num_samples:, 0] = 0.0

    beq = [1.0]

    # The target return constraint
    A_return_cstr = np.zeros((1, num_samples + num_stocks))
    A_return_cstr[0, :] = [0.0 for _ in range(num_samples)] + list(-means)

    A = np.concatenate((
        -1.*np.concatenate((
            np.eye(num_samples),
            np.transpose(-1.0*returns \
                + (means*np.ones((1, num_samples))))), axis=1),
        -1.*np.concatenate((
            np.eye(num_samples),
            np.transpose(returns \
                - (means*np.ones((1, num_samples))))), axis=1),
        A_return_cstr), axis=0)

    b = np.zeros((2*num_samples+1, 1))
    # Make sure it's a float or cvxopt
    # complains about not being a dtype
    b[2*num_samples, 0] = -float(target_return)

    if not short_sales:
        # Add the x >= 0 constraint
        A = np.concatenate((
            A,
            np.concatenate((
                np.zeros((num_stocks, num_samples)),
                -np.eye(num_stocks)), axis=1)), axis=0)
        b = np.concatenate((b, np.zeros((num_stocks, 1))), axis=0)

    Aeq = np.zeros((1, num_samples + num_stocks))
    Aeq[0, :] = [0.0 for _ in range(num_samples)] \
        + [1.0 for _ in range(num_stocks)]

    sol = solvers.lp(
        matrix(c),
        matrix(A),
        matrix(b),
        matrix(Aeq),
        matrix(beq)
    )

    return sol['x'][num_samples:]
