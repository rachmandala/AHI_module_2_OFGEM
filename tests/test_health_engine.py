"""Tests for the health engine."""

import math

import pytest

from ahi_module_2.config.health_config import HealthConfig
from ahi_module_2.core.health_engine import HealthEngine
from ahi_module_2.data_models.condition_inputs import ModifierInput
from ahi_module_2.utils.constants import HI_EOL, HI_NEW


class TestHealthEngine:
    def setup_method(self):
        self.engine = HealthEngine()

    def test_expected_life_basic(self):
        # design_life=30, ffl=1.0, normal=80, max=100 → fel=0.8, expected=30/0.8=37.5
        result = self.engine.calculate_expected_life(30.0, 1.0, 80.0, 100.0)
        assert result == pytest.approx(37.5)

    def test_expected_life_with_ffl(self):
        result = self.engine.calculate_expected_life(30.0, 1.5, 80.0, 100.0)
        assert result == pytest.approx(30.0 / (1.5 * 0.8))

    def test_aging_rate_at_expected_life_gives_hi_eol(self):
        expected_life = self.engine.calculate_expected_life(30.0, 1.0, 80.0, 100.0)
        beta = self.engine.calculate_aging_rate(expected_life)
        hi_at_eol = self.engine.calculate_base_health(expected_life, beta)
        assert hi_at_eol == pytest.approx(HI_EOL, rel=1e-6)

    def test_base_health_at_zero(self):
        beta = self.engine.calculate_aging_rate(30.0)
        hi = self.engine.calculate_base_health(0.0, beta)
        assert hi == pytest.approx(HI_NEW)

    def test_health_modifier_sum(self):
        mods = [
            ModifierInput(name="a", weight=0.1, value=2.0),
            ModifierInput(name="b", weight=0.2, value=3.0),
        ]
        hm = HealthEngine.calculate_health_modifier(mods)
        assert hm == pytest.approx(0.1 * 2.0 + 0.2 * 3.0)

    def test_health_modifier_empty(self):
        assert HealthEngine.calculate_health_modifier([]) == pytest.approx(0.0)

    def test_reliability_modifier_sum(self):
        mods = [ModifierInput(name="r", weight=0.05, value=1.0)]
        rm = HealthEngine.calculate_reliability_modifier(mods)
        assert rm == pytest.approx(0.05)

    def test_ahi_no_modifiers(self):
        beta = self.engine.calculate_aging_rate(30.0)
        hi = self.engine.calculate_base_health(5.0, beta)
        ahi = HealthEngine.calculate_ahi(hi, 0.0, 0.0)
        assert ahi == pytest.approx(hi)

    def test_ahi_with_positive_modifier(self):
        beta = self.engine.calculate_aging_rate(30.0)
        hi = self.engine.calculate_base_health(5.0, beta)
        ahi = HealthEngine.calculate_ahi(hi, 0.5, 0.0)
        assert ahi == pytest.approx(hi * math.exp(0.5))

    def test_custom_config(self):
        cfg = HealthConfig(hi_new=1.0, hi_eol=6.0)
        engine = HealthEngine(cfg)
        hi = engine.calculate_base_health(0.0, 0.1)
        assert hi == pytest.approx(1.0)
