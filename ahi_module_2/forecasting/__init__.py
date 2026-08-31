"""Forecasting sub-package."""

from ahi_module_2.forecasting.aging_projection import calculate_corrected_aging_rate
from ahi_module_2.forecasting.future_health import FutureHealthEngine
from ahi_module_2.forecasting.scenario_engine import Scenario, ScenarioEngine

__all__ = [
    "calculate_corrected_aging_rate",
    "FutureHealthEngine",
    "Scenario",
    "ScenarioEngine",
]
