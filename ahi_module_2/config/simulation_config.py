"""Simulation configuration."""

from __future__ import annotations

from pydantic import BaseModel, Field

from ahi_module_2.utils.constants import DEFAULT_SIMULATION_HORIZON, DEFAULT_TIME_STEP


class SimulationConfig(BaseModel):
    """Configuration for simulation runs."""

    time_step: float = Field(default=DEFAULT_TIME_STEP, gt=0, description="Simulation time step (years)")
    horizon: int = Field(default=DEFAULT_SIMULATION_HORIZON, gt=0, description="Simulation horizon (years)")
    random_seed: int | None = Field(default=None, description="Random seed for reproducibility")
