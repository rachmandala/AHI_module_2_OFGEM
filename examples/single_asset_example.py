"""Single asset simulation example."""

from ahi_module_2.config.simulation_config import SimulationConfig
from ahi_module_2.data_models.asset_input import AssetInput
from ahi_module_2.data_models.condition_inputs import ConditionInputs, ModifierInput
from ahi_module_2.data_models.financial_inputs import FinancialInputs
from ahi_module_2.reporting.health_report import HealthReport
from ahi_module_2.reporting.totex_report import TotExReport
from ahi_module_2.simulation.maintenance_policy import AHIBasedPolicy
from ahi_module_2.simulation.simulation_runner import SimulationRunner
from ahi_module_2.utils.enums import AssetClass

asset = AssetInput(
    asset_id="T001",
    asset_name="Gas Turbine GT-01",
    asset_class=AssetClass.TURBINE,
    design_life=30.0,
    current_age=12.0,
    max_load=150.0,
    normal_load=120.0,
    distance_to_coast_factor=1.1,
    altitude_factor=1.0,
    temperature_factor=1.3,
    corrosive_factor=1.0,
    dust_factor=1.0,
)

financials = FinancialInputs(
    corrective_maintenance_cost=75_000.0,
    preventive_maintenance_cost=8_000.0,
    major_maintenance_cost=250_000.0,
)

conditions = ConditionInputs(
    health_modifiers=[
        ModifierInput(name="vibration_level", weight=0.08, value=1.2),
        ModifierInput(name="oil_quality", weight=0.05, value=0.9),
    ],
    reliability_modifiers=[
        ModifierInput(name="insulation_condition", weight=0.04, value=1.1),
    ],
)

policy = AHIBasedPolicy(ahi_threshold=5.5)
sim_config = SimulationConfig(horizon=20, time_step=1.0)

runner = SimulationRunner(asset, financials, conditions, policy, sim_config)
tracker = runner.run()

health_entries = HealthReport.generate(tracker)
totex_entries = TotExReport.generate(tracker)

print("Year | AHI   | Band     | Cumulative TotEx")
print("-" * 50)
for h, t in zip(health_entries, totex_entries):
    print(f"{h.time:4.0f} | {h.ahi:5.3f} | {h.health_band.value:<8} | £{t.totex:,.0f}")
