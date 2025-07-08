"""Date Calculator Package.

This package provides functionality for calculating date-related values
given two of the three parameters: start_date, end_date, and days.
"""

from .date_calculator import DateCalculator
from .functions import (
    calculate_days_from_dates,
    calculate_end_date,
    calculate_start_date
)
from .date_model import DateModel

__version__ = "0.1.0"
__all__ = [
    "DateCalculator",
    "DateModel",
    "calculate_days_from_dates",
    "calculate_end_date",
    "calculate_start_date",
]