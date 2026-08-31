"""Maintenance engine – maintenance trigger and reset logic."""

from __future__ import annotations


class MaintenanceEngine:
    """Determines when major maintenance should occur and resets state."""

    def determine_major_maintenance_trigger(
        self,
        current_age: float,
        age_threshold: float | None = None,
        current_ahi: float | None = None,
        ahi_threshold: float | None = None,
    ) -> bool:
        """Return True when a major maintenance event should be triggered.

        Supports both age-based and AHI-based trigger logic.
        """
        if age_threshold is not None and current_age >= age_threshold:
            return True
        if ahi_threshold is not None and current_ahi is not None and current_ahi >= ahi_threshold:
            return True
        return False

    @staticmethod
    def perform_major_maintenance_reset(reset_age: float = 0.0) -> float:
        """Return the effective age after major maintenance reset."""
        return max(0.0, reset_age)
