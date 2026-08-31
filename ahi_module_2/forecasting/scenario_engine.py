"""Scenario engine for what-if analysis."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from ahi_module_2.utils.enums import ScenarioType


@dataclass
class Scenario:
    """A named scenario with parameter overrides."""

    name: str
    scenario_type: ScenarioType
    overrides: dict[str, Any] = field(default_factory=dict)


class ScenarioEngine:
    """Manages and applies scenarios to asset parameters."""

    def __init__(self) -> None:
        self._scenarios: list[Scenario] = []

    def add_scenario(self, scenario: Scenario) -> None:
        """Register a scenario."""
        self._scenarios.append(scenario)

    @property
    def scenarios(self) -> list[Scenario]:
        return list(self._scenarios)

    def apply_overrides(self, base_params: dict[str, Any], scenario: Scenario) -> dict[str, Any]:
        """Return a copy of *base_params* with scenario overrides applied."""
        merged = dict(base_params)
        merged.update(scenario.overrides)
        return merged
