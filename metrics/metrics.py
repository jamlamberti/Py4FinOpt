import numpy as np
import scipy.stats

def arithmetic_mean(data, prev={}):
    return np.mean(data)

def geometric_mean(data, prev={}):
    # Might not want axis = None, but it does handle
    # the column vector vs row vector case
    return scipy.stats.gmean(data, axis=None)

def median(data, prev={}):
    return np.median(data)

def standard_deviation(data, prev={}):
    return np.std(data, ddof=1)

def quartiles(data, prev={}):
    return scipy.stats.scoreatpercentile(data, per=[25, 50, 75])

def interquartile_range(data, prev={}):
    if 'quartiles' in prev:
        q = prev['quartiles']
        return q[2]-q[0]
    q = quartiles(data, prev)
    return q[2]-q[0]

def downside_variance(data, prev={}):
    if 'arithmetic_mean' in prev:
        e_r = prev['arithmetic_mean']
    else:
        e_r = arthimetic_mean(data, prev)

    return np.mean(np.square(np.maximum(e_r-data, 0.0)))

def mean_absolute_deviation(data, prev={}):
    if 'arithmetic_mean' in prev:
        e_r = prev['arithmetic_mean']
    else:
        e_r = arthimetic_mean(data, prev)

    return np.mean(np.abs(e_r-data))


def describe(data):
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

def test():
    print describe(1.*np.array([range(1, 10)]))

if __name__ == '__main__':
    test()
