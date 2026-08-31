"""Tests for the environment engine."""

import pytest

from ahi_module_2.core.environment import EnvironmentEngine
from ahi_module_2.data_models.asset_input import AssetInput
from ahi_module_2.utils.enums import AssetClass


def make_asset(**kwargs) -> AssetInput:
    defaults = dict(
        asset_id="E001",
        asset_name="Env Test",
        asset_class=AssetClass.PUMP,
        design_life=25.0,
        current_age=5.0,
        max_load=50.0,
        normal_load=40.0,
        distance_to_coast_factor=1.0,
        altitude_factor=1.0,
        temperature_factor=1.0,
        corrosive_factor=1.0,
        dust_factor=1.0,
    )
    defaults.update(kwargs)
    return AssetInput(**defaults)


class TestEnvironmentEngine:
    def setup_method(self):
        self.engine = EnvironmentEngine()

    def test_ffl_returns_max_factor(self):
        asset = make_asset(temperature_factor=1.8)
        ffl = self.engine.calculate_environment_factor(asset)
        assert ffl == pytest.approx(1.8)

    def test_ffl_all_equal(self):
        asset = make_asset()
        ffl = self.engine.calculate_environment_factor(asset)
        assert ffl == pytest.approx(1.0)

    def test_ffl_coastal_dominant(self):
        asset = make_asset(distance_to_coast_factor=2.0)
        ffl = self.engine.calculate_environment_factor(asset)
        assert ffl == pytest.approx(2.0)
