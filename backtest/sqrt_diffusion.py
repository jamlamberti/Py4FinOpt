"""square-root diffusion"""
import numpy as np


def sqrt_diffusion(mu, sigma, start, steps, mean_reversion=2.0, t_step=1.0):
    """Sqrt diffusion implementation"""
    prev = start
    prices = [start]
    for _ in range(steps - 1):
        prev = (prev + mean_reversion * (mu - prices[-1]) * t_step +
                sigma * np.sqrt(prices[-1] * t_step) * np.random.randn())
        prices.append(max(0.0, prev))
    return prices
