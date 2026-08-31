"""TotEx report generation."""

from __future__ import annotations

from dataclasses import dataclass

from ahi_module_2.simulation.state_tracker import StateTracker


@dataclass
class TotExReportEntry:
    time: float
    opex: float
    capex: float
    totex: float


class TotExReport:
    """Generates expenditure trends from simulation results."""

    @staticmethod
    def generate(tracker: StateTracker) -> list[TotExReportEntry]:
        cumulative_opex = 0.0
        cumulative_capex = 0.0
        entries = []
        for s in tracker.steps:
            cumulative_opex += s.opex
            cumulative_capex += s.capex
            entries.append(
                TotExReportEntry(
                    time=s.time,
                    opex=cumulative_opex,
                    capex=cumulative_capex,
                    totex=cumulative_opex + cumulative_capex,
                )
            )
        return entries
