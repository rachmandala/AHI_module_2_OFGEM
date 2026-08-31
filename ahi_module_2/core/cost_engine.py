"""Cost engine – OpEx, CapEx, TotEx calculations."""

from __future__ import annotations

from ahi_module_2.data_models.financial_inputs import FinancialInputs


class CostEngine:
    """Computes operational, capital, and total expenditure.

    OpEx = PoF * CorrectiveMaintenanceCost + PreventiveMaintenanceCost
    CapEx = MajorMaintenanceTrigger * MajorMaintenanceCost
    TotEx = AccumulatedOpEx + AccumulatedCapEx
    """

    def calculate_opex(
        self,
        pof: float,
        financials: FinancialInputs,
    ) -> float:
        """Return annual OpEx."""
        return pof * financials.corrective_maintenance_cost + financials.preventive_maintenance_cost

    def calculate_capex(
        self,
        major_maintenance_triggered: bool,
        financials: FinancialInputs,
    ) -> float:
        """Return CapEx for this time step (0 unless major maintenance triggered)."""
        return financials.major_maintenance_cost if major_maintenance_triggered else 0.0

    @staticmethod
    def calculate_totex(
        accumulated_opex: float,
        accumulated_capex: float,
    ) -> float:
        """Return total expenditure (TotEx = AccumulatedOpEx + AccumulatedCapEx)."""
        return accumulated_opex + accumulated_capex
