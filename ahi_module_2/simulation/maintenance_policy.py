"""Maintenance policy implementations."""

from __future__ import annotations

from abc import ABC, abstractmethod

from ahi_module_2.utils.constants import AHI_MAINTENANCE_THRESHOLD


class MaintenancePolicy(ABC):
    """Abstract base class for maintenance policies."""

    @abstractmethod
    def should_trigger(self, current_age: float, current_ahi: float) -> bool:
        """Return True when maintenance should be triggered."""


class AgeBasedPolicy(MaintenancePolicy):
    """Trigger maintenance when asset age exceeds *age_threshold*."""

    def __init__(self, age_threshold: float) -> None:
        if age_threshold <= 0:
            raise ValueError("age_threshold must be positive")
        self.age_threshold = age_threshold

    def should_trigger(self, current_age: float, current_ahi: float) -> bool:
        return current_age >= self.age_threshold


class AHIBasedPolicy(MaintenancePolicy):
    """Trigger maintenance when AHI reaches or exceeds *ahi_threshold*."""

    def __init__(self, ahi_threshold: float = AHI_MAINTENANCE_THRESHOLD) -> None:
        self.ahi_threshold = ahi_threshold

    def should_trigger(self, current_age: float, current_ahi: float) -> bool:
        return current_ahi >= self.ahi_threshold
