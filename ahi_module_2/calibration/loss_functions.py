"""Loss functions for calibration."""

from __future__ import annotations

import numpy as np


def squared_error_loss(
    predicted_opex: list[float],
    observed_opex: list[float],
    predicted_capex: list[float],
    observed_capex: list[float],
) -> float:
    """Return sum of squared errors for OpEx and CapEx.

    Objective: minimize sum(OpExError^2 + CapExError^2)
    """
    opex_errors = np.subtract(predicted_opex, observed_opex)
    capex_errors = np.subtract(predicted_capex, observed_capex)
    return float(np.sum(opex_errors**2) + np.sum(capex_errors**2))
