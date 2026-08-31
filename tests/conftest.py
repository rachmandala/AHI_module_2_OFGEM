"""Shared test fixtures."""

from __future__ import annotations

import pytest

from ahi_module_2.data_models.asset_input import AssetInput
from ahi_module_2.data_models.condition_inputs import ConditionInputs, ModifierInput
from ahi_module_2.data_models.financial_inputs import FinancialInputs
from ahi_module_2.utils.enums import AssetClass


@pytest.fixture()
def basic_asset() -> AssetInput:
    return AssetInput(
        asset_id="A001",
        asset_name="Test Turbine",
        asset_class=AssetClass.TURBINE,
        design_life=30.0,
        current_age=10.0,
        max_load=100.0,
        normal_load=80.0,
        distance_to_coast_factor=1.0,
        altitude_factor=1.0,
        temperature_factor=1.2,
        corrosive_factor=1.0,
        dust_factor=1.0,
    )


@pytest.fixture()
def basic_financials() -> FinancialInputs:
    return FinancialInputs(
        corrective_maintenance_cost=50_000.0,
        preventive_maintenance_cost=5_000.0,
        major_maintenance_cost=200_000.0,
    )


@pytest.fixture()
def empty_conditions() -> ConditionInputs:
    return ConditionInputs()


@pytest.fixture()
def with_modifiers() -> ConditionInputs:
    return ConditionInputs(
        health_modifiers=[ModifierInput(name="vibration", weight=0.1, value=1.5)],
        reliability_modifiers=[ModifierInput(name="insulation", weight=0.05, value=0.8)],
    )
