"""General-purpose helper utilities for AHI Module 2."""

from __future__ import annotations

import math

from ahi_module_2.utils.enums import HealthBand


def classify_health_band(ahi: float) -> HealthBand:
    """Return the HealthBand for a given AHI value."""
    if ahi < 2.0:
        return HealthBand.GOOD
    elif ahi < 3.5:
        return HealthBand.FAIR
    elif ahi < 5.0:
        return HealthBand.POOR
    return HealthBand.CRITICAL


def safe_log(value: float, fallback: float = 0.0) -> float:
    """Return natural log of *value*, or *fallback* if value <= 0."""
    if value <= 0:
        return fallback
    return math.log(value)


def clamp(value: float, lo: float, hi: float) -> float:
    """Clamp *value* to the closed interval [lo, hi]."""
    return max(lo, min(hi, value))
