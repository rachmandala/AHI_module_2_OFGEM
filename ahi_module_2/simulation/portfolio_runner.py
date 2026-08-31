"""Portfolio runner – aggregates simulation across multiple assets."""

from __future__ import annotations

from ahi_module_2.config.health_config import HealthConfig
from ahi_module_2.config.simulation_config import SimulationConfig
from ahi_module_2.data_models.asset_input import AssetInput
from ahi_module_2.data_models.condition_inputs import ConditionInputs
from ahi_module_2.data_models.financial_inputs import FinancialInputs
from ahi_module_2.simulation.maintenance_policy import MaintenancePolicy
from ahi_module_2.simulation.simulation_runner import SimulationRunner
from ahi_module_2.simulation.state_tracker import StateTracker


class PortfolioRunner:
    """Runs individual asset simulations and aggregates portfolio results."""

    def __init__(
        self,
        sim_config: SimulationConfig | None = None,
        health_config: HealthConfig | None = None,
    ) -> None:
        self._sim_cfg = sim_config or SimulationConfig()
        self._health_cfg = health_config or HealthConfig()

    def run(
        self,
        assets: list[tuple[AssetInput, FinancialInputs, ConditionInputs, MaintenancePolicy]],
    ) -> dict[str, StateTracker]:
        """Run simulation for each asset and return results keyed by asset_id."""
        results: dict[str, StateTracker] = {}
        for asset, financials, conditions, policy in assets:
            runner = SimulationRunner(
                asset=asset,
                financials=financials,
                condition_inputs=conditions,
                policy=policy,
                sim_config=self._sim_cfg,
                health_config=self._health_cfg,
            )
            results[asset.asset_id] = runner.run()
        return results

    @staticmethod
    def aggregate_totex(results: dict[str, StateTracker]) -> float:
        """Return sum of TotEx across all assets in the portfolio."""
        return sum(tracker.totex for tracker in results.values())
