# Methodology

This module implements the Asset Health Index (AHI) methodology based on:

> "Integrating complex asset health modelling techniques with continuous time simulation modelling:
> A practical tool" — Adolfo Crespo Márquez et al.

## Key Concepts

- **AHI** – Asset Health Index: current health state of an asset
- **FHI** – Future Health Index: projected health at a future age
- **PoF** – Probability of Failure: likelihood of asset failure in a given period

## Approach

1. Compute environmental (FFL) and load (FEL) factors
2. Derive expected asset life from design life adjusted by FFL × FEL
3. Calculate exponential aging rate beta
4. Apply health modifiers (HM) and reliability modifiers (RM) to base HI
5. Compute AHI and PoF
6. Simulate OpEx and CapEx across the asset lifecycle
7. Project FHI for forward planning
