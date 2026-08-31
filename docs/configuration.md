# Configuration Guide

## HealthConfig

| Field   | Default | Description               |
|---------|---------|---------------------------|
| hi_new  | 0.5     | Health index at new state |
| hi_eol  | 5.5     | Health index at end-of-life |

## SimulationConfig

| Field       | Default | Description              |
|-------------|---------|--------------------------|
| time_step   | 1.0     | Simulation step (years)  |
| horizon     | 40      | Simulation horizon (years)|
| random_seed | None    | Reproducibility seed     |

## FinancialConfig

| Field           | Default | Description        |
|-----------------|---------|--------------------|
| discount_rate   | 0.05    | Annual discount rate|
| currency_symbol | £       | Currency symbol    |
