"""Test Suite for the models"""
from __future__ import print_function
import csv
from collections import defaultdict
import numpy as np
from optimization import mad, mvo, downside_var, sharpe_opt

# Might want to consider breaking this function out


def load_data(data_file='data/test_data.csv'):
    """Load the data for the test"""
    rets = defaultdict(list)
    with open(data_file, 'r') as f_handler:
        reader = csv.DictReader(f_handler)
        for row in reader:
            for ticker, value in row.items():
                rets[ticker].append(float(value))
    return rets


def smoke_test(optimizers):
    """smoke test for a list of optimizers"""
    rets = load_data()
    gross_returns = []
    # iterkeys isn't a Py3 function
    for k in sorted(rets.keys()):
        gross_returns.append([1.0 + i / 100 for i in rets[k]])

    means = np.mean(gross_returns, axis=1)
    steps = np.linspace(min(means), max(means), num=100)
    for shorting in [True, False]:
        for opt_model in optimizers:
            allocations = [
                np.transpose(opt_model(
                    gross_returns,
                    x,
                    short_sales=shorting))[0]
                for x in steps]

            shorting_test = []
            for i, row in enumerate(allocations):
                assert abs(steps[i] - np.dot(means, row)) < 1e-2
                if not shorting:
                    # pylint: disable=no-member
                    assert all([x >= -np.finfo(np.float32).eps for x in row])
                else:
                    shorting_test.append(all(
                        # pylint: disable=no-member
                        [x >= -np.finfo(np.float32).eps for x in row]))
                print(
                    steps[i],
                    ["%0.3f" % x for x in row],
                    np.dot(means, row))
            if shorting:
                print(shorting_test)
                assert not all(shorting_test)


def smoke_test2(optimizers):
    """A different smoke test for other models"""
    rets = load_data()
    gross_returns = []
    for k in sorted(rets.keys()):
        gross_returns.append([1.0 + i / 100 for i in rets[k]])
    means = np.mean(gross_returns, axis=1)
    steps = np.linspace(0.0, min(means), num=100)
    for opt_model in optimizers:
        allocations = [np.transpose(opt_model(gross_returns, x))
                       for x in steps]
        shorting_test = [all([x >= -np.finfo(np.float32).eps for x in row])
                         for row in allocations]
        assert not all(shorting_test)


def test_models():
    """Run over all the models"""
    smoke_test([
        mvo.optimize_mv,
        mad.optimize_mad,
        downside_var.optimize_downside_variance])
    # Sharpe doesn't support turning on and off short sales
    smoke_test2([sharpe_opt.optimize_sharpe])
