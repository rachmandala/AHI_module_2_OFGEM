"""
03_lifecycle_simulation.py

First dynamic lifecycle simulation for AHI Module 2.

Purpose:
- Simulate asset degradation over time
- Calculate HI
- Calculate AHI
- Trigger maintenance
- Reset asset age
- Continue simulation

This validates the dynamic behavior of the OFGEM-style model.
"""

from ahi_module_2.config.health_config import HealthConfig
from ahi_module_2.core.health_engine import HealthEngine
from ahi_module_2.core.reliability_engine import ReliabilityEngine
from ahi_module_2.core.maintenance_engine import MaintenanceEngine

from ahi_module_2.data_models.asset_input import AssetInput
from ahi_module_2.utils.enums import AssetClass


# ======================================================
# CONFIGURATION
# ======================================================

SIMULATION_HORIZON = 80  # years
TIME_STEP = 1            # years

AHI_THRESHOLD = 5.5

HM_SCORE = 0.0
RM_SCORE = 0.0


# ======================================================
# INITIALIZE ENGINES
# ======================================================

health_engine = HealthEngine(HealthConfig())

reliability_engine = ReliabilityEngine()

maintenance_engine = MaintenanceEngine()


# ======================================================
# ASSET DEFINITION
# ======================================================

asset = AssetInput(
    asset_id="GT01",
    asset_name="Gas Turbine 01",
    asset_class=AssetClass.TURBINE,

    design_life=30,
    current_age=0,

    max_load=100,
    normal_load=85,

    distance_to_coast_factor=1.2,
    altitude_factor=1.0,
    temperature_factor=1.1,
    corrosive_factor=1.0,
    dust_factor=1.0,
)


# ======================================================
# PRE-CALCULATE CONSTANTS
# ======================================================

ffl = max(
    asset.distance_to_coast_factor,
    asset.altitude_factor,
    asset.temperature_factor,
    asset.corrosive_factor,
    asset.dust_factor
)

expected_life = health_engine.calculate_expected_life(
    design_life=asset.design_life,
    ffl=ffl,
    normal_load=asset.normal_load,
    max_load=asset.max_load
)

beta = health_engine.calculate_aging_rate(
    expected_life
)


# ======================================================
# SIMULATION
# ======================================================

print()
print("LIFECYCLE SIMULATION")
print("=" * 90)

header = (
    f"{'Year':<8}"
    f"{'Age':<8}"
    f"{'HI':<12}"
    f"{'AHI':<12}"
    f"{'PoF':<12}"
    f"{'Maint?':<10}"
)

print(header)
print("-" * len(header))

effective_age = 0.0

maintenance_count = 0


for year in range(0, SIMULATION_HORIZON + 1):

    hi = health_engine.calculate_base_health(
        age=effective_age,
        beta=beta
    )

    ahi = health_engine.calculate_ahi(
        hi=hi,
        hm=HM_SCORE,
        rm=RM_SCORE
    )

    pof = reliability_engine.calculate_probability_of_failure(
        ahi
    )

    maintenance_trigger = (
        maintenance_engine.determine_major_maintenance_trigger(
            current_age=effective_age,
            current_ahi=ahi,
            ahi_threshold=AHI_THRESHOLD
        )
    )

    print(
        f"{year:<8}"
        f"{effective_age:<8.1f}"
        f"{hi:<12.4f}"
        f"{ahi:<12.4f}"
        f"{pof:<12.6f}"
        f"{str(maintenance_trigger):<10}"
    )

    if maintenance_trigger:

        maintenance_count += 1

        effective_age = (
            maintenance_engine.perform_major_maintenance_reset()
        )

    else:

        effective_age += TIME_STEP


print()
print("=" * 90)
print("SIMULATION SUMMARY")
print("=" * 90)

print(f"Expected Life      : {expected_life:.2f} years")
print(f"Aging Rate (beta)  : {beta:.6f}")
print(f"Simulation Horizon : {SIMULATION_HORIZON} years")
print(f"Maintenance Count  : {maintenance_count}")