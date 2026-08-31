# AHI Module 2

**Asset Health Index – Simulation-Based Methodology**

[![CI](https://github.com/rachmandala/AHI_module_2_OFGEM/actions/workflows/ci.yml/badge.svg)](https://github.com/rachmandala/AHI_module_2_OFGEM/actions/workflows/ci.yml)

---

## Project Overview

AHI Module 2 is a production-grade Python library that implements the **Asset Health Index (AHI)** methodology described in:

> *"Integrating complex asset health modelling techniques with continuous time simulation modelling: A practical tool"*  
> Adolfo Crespo Márquez et al.

The module provides an alternative and extended implementation to AHI Module 1, with a focus on **simulation-based asset lifecycle management** for industrial assets such as turbines, generators, transformers, pumps, compressors, boilers, balance-of-plant equipment, and utility assets.

---

## Engineering Background

Asset health degradation is modelled as an exponential process driven by:

- **Environmental stressors** (coast proximity, altitude, temperature, corrosion, dust)
- **Operational load** (ratio of normal to maximum permissible load)
- **Condition modifiers** (health and reliability modifiers from condition monitoring)

---

## Mathematical Equations

### Environmental Factor
```
FFL = max(DistanceToCoastFactor, AltitudeFactor, TemperatureFactor, CorrosiveFactor, DustFactor)
```

### Load Factor
```
FEL = NormalLoad / MaximumPermissibleLoad
```

### Expected Asset Life
```
ExpectedLife = DesignLife / (FFL × FEL)
```

### Aging Rate
```
β = ln(HI_EOL / HI_NEW) / ExpectedLife      [HI_NEW=0.5, HI_EOL=5.5]
```

### Base Health Index
```
HI(t) = 0.5 × exp(β × age)
```

### Health & Reliability Modifiers
```
HM = Σ(weight_i × input_i)
RM = Σ(weight_i × input_i)
```

### Asset Health Index
```
AHI = HI × exp(HM + RM)
```

### Probability of Failure
```
H = max(4, AHI)
PoF = K × (1 + C·H + (C·H)²/2 + (C·H)³/6)
```

### Expenditure
```
OpEx  = PoF × CorrectiveMaintenanceCost + PreventiveMaintenanceCost
CapEx = MajorMaintenanceTrigger × MajorMaintenanceCost
TotEx = ΣOpEx + ΣCapEx
```

### Future Health Index (FHI)
```
β_corrected = ln(CurrentAHI / 0.5) / CurrentAge
FHI = 0.5 × exp(β_corrected × future_age)
```

---

## Architecture

```
ahi_module_2/
├── config/          – Pydantic v2 configuration models
├── data_models/     – Input data models (AssetInput, FinancialInputs, …)
├── core/            – EnvironmentEngine, HealthEngine, ReliabilityEngine,
│                      MaintenanceEngine, CostEngine
├── forecasting/     – FutureHealthEngine, ScenarioEngine
├── simulation/      – MaintenancePolicy, SimulationRunner, PortfolioRunner
├── calibration/     – Optimizer, CalibrationRunner (scipy.optimize)
├── reporting/       – HealthReport, RiskReport, MaintenanceReport, TotExReport
├── validation/      – Input, health, and calibration validators
└── utils/           – Constants, enums, helpers
```

---

## Installation

```bash
pip install -e ".[dev]"
```

---

## Usage Examples

### Single Asset Simulation

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

### Portfolio Simulation

```python
from ahi_module_2.simulation.portfolio_runner import PortfolioRunner
portfolio = PortfolioRunner(sim_config=SimulationConfig(horizon=20))
results = portfolio.run([(asset, financials, conditions, policy) for ...])
print(f"Portfolio TotEx: £{PortfolioRunner.aggregate_totex(results):,.0f}")
```

### Calibration

```python
from ahi_module_2.calibration.calibration_runner import CalibrationRunner
runner = CalibrationRunner(asset, financials, conditions, observed_opex, observed_capex)
result = runner.run()
print(result.optimised_hm_weights)
```

---

## Testing

```bash
pytest
```

Target coverage: ≥90%

---

## Roadmap

- Asset Criticality Index integration
- Consequence of Failure modelling
- Risk Matrix
- System / Plant / Portfolio Health aggregation
- Digital Twin integration
- ISO 55000 alignment
- Reliability Centered Maintenance (RCM) integration
- Machine Learning assisted health prediction
