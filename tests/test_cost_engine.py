"""Tests for cost engine."""

import pytest

from ahi_module_2.core.cost_engine import CostEngine
from ahi_module_2.data_models.financial_inputs import FinancialInputs


@pytest.fixture()
def financials():
    return FinancialInputs(
        corrective_maintenance_cost=50_000.0,
        preventive_maintenance_cost=5_000.0,
        major_maintenance_cost=200_000.0,
    )


class TestCostEngine:
    def setup_method(self):
        self.engine = CostEngine()

    def test_opex_no_failure(self, financials):
        opex = self.engine.calculate_opex(0.0, financials)
        assert opex == pytest.approx(5_000.0)

    def test_opex_with_pof(self, financials):
        pof = 0.1
        opex = self.engine.calculate_opex(pof, financials)
        assert opex == pytest.approx(0.1 * 50_000 + 5_000)

    def test_capex_no_trigger(self, financials):
        assert self.engine.calculate_capex(False, financials) == pytest.approx(0.0)

    def test_capex_with_trigger(self, financials):
        assert self.engine.calculate_capex(True, financials) == pytest.approx(200_000.0)

    def test_totex(self):
        assert CostEngine.calculate_totex(100.0, 200.0) == pytest.approx(300.0)
