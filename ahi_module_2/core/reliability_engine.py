"""Reliability engine – Probability of Failure calculations."""

from __future__ import annotations

from ahi_module_2.utils.constants import POF_AHI_FLOOR, POF_C, POF_K


class ReliabilityEngine:
    """Computes the Probability of Failure (PoF).

    PoF = K * (1 + C*H + (C*H)^2/2 + (C*H)^3/6)
    where H = max(POF_AHI_FLOOR, AHI)

    This is a third-order Taylor expansion of K * exp(C * H).
    """

    def __init__(
        self,
        k: float = POF_K,
        c: float = POF_C,
        ahi_floor: float = POF_AHI_FLOOR,
    ) -> None:
        self.k = k
        self.c = c
        self.ahi_floor = ahi_floor

    def calculate_probability_of_failure(self, ahi: float) -> float:
        """Return PoF for the given AHI value."""
        h = max(self.ahi_floor, ahi)
        ch = self.c * h
        return self.k * (1.0 + ch + ch**2 / 2.0 + ch**3 / 6.0)
