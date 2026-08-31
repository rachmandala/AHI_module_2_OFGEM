"""Health engine – core AHI calculations."""

from __future__ import annotations

import math
from typing import Sequence

from ahi_module_2.config.health_config import HealthConfig
from ahi_module_2.data_models.condition_inputs import ModifierInput


class HealthEngine:
    """Implements all health-related calculations.

    Mathematical model:
        FEL = NormalLoad / MaximumPermissibleLoad
        ExpectedLife = DesignLife / (FFL * FEL)
        beta = ln(HI_EOL / HI_NEW) / ExpectedLife
        HI(t) = HI_NEW * exp(beta * age)
        HM = sum(weight_i * input_i)
        RM = sum(weight_i * input_i)
        AHI = HI * exp(HM + RM)
    """

    def __init__(self, config: HealthConfig | None = None) -> None:
        self._cfg = config or HealthConfig()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def calculate_expected_life(
        self,
        design_life: float,
        ffl: float,
        normal_load: float,
        max_load: float,
    ) -> float:
        """Return expected service life in years."""
        fel = normal_load / max_load
        return design_life / (ffl * fel)

    def calculate_aging_rate(self, expected_life: float) -> float:
        """Return the exponential aging rate beta (1/year)."""
        return math.log(self._cfg.hi_eol / self._cfg.hi_new) / expected_life

    def calculate_base_health(self, age: float, beta: float) -> float:
        """Return base Health Index HI(t) = HI_NEW * exp(beta * age)."""
        return self._cfg.hi_new * math.exp(beta * age)

    @staticmethod
    def calculate_health_modifier(modifiers: Sequence[ModifierInput]) -> float:
        """Return total health modifier HM = sum(weight_i * value_i)."""
        return sum(m.weight * m.value for m in modifiers)

    @staticmethod
    def calculate_reliability_modifier(modifiers: Sequence[ModifierInput]) -> float:
        """Return total reliability modifier RM = sum(weight_i * value_i)."""
        return sum(m.weight * m.value for m in modifiers)

    @staticmethod
    def calculate_ahi(hi: float, hm: float, rm: float) -> float:
        """Return Asset Health Index AHI = HI * exp(HM + RM)."""
        return hi * math.exp(hm + rm)
