"""Health value validation."""

from __future__ import annotations

from ahi_module_2.utils.constants import HI_EOL, HI_NEW


class HealthValidationError(ValueError):
    pass


def validate_ahi(ahi: float) -> None:
    """Raise HealthValidationError if AHI is outside expected range."""
    if ahi < 0:
        raise HealthValidationError(f"AHI must be non-negative, got {ahi}")
    if ahi > HI_EOL * 10:
        raise HealthValidationError(f"AHI ({ahi}) is unexpectedly large (> {HI_EOL * 10}).")
