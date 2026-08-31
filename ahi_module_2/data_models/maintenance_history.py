"""Maintenance history data model."""

from __future__ import annotations

from pydantic import BaseModel, Field


class MaintenanceHistory(BaseModel):
    """Historical maintenance records for an asset."""

    major_maintenance_count: int = Field(0, ge=0, description="Total number of major maintenance events")
    age_at_last_maintenance: float = Field(0.0, ge=0, description="Asset age at most recent maintenance (years)")
