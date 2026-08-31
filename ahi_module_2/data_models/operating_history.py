"""Operating history data model."""

from __future__ import annotations

from pydantic import BaseModel, Field


class OperatingHistory(BaseModel):
    """Historical operating data for an asset."""

    planned_operating_hours: float = Field(..., ge=0, description="Planned operating hours per year")
    actual_operating_hours: float = Field(..., ge=0, description="Actual operating hours per year")
    start_stop_events: int = Field(0, ge=0, description="Number of start/stop events per year")
