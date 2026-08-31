"""Condition monitoring inputs for health and reliability modifiers."""

from __future__ import annotations

from typing import Sequence

from pydantic import BaseModel, Field


class ModifierInput(BaseModel):
    """A single weighted modifier input."""

    name: str = Field(..., description="Modifier name/label")
    weight: float = Field(..., description="Modifier weight")
    value: float = Field(..., description="Normalised input value")


class ConditionInputs(BaseModel):
    """Collection of health and reliability modifier inputs."""

    health_modifiers: Sequence[ModifierInput] = Field(
        default_factory=list,
        description="List of health modifier inputs (HM)",
    )
    reliability_modifiers: Sequence[ModifierInput] = Field(
        default_factory=list,
        description="List of reliability modifier inputs (RM)",
    )
