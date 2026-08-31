"""Tests for forecasting modules."""

import math

import pytest

from ahi_module_2.config.health_config import HealthConfig
from ahi_module_2.forecasting.aging_projection import calculate_corrected_aging_rate
from ahi_module_2.forecasting.future_health import FutureHealthEngine
from ahi_module_2.forecasting.scenario_engine import Scenario, ScenarioEngine
from ahi_module_2.utils.constants import HI_NEW
from ahi_module_2.utils.enums import ScenarioType


class TestAgingProjection:
    def test_zero_age_returns_zero(self):
        rate = calculate_corrected_aging_rate(1.0, 0.0)
        assert rate == pytest.approx(0.0)

    def test_known_value(self):
        # If AHI = HI_NEW * exp(beta * age), then beta_corrected = beta
        beta = 0.05
        age = 10.0
        ahi = HI_NEW * math.exp(beta * age)
        rate = calculate_corrected_aging_rate(ahi, age)
        assert rate == pytest.approx(beta, rel=1e-6)

    def test_negative_ahi_returns_zero(self):
        rate = calculate_corrected_aging_rate(-1.0, 5.0)
        assert rate == pytest.approx(0.0)


class TestFutureHealthEngine:
    def setup_method(self):
        self.engine = FutureHealthEngine()

    def test_project_at_current_age_gives_ahi(self):
        age = 10.0
        beta = 0.05
        ahi = HI_NEW * math.exp(beta * age)
        fhi = self.engine.project_future_health(ahi, age, age)
        assert fhi == pytest.approx(ahi, rel=1e-4)

    def test_project_forward(self):
        age = 5.0
        ahi = HI_NEW * math.exp(0.05 * age)
        fhi = self.engine.project_future_health(ahi, age, 20.0)
        assert fhi > ahi  # future health should be worse (higher index)

    def test_project_zero_age_fallback(self):
        # Should not raise
        fhi = self.engine.project_future_health(HI_NEW, 0.0, 10.0)
        assert fhi == pytest.approx(HI_NEW)


class TestScenarioEngine:
    def test_add_and_retrieve_scenarios(self):
        engine = ScenarioEngine()
        s = Scenario("high_load", ScenarioType.LOAD, overrides={"normal_load": 95.0})
        engine.add_scenario(s)
        assert len(engine.scenarios) == 1
        assert engine.scenarios[0].name == "high_load"

    def test_apply_overrides(self):
        engine = ScenarioEngine()
        s = Scenario("coastal", ScenarioType.ENVIRONMENTAL, overrides={"distance_to_coast_factor": 1.8})
        result = engine.apply_overrides({"distance_to_coast_factor": 1.0, "altitude_factor": 1.0}, s)
        assert result["distance_to_coast_factor"] == pytest.approx(1.8)
        assert result["altitude_factor"] == pytest.approx(1.0)
