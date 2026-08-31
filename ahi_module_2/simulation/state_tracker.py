"""State tracker for simulation step results."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class SimulationStep:
    """Snapshot of asset state at a single simulation time step."""

    time: float
    age: float
    hi: float
    ahi: float
    pof: float
    opex: float
    capex: float
    totex: float
    fhi: float
    maintenance_triggered: bool = False


@dataclass
class StateTracker:
    """Accumulates simulation steps and running cost totals."""

    steps: list[SimulationStep] = field(default_factory=list)
    accumulated_opex: float = 0.0
    accumulated_capex: float = 0.0

    def record(self, step: SimulationStep) -> None:
        """Append a simulation step and update accumulators."""
        self.accumulated_opex += step.opex
        self.accumulated_capex += step.capex
        self.steps.append(step)

    @property
    def totex(self) -> float:
        return self.accumulated_opex + self.accumulated_capex
