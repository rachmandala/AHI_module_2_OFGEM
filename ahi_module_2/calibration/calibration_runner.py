"""High-level calibration runner."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from ahi_module_2.calibration.loss_functions import squared_error_loss
from ahi_module_2.calibration.optimizer import Optimizer
from ahi_module_2.config.health_config import HealthConfig
from ahi_module_2.config.simulation_config import SimulationConfig
from ahi_module_2.data_models.asset_input import AssetInput
from ahi_module_2.data_models.condition_inputs import ConditionInputs, ModifierInput
from ahi_module_2.data_models.financial_inputs import FinancialInputs
from ahi_module_2.data_models.maintenance_history import MaintenanceHistory
from ahi_module_2.data_models.operating_history import OperatingHistory
from ahi_module_2.simulation.maintenance_policy import AHIBasedPolicy
from ahi_module_2.simulation.simulation_runner import SimulationRunner


@dataclass
class CalibrationResult:
    """Outcome of a calibration run."""

    optimised_hm_weights: list[float]
    optimised_rm_weights: list[float]
    final_loss: float


class CalibrationRunner:
    """Calibrates health and reliability modifier weights against historical data.

    Modifies HM and RM weights to minimise:
        sum(OpExError^2 + CapExError^2)
    """

    def __init__(
        self,
        asset: AssetInput,
        financials: FinancialInputs,
        condition_inputs: ConditionInputs,
        observed_opex: list[float],
        observed_capex: list[float],
        operating_history: OperatingHistory | None = None,
        maintenance_history: MaintenanceHistory | None = None,
        sim_config: SimulationConfig | None = None,
        health_config: HealthConfig | None = None,
        optimizer: Optimizer | None = None,
    ) -> None:
        self._asset = asset
        self._financials = financials
        self._condition_inputs = condition_inputs
        self._observed_opex = observed_opex
        self._observed_capex = observed_capex
        self._sim_cfg = sim_config or SimulationConfig(horizon=len(observed_opex))
        self._health_cfg = health_config or HealthConfig()
        self._optimizer = optimizer or Optimizer()

    def _build_condition_inputs(
        self, hm_weights: list[float], rm_weights: list[float]
    ) -> ConditionInputs:
        hm_inputs = [
            ModifierInput(
                name=m.name,
                weight=hm_weights[i] if i < len(hm_weights) else m.weight,
                value=m.value,
            )
            for i, m in enumerate(self._condition_inputs.health_modifiers)
        ]
        rm_inputs = [
            ModifierInput(
                name=m.name,
                weight=rm_weights[i] if i < len(rm_weights) else m.weight,
                value=m.value,
            )
            for i, m in enumerate(self._condition_inputs.reliability_modifiers)
        ]
        return ConditionInputs(health_modifiers=hm_inputs, reliability_modifiers=rm_inputs)

    def _objective(self, params: np.ndarray) -> float:
        n_hm = len(self._condition_inputs.health_modifiers)
        hm_weights = list(params[:n_hm])
        rm_weights = list(params[n_hm:])

        conditions = self._build_condition_inputs(hm_weights, rm_weights)
        policy = AHIBasedPolicy()
        runner = SimulationRunner(
            asset=self._asset,
            financials=self._financials,
            condition_inputs=conditions,
            policy=policy,
            sim_config=self._sim_cfg,
            health_config=self._health_cfg,
        )
        tracker = runner.run()

        pred_opex = [s.opex for s in tracker.steps[: len(self._observed_opex)]]
        pred_capex = [s.capex for s in tracker.steps[: len(self._observed_capex)]]

        return squared_error_loss(pred_opex, self._observed_opex, pred_capex, self._observed_capex)

    def run(self) -> CalibrationResult:
        """Execute calibration and return optimised weights."""
        n_hm = len(self._condition_inputs.health_modifiers)
        n_rm = len(self._condition_inputs.reliability_modifiers)
        initial = np.array(
            [m.weight for m in self._condition_inputs.health_modifiers]
            + [m.weight for m in self._condition_inputs.reliability_modifiers],
            dtype=float,
        )
        optimised = self._optimizer.minimize(self._objective, initial)
        final_loss = self._objective(optimised)
        return CalibrationResult(
            optimised_hm_weights=list(optimised[:n_hm]),
            optimised_rm_weights=list(optimised[n_hm:]),
            final_loss=final_loss,
        )
