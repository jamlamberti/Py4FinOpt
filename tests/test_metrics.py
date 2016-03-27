"""Collection of tests for metrics"""
import numpy as np
from metrics import metrics


def test_metrics():
    """A simple smoke test"""
    data = 1. * np.array([range(1, 10)])
    res = metrics.describe(data)
    assert res['arithmetic_mean'] == 5.0
    assert abs(res['downside_variance']-3.33333) < 0.00001
    assert all([
        res['quartiles'][i] == v for i, v in enumerate([3.0, 5.0, 7.0])])
    assert res['interquartile_range'] == 4.0
    assert res['median'] == 5.0
    assert abs(res['standard_deviation'] - 2.7386) < 0.0001
    assert abs(res['mean_absolute_deviation']-2.22222) < 0.00001
    assert abs(res['geometric_mean']-4.147166) < 0.00001

    funcs = [
        metrics.arithmetic_mean, metrics.geometric_mean, metrics.median,
        metrics.standard_deviation, metrics.quartiles,
        metrics.interquartile_range, metrics.downside_variance,
        metrics.mean_absolute_deviation
    ]

    for func in funcs:
        assert func(data) == res[func.__name__]
