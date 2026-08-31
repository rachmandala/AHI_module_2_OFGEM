"""Financial configuration."""

from __future__ import annotations

from pydantic import BaseModel, Field


class FinancialConfig(BaseModel):
    """Configuration for financial calculations."""

    discount_rate: float = Field(default=0.05, ge=0, description="Annual discount rate for NPV calculations")
    currency_symbol: str = Field(default="£", description="Currency symbol for reporting")
