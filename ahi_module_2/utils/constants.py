"""Constants used throughout AHI Module 2."""

# Health Index boundary values
HI_NEW: float = 0.5  # Health Index at new condition
HI_EOL: float = 5.5  # Health Index at end of life

# Probability of Failure constants
POF_K: float = 1e-4  # Base PoF scaling constant
POF_C: float = 1.0   # PoF Taylor series coefficient

# AHI threshold above which PoF uses max(4, AHI)
POF_AHI_FLOOR: float = 4.0

# Default AHI threshold for AHI-based maintenance policy
AHI_MAINTENANCE_THRESHOLD: float = 5.5

# Simulation defaults
DEFAULT_TIME_STEP: float = 1.0       # years
DEFAULT_SIMULATION_HORIZON: int = 40  # years
