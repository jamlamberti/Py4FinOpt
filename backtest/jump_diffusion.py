"""Jump Diffusion Model"""
import numpy as np


def jump_diffusion(
        mu,
        sigma,
        start,
        steps,
        t_step=1.0,
        riskless_short_rate=0.05,
        delta=0.25,
        poisson_intensity=0.75):
    """Merton Jump Diffusion implementation"""
    jump_correction = poisson_intensity * (np.exp(mu + 0.5 * delta**2) - 1)
    prices = [start]

    for _ in range(steps - 1):
        prices.append(max(
            0.0,
            prices[-1] * (np.exp(
                (riskless_short_rate - jump_correction - 0.5 * sigma**2) *
                t_step +
                sigma * np.sqrt(t_step) * np.random.standard_normal()) +
                (np.exp(mu + delta * np.random.standard_normal()) - 1) *
                np.random.poisson(poisson_intensity * t_step))))
    return prices
