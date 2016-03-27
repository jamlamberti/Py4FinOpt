"""Collection of tests for metrics"""
import numpy as np
from metrics import metrics


def test_metrics():
    """A simple smoke test"""
    res = metrics.describe(1. * np.array([range(1, 10)]))
    assert res['arithmetic_mean'] == 5.0
    assert abs(res['downside_variance']-3.33333) < 0.00001
    assert res['quartiles'] == [3.0, 5.0, 7.0]
    assert res['interquartile_range'] == 4.0
    assert res['median'] == 5.0
    assert abs(res['standard_deviation'] - 2.7386) < 0.0001
    assert abs(res['mean_absolute_deviation']-2.22222) < 0.00001
    assert abs(res['geometric_mean']-4.147166) < 0.00001
