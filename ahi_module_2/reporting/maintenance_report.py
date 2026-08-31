"""Maintenance report generation."""

from __future__ import annotations

from dataclasses import dataclass

from ahi_module_2.simulation.state_tracker import StateTracker


@dataclass
class MaintenanceEvent:
    time: float
    age_at_maintenance: float
    ahi_at_maintenance: float


class MaintenanceReport:
    """Extracts maintenance events from simulation results."""

    @staticmethod
    def generate(tracker: StateTracker) -> list[MaintenanceEvent]:
        return [
            MaintenanceEvent(
                time=s.time,
                age_at_maintenance=s.age,
                ahi_at_maintenance=s.ahi,
            )
            for s in tracker.steps
            if s.maintenance_triggered
        ]
