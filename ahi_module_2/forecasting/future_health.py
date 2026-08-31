"""Future Health Index projection."""

from __future__ import annotations

import math

from ahi_module_2.config.health_config import HealthConfig
from ahi_module_2.forecasting.aging_projection import calculate_corrected_aging_rate

# Guard against overflow when projecting very high aging rates over long horizons
_MAX_FHI_EXPONENT: float = 700.0


class FutureHealthEngine:
    """Projects Future Health Index (FHI) forward in time.

    beta_corrected = ln(CurrentAHI / HI_NEW) / CurrentAge
    FHI(future_age) = HI_NEW * exp(beta_corrected * future_age)
    """

    def __init__(self, config: HealthConfig | None = None) -> None:
        self._cfg = config or HealthConfig()

    def calculate_corrected_aging_rate(self, current_ahi: float, current_age: float) -> float:
        """Delegate to aging_projection utility."""
        return calculate_corrected_aging_rate(current_ahi, current_age, self._cfg)

    def project_future_health(
        self,
        current_ahi: float,
        current_age: float,
        future_age: float,
    ) -> float:
        """Return FHI at *future_age* given the current state."""
        beta_c = self.calculate_corrected_aging_rate(current_ahi, current_age)
        exponent = min(beta_c * future_age, _MAX_FHI_EXPONENT)
        return self._cfg.hi_new * math.exp(exponent)
