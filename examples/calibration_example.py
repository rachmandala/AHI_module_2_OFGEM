"""Calibration example."""

from ahi_module_2.calibration.calibration_runner import CalibrationRunner
from ahi_module_2.config.simulation_config import SimulationConfig
from ahi_module_2.data_models.asset_input import AssetInput
from ahi_module_2.data_models.condition_inputs import ConditionInputs, ModifierInput
from ahi_module_2.data_models.financial_inputs import FinancialInputs
from ahi_module_2.utils.enums import AssetClass

asset = AssetInput(
    asset_id="C001",
    asset_name="Compressor",
    asset_class=AssetClass.COMPRESSOR,
    design_life=25.0,
    current_age=8.0,
    max_load=80.0,
    normal_load=65.0,
    distance_to_coast_factor=1.0,
    altitude_factor=1.0,
    temperature_factor=1.2,
    corrosive_factor=1.1,
    dust_factor=1.0,
)
financials = FinancialInputs(
    corrective_maintenance_cost=40_000.0,
    preventive_maintenance_cost=4_000.0,
    major_maintenance_cost=150_000.0,
)
conditions = ConditionInputs(
    health_modifiers=[ModifierInput(name="vibration", weight=0.1, value=1.5)],
)
observed_opex = [6000.0, 6200.0, 6400.0, 6600.0, 6800.0]
cfg = SimulationConfig(horizon=5, time_step=1.0)

runner = CalibrationRunner(
    asset=asset,
    financials=financials,
    condition_inputs=conditions,
    observed_opex=observed_opex,
    observed_capex=[0.0] * 5,
    sim_config=cfg,
)
result = runner.run()
print(f"Optimised HM weights: {result.optimised_hm_weights}")
print(f"Optimised RM weights: {result.optimised_rm_weights}")
print(f"Final loss: {result.final_loss:.2f}")
