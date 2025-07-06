
from datetime import date

from .date_calculator import DateCalculator


# Module-level constants
DEFAULT_INCLUDE_START: bool = True

# Module-level calculator instance
_calculator = DateCalculator()


def calculate_days_from_dates(
    start_date: date,
    end_date: date,
    include_start: bool = DEFAULT_INCLUDE_START
) -> int:
    """Calculate the number of days elapsed between start and end dates.
    
    This is a convenience function that wraps the DateCalculator method.
    
    Parameters
    ----------
    start_date : date
        The starting date
    end_date : date
        The ending date
    include_start : bool, optional
        Whether to include the start date in the count, by default True
        
    Returns
    -------
    int
        The number of days elapsed. If include_start is True, the count
        includes the start date. If False, it excludes the start date.
        
    Raises
    ------
    ValueError
        If start_date is after end_date
        
    Examples
    --------
    >>> from datetime import date
    >>> start = date(2024, 1, 1)
    >>> end = date(2024, 1, 3)
    >>> calculate_days_from_dates(start, end)
    3
    >>> calculate_days_from_dates(start, end, include_start=False)
    2
    """
    return _calculator.calculate_days_from_dates(start_date, end_date, include_start)


def calculate_end_date(
    start_date: date,
    days: int,
    include_start: bool = DEFAULT_INCLUDE_START
) -> date:
    """Calculate the end date given a start date and number of days.
    
    This is a convenience function that wraps the DateCalculator method.
    
    Parameters
    ----------
    start_date : date
        The starting date
    days : int
        The number of days to add
    include_start : bool, optional
        Whether the start date is included in the count, by default True
        
    Returns
    -------
    date
        The calculated end date. If include_start is True, the end date
        will be start_date + (days - 1). If False, it will be 
        start_date + days.
        
    Raises
    ------
    ValueError
        If days is negative
        
    Examples
    --------
    >>> from datetime import date
    >>> start = date(2024, 1, 1)
    >>> calculate_end_date(start, 3)
    datetime.date(2024, 1, 3)
    >>> calculate_end_date(start, 3, include_start=False)
    datetime.date(2024, 1, 4)
    """
    return _calculator.calculate_end_date(start_date, days, include_start)


def calculate_start_date(
    end_date: date,
    days: int,
    include_start: bool = DEFAULT_INCLUDE_START
) -> date:
    """Calculate the start date given an end date and number of days.
    
    This is a convenience function that wraps the DateCalculator method.
    
    Parameters
    ----------
    end_date : date
        The ending date
    days : int
        The number of days to subtract
    include_start : bool, optional
        Whether the start date is included in the count, by default True
        
    Returns
    -------
    date
        The calculated start date. If include_start is True, the start date
        will be end_date - (days - 1). If False, it will be 
        end_date - days.
        
    Raises
    ------
    ValueError
        If days is negative
        
    Examples
    --------
    >>> from datetime import date
    >>> end = date(2024, 1, 3)
    >>> calculate_start_date(end, 3)
    datetime.date(2024, 1, 1)
    >>> calculate_start_date(end, 3, include_start=False)
    datetime.date(2023, 12, 31)
    """
    return _calculator.calculate_start_date(end_date, days, include_start)