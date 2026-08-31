"""Tests for reporting modules."""

import pytest

from ahi_module_2.reporting.health_report import HealthReport
from ahi_module_2.reporting.maintenance_report import MaintenanceReport
from ahi_module_2.reporting.risk_report import RiskReport
from ahi_module_2.reporting.totex_report import TotExReport
from ahi_module_2.simulation.state_tracker import SimulationStep, StateTracker
from ahi_module_2.utils.enums import HealthBand


def make_tracker(steps_data: list[dict]) -> StateTracker:
    tracker = StateTracker()
    for d in steps_data:
        tracker.record(SimulationStep(**d))
    return tracker


BASE_STEP = dict(time=0, age=0, hi=0.5, ahi=0.5, pof=0.01, opex=100, capex=0, totex=100, fhi=0.5, maintenance_triggered=False)


class TestHealthReport:
    def test_generates_entries(self):
        tracker = make_tracker([BASE_STEP])
        entries = HealthReport.generate(tracker)
        assert len(entries) == 1
        assert entries[0].health_band == HealthBand.GOOD

    def test_health_band_critical(self):
        step = {**BASE_STEP, "ahi": 5.5}
        tracker = make_tracker([step])
        entries = HealthReport.generate(tracker)
        assert entries[0].health_band == HealthBand.CRITICAL


class TestRiskReport:
    def test_sorted_by_pof_descending(self):
        s1 = {**BASE_STEP, "time": 0, "pof": 0.01}
        s2 = {**BASE_STEP, "time": 1, "pof": 0.05}
        tracker = make_tracker([s1, s2])
        entries = RiskReport.generate(tracker)
        assert entries[0].pof >= entries[1].pof
        assert entries[0].failure_rank == 1


class TestMaintenanceReport:
    def test_only_maintenance_steps(self):
        s1 = {**BASE_STEP, "maintenance_triggered": True}
        s2 = {**BASE_STEP, "maintenance_triggered": False}
        tracker = make_tracker([s1, s2])
        events = MaintenanceReport.generate(tracker)
        assert len(events) == 1

    def test_empty_when_no_maintenance(self):
        tracker = make_tracker([BASE_STEP])
        assert MaintenanceReport.generate(tracker) == []


class TestTotExReport:
    def test_cumulative_totex_increases(self):
        steps = [{**BASE_STEP, "time": i, "opex": 100, "capex": 0} for i in range(3)]
        tracker = make_tracker(steps)
        entries = TotExReport.generate(tracker)
        assert entries[-1].totex == pytest.approx(300.0)

    def test_capex_accumulated(self):
        s1 = {**BASE_STEP, "capex": 1000}
        tracker = make_tracker([s1])
        entries = TotExReport.generate(tracker)
        assert entries[0].capex == pytest.approx(1000.0)
