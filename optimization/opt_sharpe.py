import numpy as np
from cvxopt import solvers, matrix

solvers.options["show_progress"] = False

def opt_sharpe(returns, r_f=1, short_sales=False):
    returns = np.asmatrix(returns)
    N, T = returns.shape
    Q = np.cov(returns)
    means = np.mean(returns, axis=1)
    last_x = (1./N)*np.ones((N, 1))
    def f(x_mat=None, z=None):
        if x_mat is None:
            x0 = (1./N)*np.ones((N, 1))
            return 0, matrix(x0)
        else:
            x = np.asmatrix(x_mat)
            last_x = x
            sharpe = (r_f-np.transpose(means)*x)/np.sqrt(np.transpose(x)*Q*x)
            # Needs more...
            dF = np.transpose(means*(1.0/np.sqrt(np.transpose(x)*Q*x))) + \
                (r_f-np.transpose(means)*x)*(-1/(2*float(np.transpose(x)*Q*x)**(2.0/3)))*np.transpose(x)*(Q + np.transpose(Q))
            if z is None:
                # Return val, d(f)/dx
                return sharpe, matrix(dF)
            else:
                # Return val, d(f)/dx, and hessian
                H = means*(-1/(float(x.T*Q*x)**(2/3)))*x.T*(Q.T + Q) + \
                    (r_f - means.T*x)*(-1/(2*float(x.T*Q*x)**(2/3)))+(Q.T + Q).T + \
                    (Q.T + Q).T*(1/(4*float(x.T*Q*x)**(4/3)))
                return sharpe, matrix(dF), matrix(H)


    G = np.zeros((1, N))
    h = [0.0]

    A = np.ones((1, N))
    b = [1.0]
    solvers.options['maxiters'] = 500
    sol = solvers.cp(
        f,
        G=matrix(G),
        h=matrix(h),
        A=matrix(A),
        b=matrix(b),
    )
    print sol['status']
    return sol['x']


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
    steps = np.linspace(0.0, 1.0, num=50)
    xs = map(lambda x: np.transpose(opt_sharpe(r, x))[0], steps)
    for i, row in enumerate(xs):
        print "Rf:", steps[i], map(lambda x: "%0.3f"%x, row)

