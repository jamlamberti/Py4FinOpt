from cvxopt import solvers, matrix
import collections
import numpy as np

solvers.options["show_progress"] = False

def optimize_downside_variance(returns, m, short_sales=False):
    # min (1/T)sum(y_t^2)
    # s.t. mu*x >= m
    # e'x = 1
    # y_t >= 0
    # y_t >= (mu-ret_t)*x
    # {x >= 0} - Shorting constraint
    
    returns = np.asmatrix(returns)
    means = np.mean(returns, axis=1)

    N, T = returns.shape
    
    P = (2.0/T)*np.concatenate((np.zeros((N, N+T)),
        np.concatenate((np.zeros((T, N)), np.eye(T)), axis=1)),axis=0)

    q = np.zeros((N+T, 1))
    
    A = np.zeros((1, T+N))
    A[0, 0:N] = 1.0
    
    b = [1.0]
    
    h = np.zeros((2*T + 1, 1))
    h[0, 0] = -m
    
    G_0 = np.zeros((1, N+T))
    G_0[0, 0:N] = -np.transpose(means)
    
    G_1 = np.concatenate((np.zeros((T, N)), -1.0*np.eye(T)), axis=1)
    G_2 = np.concatenate((np.transpose(-returns+(means*np.ones((1, T)))), -1.0*np.eye(T)), axis=1)
    G = np.concatenate((G_0, G_1, G_2), axis=0)
    
    if not short_sales:
        h = np.concatenate((h, np.zeros((N, 1))), axis=0)
        G = np.concatenate((G, np.concatenate((-1.0*np.eye(N), np.zeros((N, T))), axis=1)), axis=0)

    sol = solvers.qp(
        matrix(P),
        matrix(q),
        matrix(G),
        matrix(h),
        matrix(A),
        matrix(b)
    )

    return sol['x'][:N]

