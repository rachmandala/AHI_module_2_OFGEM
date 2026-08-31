"""Calibration result validation."""

from __future__ import annotations

from ahi_module_2.calibration.calibration_runner import CalibrationResult


class CalibrationValidationError(ValueError):
    pass


def validate_calibration_result(result: CalibrationResult, loss_threshold: float = 1e6) -> None:
    """Raise CalibrationValidationError if calibration loss is too high."""
    if result.final_loss > loss_threshold:
        raise CalibrationValidationError(
            f"Calibration loss {result.final_loss:.2f} exceeds threshold {loss_threshold}."
        )
