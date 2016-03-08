import numpy as np
from cvxopt import solvers, matrix

def mvo(returns, m=100):
    # K is the number of stocks
    K = returns.shape[1]

    # Compute the means of the returns
    mu = np.mean(returns, axis=1)

    Q = np.cov(returns)

    G = -1.0*np.eye(K)
    h = np.zeros((K, 1))
    A = np.ones((1, K))
    b = [1.0]
    
    # Solve the QP
    sol = solvers.qp(
        matrix(m*Q),
        matrix(-1.0*mu),
        matrix(G),
        matrix(h),
        matrix(A),
        matrix(b)
    )

    # Get the values of decision variable x
    return sol['x']

