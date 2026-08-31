"""Risk report generation."""

from __future__ import annotations

from dataclasses import dataclass

from ahi_module_2.simulation.state_tracker import StateTracker


@dataclass
class RiskReportEntry:
    time: float
    pof: float
    failure_rank: int


class RiskReport:
    """Generates a risk report sorted by PoF."""

    @staticmethod
    def generate(tracker: StateTracker) -> list[RiskReportEntry]:
        sorted_steps = sorted(tracker.steps, key=lambda s: s.pof, reverse=True)
        return [
            RiskReportEntry(time=s.time, pof=s.pof, failure_rank=rank + 1)
            for rank, s in enumerate(sorted_steps)
        ]
