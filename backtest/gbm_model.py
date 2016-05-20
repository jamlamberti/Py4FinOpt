"""A simple geometric Brownian Motion Model"""
import numpy as np


def gbm_model(mu, sigma, start, steps, t_step=1.0):
    """Implementation of the model"""
    prices = [start]
    for _ in range(steps - 1):
        prices.append(prices[-1] *
                      (1.0 + mu * t_step +
                       sigma * np.random.randn() * np.sqrt(t_step)))
    return prices
