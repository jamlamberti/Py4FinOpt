from cvxopt import solvers, matrix
import collections
import numpy as np

solvers.options["show_progress"] = False

def optimize_mad(returns, m, short_sales=False):
    returns = np.asmatrix(returns)
    means = np.mean(returns, axis=1)
    N, T = returns.shape
    
    c = np.zeros((T+N, 1))
    c[0:T, 0] = 1.0/T
    c[T:, 0] = 0.0
    
    beq = [1.0]

    A1 = -np.concatenate((np.eye(T), np.transpose(-returns+(means*np.ones((1, T))))), axis=1)
    A2 = -np.concatenate((np.eye(T), np.transpose(returns-(means*np.ones((1, T))))), axis=1)
    A3 = np.zeros((1, T+N))
    A3[0, :] = [0.0 for _ in range(T)] + list(-means)
    A = np.concatenate((A1, A2, A3), axis=0)

    b = np.zeros((2*T+1, 1))
    b[2*T, 0] = -m

    if not short_sales:
        A = np.concatenate((A, np.concatenate((np.zeros((N, T)), -np.eye(N)), axis=1)), axis=0)
        b = np.concatenate((b, np.zeros((N, 1))), axis=0)
    
    Aeq = np.zeros((1, T+N))
    Aeq[0, :] = [0.0 for _ in range(T)] + [1.0 for _ in range(N)]
    
    sol = solvers.lp(
        matrix(c),
        matrix(A),
        matrix(b),
        matrix(Aeq),
        matrix(beq)
    )

    return sol['x'][T:]

