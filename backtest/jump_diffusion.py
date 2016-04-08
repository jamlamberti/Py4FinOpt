"""Jump Diffusion Model"""
import numpy as np
import numpy.random as npr


def jump_diffusion(
        mu,
        sigma,
        start,
        steps,
        t_step=1.0,
        riskless_sr=0.05,
        delta=0.25,
        poisson_intensity=0.75):
    """Merton Jump Diffusion implementation"""
    jump_correction = poisson_intensity * (np.exp(mu + 0.5 * delta**2) - 1)
    prices = [start]
    # Pylint and pep8 disagree on continuation indents here
    # I am choosing pep8 over pylint here
    # pylint: disable=bad-continuation
    for _ in range(steps - 1):
        prices.append(max(
            0.0,
            prices[-1] * (np.exp(
                t_step * (riskless_sr - jump_correction - 0.5 * sigma**2) +
                sigma * np.sqrt(t_step) * npr.standard_normal()) +
                (np.exp(mu + delta * npr.standard_normal()) - 1) *
                npr.poisson(poisson_intensity * t_step))))
    return prices
