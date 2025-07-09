# functions.py
import datetime
from .date_calculator import DateCalculator

# Module-level constants
DEFAULT_INCLUDE_START: bool = True

# Module-level calculator instance
_calculator = DateCalculator()

def calculate_days_from_dates(
    start_date: datetime.date,
    end_date: datetime.date,
    include_start: bool = DEFAULT_INCLUDE_START
) -> int:
    """Calculate the number of days elapsed between start and end dates.
    
    This is a convenience function that wraps the DateCalculator method.
    
    Parameters
    ----------
    start_date : datetime.date
        The starting date
    end_date : datetime.date
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
    >>> import datetime
    >>> start = datetime.date(1989, 1, 28)
    >>> end = datetime.date(2025, 7, 7)
    >>> calculate_days_from_dates(start, end)
    13345
    >>> calculate_days_from_dates(start, end, include_start=False)
    13344
    """
    return _calculator.calculate_days_from_dates(start_date, end_date, include_start)

def calculate_start_date(
    end_date: datetime.date,
    days: int,
    include_start: bool = DEFAULT_INCLUDE_START
) -> datetime.date:
    """Calculate the start date given an end date and number of days.
    
    This is a convenience function that wraps the DateCalculator method.
    
    Parameters
    ----------
    end_date : datetime.date
        The ending date
    days : int
        The number of days to subtract
    include_start : bool, optional
        Whether the start date is included in the count, by default True
        
    Returns
    -------
    datetime.date
        The calculated start date. If include_start is True, the start date
        will be end_date - (days - 1). If False, it will be 
        end_date - days.
        
    Raises
    ------
    ValueError
        If days is negative
        
    Examples
    --------
    >>> import datetime
    >>> end = datetime.date(2025, 7, 7)
    >>> calculate_start_date(end, 10000)
    datetime.date(1998, 3, 11)
    >>> calculate_start_date(end, 10000, include_start=False)
    datetime.date(1998, 3, 10)
    """
    return _calculator.calculate_start_date(end_date, days, include_start)

def calculate_end_date(
    start_date: datetime.date,
    days: int,
    include_start: bool = DEFAULT_INCLUDE_START
) -> datetime.date:
    """Calculate the end date given a start date and number of days.
    
    This is a convenience function that wraps the DateCalculator method.
    
    Parameters
    ----------
    start_date : datetime.date
        The starting date
    days : int
        The number of days to add
    include_start : bool, optional
        Whether the start date is included in the count, by default True
        
    Returns
    -------
    datetime.date
        The calculated end date. If include_start is True, the end date
        will be start_date + (days - 1). If False, it will be 
        start_date + days.
        
    Raises
    ------
    ValueError
        If days is negative
        
    Examples
    --------
    >>> import datetime
    >>> start = datetime.date(1989, 1, 28)
    >>> calculate_end_date(start, 10000)
    datetime.date(2016, 6, 14)
    >>> calculate_end_date(start, 10000, include_start=False)
    datetime.date(2016, 6, 15)
    """
    return _calculator.calculate_end_date(start_date, days, include_start)