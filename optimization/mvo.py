# I think having the variable names match up with what
# cvxopt uses in their docs is nicer
# pylint: disable=invalid-name
"""Mean Variance Optimization (MVO) Model"""
import numpy as np
from cvxopt import solvers, matrix

solvers.options["show_progress"] = False


def optimize_mv(returns, target_return, short_sales=False):
    """
    Solves the MVO model:
        min x'Qx
        s.t. mu'x >= target_return
             e'x = 1
             {x >= 0} - Short selling constraint
    """
    returns = np.asmatrix(returns)
    num_stocks = returns.shape[0]
    means = np.mean(returns, axis=1)

    P = np.cov(returns)

    q = [0.0 for _ in range(num_stocks)]

    G = np.zeros((1, num_stocks)) + np.transpose(-1.0 * means)
    h = [float(-target_return)]

    if not short_sales:
        G = np.concatenate((G, -np.eye(num_stocks)), axis=0)
        h = h + [0.0 for _ in range(num_stocks)]

    A = np.ones((1, num_stocks))
    b = [1.0]

    sol = solvers.qp(
        matrix(2 * P),
        matrix(q),
        matrix(G),
        matrix(h),
        matrix(A),
        matrix(b)
    )

    return sol['x']
