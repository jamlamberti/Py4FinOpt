"""
Useful for computing a bunch of metrics over
time-series data
"""
from __future__ import print_function
import numpy as np
import scipy.stats

def arithmetic_mean(data, prev=None):
    """Computes the arithmetic mean of the data"""
    # pylint: disable=unused-argument
    return np.mean(data)

def geometric_mean(data, prev=None):
    """Computes the geometric mean of the data"""
    # pylint: disable=unused-argument
    # Might not want axis = None, but it does handle
    # the column vector vs row vector case
    return scipy.stats.gmean(data, axis=None)

def median(data, prev=None):
    """Computes the median of the data"""
    # pylint: disable=unused-argument
    return np.median(data)

def standard_deviation(data, prev=None):
    """Computes the standard deviation with 1 degree of freedom"""
    # pylint: disable=unused-argument
    return np.std(data, ddof=1)

def quartiles(data, prev=None):
    """Computes the 1st, 2nd and 3rd quartiles"""
    # pylint: disable=unused-argument
    return scipy.stats.scoreatpercentile(data, per=[25, 50, 75])

def interquartile_range(data, prev=None):
    """Computes the IQR (q3-q1)"""
    if prev is None:
        prev = {}

    if 'quartiles' in prev:
        quarts = prev['quartiles']
        return quarts[2]-quarts[0]

    quarts = quartiles(data, prev)
    return quarts[2]-quarts[0]

def downside_variance(data, prev=None):
    """
    Computes the downside variance:
        (1/T)*sum(max(0.0, e_r-x_t)^2)
    where:
        e_r is the expected return (arithmetic mean)
        x_t is the value at t
    """
    if prev is None:
        prev = {}

    if 'arithmetic_mean' in prev:
        e_r = prev['arithmetic_mean']
    else:
        e_r = arithmetic_mean(data, prev)
    # Can't seem to pick up certain dynamic functions in np
    # pylint: disable=no-member
    return np.mean(np.square(np.maximum(e_r-data, 0.0)))

def mean_absolute_deviation(data, prev=None):
    """
    Computes Mean Absolute Deviation (MAD):
        (1/T)*sum(|e_r - x_t|)
    where:
        e_r is the expected return
        x_t is the value at t
    Effectively standard deviation but with a L1 Norm
    """
    if prev is None:
        prev = {}

    if 'arithmetic_mean' in prev:
        e_r = prev['arithmetic_mean']
    else:
        e_r = arithmetic_mean(data, prev)

    return np.mean(np.abs(e_r-data))


def describe(data):
    """Describes a time-series dataset by computing all metrics over it"""
    result = {}
    funcs = [
        arithmetic_mean,
        geometric_mean,
        median,
        standard_deviation,
        quartiles,
        interquartile_range,
        downside_variance,
        mean_absolute_deviation,
    ]

    for func in funcs:
        result[func.__name__] = func(data, result)

    return result

def smoke_test():
    """A simple smoke test"""
    print(describe(1.*np.array([range(1, 10)])))

if __name__ == '__main__':
    smoke_test()
