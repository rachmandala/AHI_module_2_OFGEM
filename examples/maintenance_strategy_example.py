"""Maintenance strategy comparison example."""

from ahi_module_2.config.simulation_config import SimulationConfig
from ahi_module_2.data_models.asset_input import AssetInput
from ahi_module_2.data_models.condition_inputs import ConditionInputs
from ahi_module_2.data_models.financial_inputs import FinancialInputs
from ahi_module_2.simulation.maintenance_policy import AgeBasedPolicy, AHIBasedPolicy
from ahi_module_2.simulation.simulation_runner import SimulationRunner
from ahi_module_2.utils.enums import AssetClass

asset = AssetInput(
    asset_id="G001",
    asset_name="Generator",
    asset_class=AssetClass.GENERATOR,
    design_life=35.0,
    current_age=5.0,
    max_load=200.0,
    normal_load=160.0,
    distance_to_coast_factor=1.0,
    altitude_factor=1.0,
    temperature_factor=1.0,
    corrosive_factor=1.0,
    dust_factor=1.0,
)
financials = FinancialInputs(
    corrective_maintenance_cost=100_000.0,
    preventive_maintenance_cost=10_000.0,
    major_maintenance_cost=400_000.0,
)
conditions = ConditionInputs()
cfg = SimulationConfig(horizon=25, time_step=1.0)

for strategy, policy in [
    ("AHI-Based (≥5.5)", AHIBasedPolicy()),
    ("Age-Based (20yr)", AgeBasedPolicy(20.0)),
]:
    tracker = SimulationRunner(asset, financials, conditions, policy, cfg).run()
    print(f"{strategy}: TotEx = £{tracker.totex:,.0f}")
