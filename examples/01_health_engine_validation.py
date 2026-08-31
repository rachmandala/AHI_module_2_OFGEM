from ahi_module_2.config.health_config import HealthConfig
from ahi_module_2.core.health_engine import HealthEngine
from ahi_module_2.data_models.asset_input import AssetInput
from ahi_module_2.utils.enums import AssetClass

cfg = HealthConfig()

engine = HealthEngine(cfg)

asset = AssetInput(
    asset_id="GT01",
    asset_name="Gas Turbine 01",
    asset_class=AssetClass.TURBINE,

    design_life=30,
    current_age=15,

    max_load=100,
    normal_load=85,

    distance_to_coast_factor=1.2,
    altitude_factor=1.0,
    temperature_factor=1.1,
    corrosive_factor=1.0,
    dust_factor=1.0,
)

ffl = max(
    asset.distance_to_coast_factor,
    asset.altitude_factor,
    asset.temperature_factor,
    asset.corrosive_factor,
    asset.dust_factor,
)

life = engine.calculate_expected_life(
    design_life=asset.design_life,
    ffl=ffl,
    normal_load=asset.normal_load,
    max_load=asset.max_load
)

beta = engine.calculate_aging_rate(life)

hi = engine.calculate_base_health(
    age=asset.current_age,
    beta=beta
)

ahi = engine.calculate_ahi(
    hi=hi,
    hm=0.1,
    rm=0.05
)

print("\nAHI MODULE 2 VALIDATION")
print("=" * 50)
print(f"FFL           : {ffl:.4f}")
print(f"Expected Life : {life:.4f}")
print(f"Beta          : {beta:.6f}")
print(f"HI            : {hi:.4f}")
print(f"AHI           : {ahi:.4f}")