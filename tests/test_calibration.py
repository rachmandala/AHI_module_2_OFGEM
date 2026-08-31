"""Tests for calibration module."""

import pytest

from ahi_module_2.calibration.calibration_runner import CalibrationResult, CalibrationRunner
from ahi_module_2.calibration.loss_functions import squared_error_loss
from ahi_module_2.calibration.optimizer import Optimizer
from ahi_module_2.config.simulation_config import SimulationConfig
from ahi_module_2.data_models.condition_inputs import ConditionInputs, ModifierInput


class TestLossFunctions:
    def test_zero_error(self):
        loss = squared_error_loss([1.0, 2.0], [1.0, 2.0], [3.0], [3.0])
        assert loss == pytest.approx(0.0)

    def test_nonzero_error(self):
        loss = squared_error_loss([2.0], [1.0], [4.0], [3.0])
        assert loss == pytest.approx(2.0)  # 1^2 + 1^2


class TestOptimizer:
    def test_minimises_simple_quadratic(self):
        import numpy as np

        opt = Optimizer(method="Powell")
        result = opt.minimize(lambda x: (x[0] - 3.0) ** 2, np.array([0.0]))
        assert result[0] == pytest.approx(3.0, abs=1e-4)


class TestCalibrationRunner:
    def test_run_returns_calibration_result(self, basic_asset, basic_financials, with_modifiers):
        observed = [5500.0] * 5
        cfg = SimulationConfig(horizon=5, time_step=1.0)
        runner = CalibrationRunner(
            asset=basic_asset,
            financials=basic_financials,
            condition_inputs=with_modifiers,
            observed_opex=observed,
            observed_capex=[0.0] * 5,
            sim_config=cfg,
        )
        result = runner.run()
        assert isinstance(result, CalibrationResult)
        assert result.final_loss >= 0.0
        assert len(result.optimised_hm_weights) == 1
        assert len(result.optimised_rm_weights) == 1
