"""Financial inputs data model."""

from __future__ import annotations

from pydantic import BaseModel, Field


class FinancialInputs(BaseModel):
    """Cost inputs for OpEx/CapEx calculation."""

    corrective_maintenance_cost: float = Field(..., ge=0, description="Cost of a corrective maintenance event (£)")
    preventive_maintenance_cost: float = Field(..., ge=0, description="Annual preventive maintenance cost (£/year)")
    major_maintenance_cost: float = Field(..., ge=0, description="Cost of a major maintenance event (£)")
