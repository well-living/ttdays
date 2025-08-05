"""Date Calculator Package.

This package provides functionality for calculating date-related values
given two of the three parameters: start_date, end_date, and days.
"""

from .date_model import DatePeriod
from .date_calculator import (
    calculate_days_from_dates,
    calculate_months_from_dates,
    calculate_years_from_dates,
    calculate_start_date,
    calculate_start_date_from_months,
    calculate_start_date_from_years,
    calculate_end_date,
    calculate_end_date_from_months,
    calculate_end_date_from_years
)


__version__ = "0.1.1"
__all__ = [
    "DatePeriod",
    "calculate_days_from_dates",
    "calculate_months_from_dates",
    "calculate_years_from_dates",
    "calculate_start_date",
    "calculate_start_date_from_months",
    "calculate_start_date_from_years",
    "calculate_end_date",
    "calculate_end_date_from_months",
    "calculate_end_date_from_years"
]