from ahi_module_2.data_models.asset_input import AssetInput
from ahi_module_2.core.health_engine import HealthEngine

asset = AssetInput(
    asset_id="GT01",
    design_life=100000,
    current_age=50000,
    max_load=100,
    normal_load=85,
    distance_to_coast_factor=1.2,
    altitude_factor=1.0,
    temperature_factor=1.1,
    corrosive_factor=1.0,
    dust_factor=1.0
)

life = HealthEngine.expected_life(asset)

beta = HealthEngine.aging_rate(asset)

hi = HealthEngine.base_health(asset)

ahi = HealthEngine.calculate_ahi(
    asset,
    hm_score=0.1,
    rm_score=0.05
)

print("\nRESULTS")
print("-" * 40)
print(f"Expected Life : {life}")
print(f"Beta          : {beta}")
print(f"HI            : {hi}")
print(f"AHI           : {ahi}")