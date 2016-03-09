import numpy as np
from cvxopt import solvers, matrix
import scipy.stats

solvers.options["show_progress"] = False

def mvo_no_shorts(returns, m):
    returns = np.asmatrix(returns)
    K = returns.shape[0]

    # Compute the means of the returns
    mu = np.mean(returns, axis=1)
    P = np.cov(returns)
    q = [0.0 for _ in range(K)]

    ret_cond = np.zeros((1, K)) + np.transpose(-1.0*mu)
    G = np.concatenate((ret_cond, -np.eye(K)), axis=0)
    h = [float(-m)] + [0.0 for _ in range(K)]

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


def mvo_shorts(returns, m):
    # K is the number of stocks
    returns = np.asmatrix(returns)
    K = returns.shape[0]

    # Compute the means of the returns
    mu = np.mean(returns, axis=1)

    P = np.cov(returns)
    q = [0.0 for _ in range(K)]

    G = np.transpose(-1.0*mu)

    h = [float(-m)]
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

def mvo(returns, m, short_sales=False):
    if short_sales:
        return mvo_shorts(returns, m)
    return mvo_no_shorts(returns, m)

if __name__ == '__main__':
    rets = {
        'Stocks': [
            26.81, -8.78, 22.69, 16.36, 12.36, -10.10, 23.94, 11.00, -8.47, 3.94, 14.30, 18.99,
            -14.69, -26.47, 37.23, 23.93, -7.16, 6.57, 18.61, 32.50, -4.92, 21.55, 22.56, 6.27,
            31.17, 18.67, 5.25, 16.61, 31.69, -3.10, 30.46, 7.62, 10.08, 1.32, 37.58, 22.96,
            33.36, 28.58, 21.04, -9.10, -11.89, -22.10, 28.68
            ],
        'Bonds': [
            2.20, 5.72, 1.79, 3.71, 0.93, 5.12, -2.86, 2.25, -5.63, 18.92, 11.24, 2.39, 3.29,
            4.00, 5.52, 15.56, 0.38, -1.26, -1.26, -2.48, 4.04, 44.28, 1.29, 15.29, 32.27,
            22.39, -3.03, 6.84, 18.54, 7.74, 19.36, 7.34, 13.06, -7.32, 25.94, 0.13, 12.02,
            14.45, -7.51, 17.22, 5.51, 15.15, 0.54
            ],
        'MM': [
            2.33, 2.93, 3.38, 3.85, 4.32, 5.40, 4.51, 6.02, 8.97, 4.90, 4.14, 5.33, 9.95, 8.53,
            5.20, 4.65, 6.56, 10.03, 13.78, 18.90, 12.37, 8.95, 9.47, 8.38, 8.27, 6.91, 6.77,
            8.76, 8.45, 7.31, 4.43, 2.92, 2.96, 5.45, 5.60, 5.29, 5.50, 4.68, 5.30, 6.40, 1.82,
            1.24, 0.98
        ]

    }

    r = []
    for k in sorted(rets.keys()):
        r.append([1.0+i/100 for i in rets[k]])

    means = np.mean(r, axis=1)
    steps = np.linspace(min(means), max(means), num=100)
    xs = map(lambda x: np.transpose(mvo_shorts(r, x))[0], steps)
    
    for i, row in enumerate(xs):
        print steps[i], map(lambda x: "%0.3f"%x, row), np.dot(means, row)

