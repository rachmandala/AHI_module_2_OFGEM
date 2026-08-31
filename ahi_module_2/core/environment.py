"""Environment engine – calculates the environmental factor FFL."""

from __future__ import annotations

from ahi_module_2.data_models.asset_input import AssetInput


class EnvironmentEngine:
    """Calculates the combined environmental factor for an asset.

    FFL = max(
        DistanceToCoastFactor,
        AltitudeFactor,
        TemperatureFactor,
        CorrosiveFactor,
        DustFactor,
    )
    """

    @staticmethod
    def calculate_environment_factor(asset: AssetInput) -> float:
        """Return FFL for the given asset."""
        return max(
            asset.distance_to_coast_factor,
            asset.altitude_factor,
            asset.temperature_factor,
            asset.corrosive_factor,
            asset.dust_factor,
        )
