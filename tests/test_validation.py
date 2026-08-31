"""Tests for validation modules and helpers."""

import pytest

from ahi_module_2.calibration.calibration_runner import CalibrationResult
from ahi_module_2.core.maintenance_engine import MaintenanceEngine
from ahi_module_2.data_models.asset_input import AssetInput
from ahi_module_2.utils.enums import AssetClass, HealthBand
from ahi_module_2.utils.helpers import classify_health_band, clamp, safe_log
from ahi_module_2.validation.calibration_validation import (
    CalibrationValidationError,
    validate_calibration_result,
)
from ahi_module_2.validation.health_validation import HealthValidationError, validate_ahi
from ahi_module_2.validation.input_validation import InputValidationError, validate_asset_input


class TestHelpers:
    def test_classify_good(self):
        assert classify_health_band(1.0) == HealthBand.GOOD

    def test_classify_fair(self):
        assert classify_health_band(2.5) == HealthBand.FAIR

    def test_classify_poor(self):
        assert classify_health_band(4.0) == HealthBand.POOR

    def test_classify_critical(self):
        assert classify_health_band(5.5) == HealthBand.CRITICAL

    def test_safe_log_positive(self):
        import math
        assert safe_log(1.0) == pytest.approx(0.0)
        assert safe_log(math.e) == pytest.approx(1.0)

    def test_safe_log_zero_returns_fallback(self):
        assert safe_log(0.0) == pytest.approx(0.0)
        assert safe_log(-1.0, fallback=-999.0) == pytest.approx(-999.0)

    def test_clamp(self):
        assert clamp(5.0, 0.0, 3.0) == pytest.approx(3.0)
        assert clamp(-1.0, 0.0, 3.0) == pytest.approx(0.0)
        assert clamp(2.0, 0.0, 3.0) == pytest.approx(2.0)


class TestInputValidation:
    def _make(self, **kw) -> AssetInput:
        base = dict(
            asset_id="V001", asset_name="Test", asset_class=AssetClass.PUMP,
            design_life=20.0, current_age=5.0, max_load=50.0, normal_load=40.0,
            distance_to_coast_factor=1.0, altitude_factor=1.0,
            temperature_factor=1.0, corrosive_factor=1.0, dust_factor=1.0,
        )
        base.update(kw)
        return AssetInput(**base)

    def test_valid_asset_passes(self):
        validate_asset_input(self._make())  # should not raise

    def test_excessive_age_raises(self):
        with pytest.raises(InputValidationError):
            validate_asset_input(self._make(current_age=50.0))


class TestHealthValidation:
    def test_valid_ahi_passes(self):
        validate_ahi(3.0)

    def test_negative_ahi_raises(self):
        with pytest.raises(HealthValidationError):
            validate_ahi(-0.1)

    def test_very_large_ahi_raises(self):
        with pytest.raises(HealthValidationError):
            validate_ahi(999.0)


class TestCalibrationValidation:
    def test_good_result_passes(self):
        result = CalibrationResult(optimised_hm_weights=[0.1], optimised_rm_weights=[], final_loss=0.0)
        validate_calibration_result(result)

    def test_high_loss_raises(self):
        result = CalibrationResult(optimised_hm_weights=[], optimised_rm_weights=[], final_loss=2e6)
        with pytest.raises(CalibrationValidationError):
            validate_calibration_result(result)


class TestMaintenanceEngine:
    def setup_method(self):
        self.engine = MaintenanceEngine()

    def test_age_trigger(self):
        assert self.engine.determine_major_maintenance_trigger(20.0, age_threshold=20.0) is True

    def test_ahi_trigger(self):
        assert self.engine.determine_major_maintenance_trigger(
            10.0, current_ahi=5.5, ahi_threshold=5.5
        ) is True

    def test_no_trigger(self):
        assert self.engine.determine_major_maintenance_trigger(10.0) is False

    def test_reset_returns_zero(self):
        assert MaintenanceEngine.perform_major_maintenance_reset() == pytest.approx(0.0)
