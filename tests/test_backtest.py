"""A collection of tests for backtest module"""
def test_gbm_model():
    """Test GBM Model"""
    from backtest.gbm_model import gbm_model
    steps = 100
    sim = gbm_model(100.0, 1.0, 105.0, steps)
    # Probably want to check mean and sigma
    assert len(sim) == steps

def test_sqrt_diffusion():
    """Test Square-Root Diffusion Model"""
    from backtest.sqrt_diffusion import sqrt_diffusion
    steps = 100
    sim = sqrt_diffusion(100.0, 1.0, 80.0, steps, mean_reversion=3.0)
    assert len(sim) == steps
