"""Simulation runner for a single asset."""

from __future__ import annotations

from ahi_module_2.config.health_config import HealthConfig
from ahi_module_2.config.simulation_config import SimulationConfig
from ahi_module_2.core.cost_engine import CostEngine
from ahi_module_2.core.environment import EnvironmentEngine
from ahi_module_2.core.health_engine import HealthEngine
from ahi_module_2.core.reliability_engine import ReliabilityEngine
from ahi_module_2.data_models.asset_input import AssetInput
from ahi_module_2.data_models.condition_inputs import ConditionInputs
from ahi_module_2.data_models.financial_inputs import FinancialInputs
from ahi_module_2.forecasting.future_health import FutureHealthEngine
from ahi_module_2.simulation.maintenance_policy import MaintenancePolicy
from ahi_module_2.simulation.state_tracker import SimulationStep, StateTracker


class SimulationRunner:
    """Runs a time-stepped simulation for a single asset."""

    def __init__(
        self,
        asset: AssetInput,
        financials: FinancialInputs,
        condition_inputs: ConditionInputs,
        policy: MaintenancePolicy,
        sim_config: SimulationConfig | None = None,
        health_config: HealthConfig | None = None,
    ) -> None:
        self._asset = asset
        self._financials = financials
        self._condition_inputs = condition_inputs
        self._policy = policy
        self._sim_cfg = sim_config or SimulationConfig()
        self._health_cfg = health_config or HealthConfig()

        self._env_engine = EnvironmentEngine()
        self._health_engine = HealthEngine(self._health_cfg)
        self._reliability_engine = ReliabilityEngine()
        self._cost_engine = CostEngine()
        self._fhi_engine = FutureHealthEngine(self._health_cfg)

    def run(self) -> StateTracker:
        """Execute the simulation and return a StateTracker."""
        tracker = StateTracker()

        ffl = self._env_engine.calculate_environment_factor(self._asset)
        expected_life = self._health_engine.calculate_expected_life(
            self._asset.design_life,
            ffl,
            self._asset.normal_load,
            self._asset.max_load,
        )
        beta = self._health_engine.calculate_aging_rate(expected_life)

        hm = self._health_engine.calculate_health_modifier(self._condition_inputs.health_modifiers)
        rm = self._health_engine.calculate_reliability_modifier(
            self._condition_inputs.reliability_modifiers
        )

        dt = self._sim_cfg.time_step
        # age_offset tracks the simulation time at which the most recent maintenance reset occurred.
        # Effective age at step i is: (i * dt) - age_offset + initial_age
        age_offset = 0.0

        for step_idx in range(self._sim_cfg.horizon):
            sim_time = step_idx * dt
            age_at_step = self._asset.current_age + sim_time - age_offset

            hi = self._health_engine.calculate_base_health(age_at_step, beta)
            ahi = self._health_engine.calculate_ahi(hi, hm, rm)
            pof = self._reliability_engine.calculate_probability_of_failure(ahi)

            maintenance = self._policy.should_trigger(age_at_step, ahi)
            if maintenance:
                # Reset effective age to 0 by advancing the offset to current sim_time + initial_age
                age_offset = sim_time + self._asset.current_age
                age_at_step = 0.0
                hi = self._health_engine.calculate_base_health(0.0, beta)
                ahi = self._health_engine.calculate_ahi(hi, hm, rm)
                pof = self._reliability_engine.calculate_probability_of_failure(ahi)

            opex = self._cost_engine.calculate_opex(pof, self._financials)
            capex = self._cost_engine.calculate_capex(maintenance, self._financials)
            totex = self._cost_engine.calculate_totex(
                tracker.accumulated_opex + opex,
                tracker.accumulated_capex + capex,
            )
            fhi = self._fhi_engine.project_future_health(
                ahi,
                max(age_at_step, 0.01),
                age_at_step + expected_life,
            )

            tracker.record(
                SimulationStep(
                    time=sim_time,
                    age=age_at_step,
                    hi=hi,
                    ahi=ahi,
                    pof=pof,
                    opex=opex,
                    capex=capex,
                    totex=totex,
                    fhi=fhi,
                    maintenance_triggered=maintenance,
                )
            )

        return tracker
