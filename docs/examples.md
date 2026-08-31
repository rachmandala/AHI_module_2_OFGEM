# Examples

See the `examples/` directory for runnable scripts:

- `single_asset_example.py` – run a full simulation for one asset
- `portfolio_example.py` – multi-asset portfolio simulation
- `maintenance_strategy_example.py` – compare AHI vs age-based strategies
- `calibration_example.py` – calibrate modifier weights against historical data

## Quick Start

```python
from ahi_module_2 import AssetInput, FinancialInputs, ConditionInputs
from ahi_module_2 import AHIBasedPolicy, SimulationRunner
from ahi_module_2.config.simulation_config import SimulationConfig
from ahi_module_2.utils.enums import AssetClass

asset = AssetInput(
    asset_id="A001", asset_name="Pump", asset_class=AssetClass.PUMP,
    design_life=25.0, current_age=10.0, max_load=50.0, normal_load=40.0,
    distance_to_coast_factor=1.0, altitude_factor=1.0, temperature_factor=1.1,
    corrosive_factor=1.0, dust_factor=1.0,
)
financials = FinancialInputs(
    corrective_maintenance_cost=30000, preventive_maintenance_cost=3000,
    major_maintenance_cost=120000,
)
runner = SimulationRunner(asset, financials, ConditionInputs(), AHIBasedPolicy(),
                          SimulationConfig(horizon=20))
tracker = runner.run()
print(f"TotEx: £{tracker.totex:,.0f}")
```
