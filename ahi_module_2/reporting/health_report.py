"""Health report generation."""

from __future__ import annotations

from dataclasses import dataclass

from ahi_module_2.simulation.state_tracker import StateTracker
from ahi_module_2.utils.helpers import classify_health_band
from ahi_module_2.utils.enums import HealthBand


@dataclass
class HealthReportEntry:
    time: float
    hi: float
    ahi: float
    health_band: HealthBand


class HealthReport:
    """Generates a health report from simulation results."""

    @staticmethod
    def generate(tracker: StateTracker) -> list[HealthReportEntry]:
        return [
            HealthReportEntry(
                time=s.time,
                hi=s.hi,
                ahi=s.ahi,
                health_band=classify_health_band(s.ahi),
            )
            for s in tracker.steps
        ]
