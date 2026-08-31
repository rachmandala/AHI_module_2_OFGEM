"""Tests for the reliability engine."""

import pytest

from ahi_module_2.core.reliability_engine import ReliabilityEngine
from ahi_module_2.utils.constants import POF_AHI_FLOOR, POF_C, POF_K


class TestReliabilityEngine:
    def setup_method(self):
        self.engine = ReliabilityEngine()

    def test_pof_at_floor(self):
        # AHI below floor → use floor value
        pof = self.engine.calculate_probability_of_failure(2.0)
        h = POF_AHI_FLOOR
        ch = POF_C * h
        expected = POF_K * (1.0 + ch + ch**2 / 2.0 + ch**3 / 6.0)
        assert pof == pytest.approx(expected)

    def test_pof_above_floor(self):
        ahi = 6.0
        pof = self.engine.calculate_probability_of_failure(ahi)
        ch = POF_C * ahi
        expected = POF_K * (1.0 + ch + ch**2 / 2.0 + ch**3 / 6.0)
        assert pof == pytest.approx(expected)

    def test_pof_increases_with_ahi(self):
        pof_low = self.engine.calculate_probability_of_failure(4.0)
        pof_high = self.engine.calculate_probability_of_failure(5.5)
        assert pof_high > pof_low

    def test_custom_k_c(self):
        engine = ReliabilityEngine(k=0.001, c=0.5)
        pof = engine.calculate_probability_of_failure(4.0)
        h = max(4.0, 4.0)
        ch = 0.5 * h
        expected = 0.001 * (1.0 + ch + ch**2 / 2.0 + ch**3 / 6.0)
        assert pof == pytest.approx(expected)
