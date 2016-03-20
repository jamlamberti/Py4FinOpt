import numpy as np
from cvxopt import solvers, matrix
import scipy.stats

solvers.options["show_progress"] = False

def optimize_mv(returns, m, short_sales=False):
    returns = np.asmatrix(returns)

    # K is the number of stocks
    K = returns.shape[0]

    # Compute the means of the returns
    mu = np.mean(returns, axis=1)
    P = np.cov(returns)
    q = [0.0 for _ in range(K)]

    G = np.zeros((1, K)) + np.transpose(-1.0*mu)
    h = [float(-m)]
    
    if not short_sales:
        G = np.concatenate((G, -np.eye(K)), axis=0)
        h = h + [0.0 for _ in range(K)]

    A = np.ones((1, K))
    b = [1.0]
    sol = solvers.qp(
        matrix(2*P),
        matrix(q),
        matrix(G),
        matrix(h),
        matrix(A),
        matrix(b)
    )

    return sol['x']

