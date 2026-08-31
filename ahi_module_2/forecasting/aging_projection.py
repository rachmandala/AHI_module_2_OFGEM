"""Aging projection helpers."""

from __future__ import annotations

import math

from ahi_module_2.config.health_config import HealthConfig


def calculate_corrected_aging_rate(
    current_ahi: float,
    current_age: float,
    config: HealthConfig | None = None,
) -> float:
    """Return beta_corrected = ln(current_ahi / HI_NEW) / current_age.

    Returns 0.0 if current_age is 0 to avoid division by zero.
    """
    cfg = config or HealthConfig()
    if current_age <= 0:
        return 0.0
    ratio = current_ahi / cfg.hi_new
    if ratio <= 0:
        return 0.0
    return math.log(ratio) / current_age
