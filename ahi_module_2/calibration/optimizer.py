"""Calibration optimizer using scipy.optimize."""

from __future__ import annotations

from typing import Callable

import numpy as np
from scipy.optimize import minimize


class Optimizer:
    """Wraps scipy.optimize.minimize for calibration tasks."""

    def __init__(self, method: str = "Powell") -> None:
        self.method = method
        self.result: object = None

    def minimize(
        self,
        objective: Callable[[np.ndarray], float],
        initial_params: np.ndarray,
        bounds: list[tuple[float | None, float | None]] | None = None,
    ) -> np.ndarray:
        """Minimise *objective* starting from *initial_params*.

        Returns the optimised parameter vector.
        """
        result = minimize(
            objective,
            initial_params,
            method=self.method,
            bounds=bounds,
        )
        self.result = result
        return result.x
