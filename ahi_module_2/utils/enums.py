"""Enumerations for AHI Module 2."""

from enum import Enum


class AssetClass(str, Enum):
    """Supported industrial asset classes."""

    TURBINE = "turbine"
    GENERATOR = "generator"
    TRANSFORMER = "transformer"
    PUMP = "pump"
    COMPRESSOR = "compressor"
    BOILER = "boiler"
    BALANCE_OF_PLANT = "balance_of_plant"
    UTILITY = "utility"
    OTHER = "other"


class HealthBand(str, Enum):
    """Asset health band classifications."""

    GOOD = "good"           # AHI < 2.0
    FAIR = "fair"           # 2.0 <= AHI < 3.5
    POOR = "poor"           # 3.5 <= AHI < 5.0
    CRITICAL = "critical"   # AHI >= 5.0


class MaintenanceStrategy(str, Enum):
    """Maintenance strategy types."""

    AGE_BASED = "age_based"
    AHI_BASED = "ahi_based"


class ScenarioType(str, Enum):
    """Scenario types for forecasting."""

    ENVIRONMENTAL = "environmental"
    LOAD = "load"
    MAINTENANCE = "maintenance"
    DEGRADATION = "degradation"
