"""Input validation utilities."""

from __future__ import annotations

from ahi_module_2.data_models.asset_input import AssetInput


class InputValidationError(ValueError):
    pass


def validate_asset_input(asset: AssetInput) -> None:
    """Raise InputValidationError if the asset has invalid field combinations."""
    if asset.current_age > asset.design_life * 2:
        raise InputValidationError(
            f"current_age ({asset.current_age}) exceeds twice the design_life ({asset.design_life})."
        )
