# I think having the variable names match up with what
# cvxopt uses in their docs is nicer
# pylint: disable=invalid-name
"""Downside Variance Model"""
import numpy as np
from cvxopt import solvers, matrix

solvers.options["show_progress"] = False

def optimize_downside_variance(returns, target_return, short_sales=False):
    """
    Solves the downside variance model:
        min (1/T)*sum(y_t^2)
        s.t. mu'*x >= target_return
             e'x = 1
             y_t >= 0
             y_t >= (mu-r_t)*x
             {x >= 0} - Short selling constraint
    where:
        x is the optimal allocation
        mu is the vector of expected returns of the stocks
        r_t is the return at time t

    cvx solves:
        min (1/2)x'Px + q'x
        s.t. Gx <= h
             Ax = b
    """

    returns = np.asmatrix(returns)
    means = np.mean(returns, axis=1)

    num_stocks, num_samples = returns.shape

    # Note: we are accounting for the 1/2 here
    P = (2.0/num_samples)*np.concatenate((
        np.zeros((num_stocks, num_stocks + num_samples)),
        np.concatenate((
            np.zeros((num_samples, num_stocks)),
            np.eye(num_samples)), axis=1)), axis=0)

    q = np.zeros((num_stocks + num_samples, 1))

    A = np.zeros((1, num_samples + num_stocks))
    A[0, 0:num_stocks] = 1.0

    b = [1.0]

    h = np.zeros((2*num_samples + 1, 1))
    h[0, 0] = -float(target_return)

    # Constraint on target returns mu'*x > m
    G_return_cstr = np.zeros((1, num_stocks + num_samples))
    G_return_cstr[0, 0:num_stocks] = -means.T

    G = np.concatenate((
        G_return_cstr,
        np.concatenate((
            np.zeros((num_samples, num_stocks)),
            -1.0*np.eye(num_samples)), axis=1),
        np.concatenate((
            np.transpose(-1.0*returns+(means*np.ones((1, num_samples)))),
            -1.0*np.eye(num_samples)), axis=1)
        ), axis=0)

    if not short_sales:
        # Add in the no shorting constraint (x >= 0)
        h = np.concatenate((h, np.zeros((num_stocks, 1))), axis=0)
        G = np.concatenate((
            G,
            np.concatenate((
                -1.0*np.eye(num_stocks),
                np.zeros((num_stocks, num_samples))), axis=1)
            ), axis=0)

    sol = solvers.qp(
        matrix(P),
        matrix(q),
        matrix(G),
        matrix(h),
        matrix(A),
        matrix(b)
    )

    return sol['x'][:num_stocks]
