"""Health engine configuration."""

from __future__ import annotations

from pydantic import BaseModel, Field

from ahi_module_2.utils.constants import HI_EOL, HI_NEW


class HealthConfig(BaseModel):
    """Configuration for the health calculation engine."""

    hi_new: float = Field(default=HI_NEW, gt=0, description="Health Index at new condition")
    hi_eol: float = Field(default=HI_EOL, gt=0, description="Health Index at end of life")
