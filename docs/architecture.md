# Architecture

## Module Structure

```
ahi_module_2/
├── config/          – Pydantic configuration models
├── data_models/     – Input data models
├── core/            – Core calculation engines
├── forecasting/     – Future Health Index and scenario analysis
├── simulation/      – Maintenance policy and simulation runner
├── calibration/     – Optimizer and calibration runner
├── reporting/       – Report generators
├── validation/      – Input and output validation
└── utils/           – Constants, enums, helpers
```

## Dependency Graph

```
data_models → core → simulation → reporting
                   ↗
forecasting →
calibration →
```

## Design Principles

- SOLID: Each engine has a single responsibility
- Dependency injection: engines receive configs and data models
- Pydantic v2 for all inputs
- Full type hints throughout
