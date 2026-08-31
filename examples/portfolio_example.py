"""Portfolio simulation example."""

from ahi_module_2.config.simulation_config import SimulationConfig
from ahi_module_2.data_models.asset_input import AssetInput
from ahi_module_2.data_models.condition_inputs import ConditionInputs
from ahi_module_2.data_models.financial_inputs import FinancialInputs
from ahi_module_2.simulation.maintenance_policy import AHIBasedPolicy
from ahi_module_2.simulation.portfolio_runner import PortfolioRunner
from ahi_module_2.utils.enums import AssetClass

assets = [
    AssetInput(
        asset_id=f"P00{i}",
        asset_name=f"Pump {i}",
        asset_class=AssetClass.PUMP,
        design_life=25.0,
        current_age=float(i * 3),
        max_load=50.0,
        normal_load=40.0,
        distance_to_coast_factor=1.0,
        altitude_factor=1.0,
        temperature_factor=1.1,
        corrosive_factor=1.0,
        dust_factor=1.0,
    )
    for i in range(1, 4)
]

financials = FinancialInputs(
    corrective_maintenance_cost=30_000.0,
    preventive_maintenance_cost=3_000.0,
    major_maintenance_cost=120_000.0,
)
conditions = ConditionInputs()
policy = AHIBasedPolicy()
cfg = SimulationConfig(horizon=15, time_step=1.0)

runner = PortfolioRunner(sim_config=cfg)
results = runner.run([(a, financials, conditions, policy) for a in assets])

total = PortfolioRunner.aggregate_totex(results)
print(f"Portfolio TotEx over 15 years: £{total:,.0f}")
