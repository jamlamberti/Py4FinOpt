"""An optimizer for Sharpe Ratio"""

import numpy as np
import scipy.optimize
# from cvxopt import solvers, matrix
# solvers.options["show_progress"] = False
# solvers.options['maxiters'] = 500


def optimize_sharpe(returns, r_f=1):
    """
    Optimize the Sharpe Ratio of a portfolio,
    short_sales not working yet...
    """
    returns = np.asmatrix(returns)
    num_stocks, _ = returns.shape
    covar = np.cov(returns)
    means = np.mean(returns, axis=1)

    def transform_input(decision_vars):
        """Make sure the decision vars sum to 1"""
        mod_vars = list(decision_vars)
        mod_vars.append(1 - sum(mod_vars))
        return mod_vars

    def neg_sharpe(dec_vars):
        """Compute -1*sharpe_ratio"""
        dec_vars = np.asmatrix(transform_input(dec_vars)).T
        sharpe = (r_f - means.T * dec_vars) \
            / np.sqrt(dec_vars.T * covar * dec_vars)
        return sharpe

    sol = scipy.optimize.fmin(
        neg_sharpe,
        scipy.ones(num_stocks - 1, dtype=float) * 1. / num_stocks,
        disp=False,
        full_output=False)
    return transform_input(sol)
