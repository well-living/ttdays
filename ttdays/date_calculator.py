# ttdays/date_calculator.py
import datetime
from typing import Union, Optional
from dateutil.relativedelta import relativedelta

from .date_model import DatePeriod, NullableDate


def _complete_nullable_date(
    nullable_date: NullableDate, 
    day: Optional[int] = None,
    date_position: str = "year_mid"
) -> datetime.date:
    """Complete a NullableDate to a full datetime.date object.
    
    Parameters
    ----------
    nullable_date : NullableDate
        The nullable date to complete
    day : Optional[int], optional
        Specific day to use when month is present but day is missing
    date_position : str, optional
        Position within year when only year is available, by default "year_mid"
        Options: "year_start"/"YS" (Jan 1), "year_mid"/"YM" (Jul 1), "year_end"/"YE" (Dec 31)
        
    Returns
    -------
    datetime.date
        Complete date object
        
    Raises
    ------
    ValueError
        If date_position is invalid or resulting date is invalid
    """
    if nullable_date.date is not None:
        # Already complete
        return nullable_date.date
    
    year = nullable_date.year
    month = nullable_date.month
    
    if month is not None:
        # Year and month present, need day
        target_day = day if day is not None else 1
        try:
            return datetime.date(year, month, target_day)
        except ValueError:
            raise ValueError(f"Invalid date: {year}-{month:02d}-{target_day:02d}")
    else:
        # Only year present, need month and day based on position
        position_map = {
            "year_start": (1, 1),   # January 1
            "YS": (1, 1),
            "year_mid": (7, 1),     # July 1  
            "YM": (7, 1),
            "year_end": (12, 31),   # December 31
            "YE": (12, 31)
        }
        
        if date_position not in position_map:
            raise ValueError(f"Invalid date_position: {date_position}. "
                           f"Options: {list(position_map.keys())}")
        
        target_month, target_day = position_map[date_position]
        return datetime.date(year, target_month, target_day)


def _parse_date(
    date_input: Union[datetime.date, str, NullableDate], 
    day: Optional[int] = None,
    date_position: str = "year_mid"
) -> datetime.date:
    """Parse date input, converting string or NullableDate to datetime.date if necessary.
    
    Parameters
    ----------
    date_input : Union[datetime.date, str, NullableDate]
        Date as datetime.date object, string, or NullableDate
    day : Optional[int], optional
        Specific day to use for incomplete dates
    date_position : str, optional
        Position within year for year-only dates, by default "year_mid"
        
    Returns
    -------
    datetime.date
        Parsed date object
        
    Raises
    ------
    ValueError
        If string format is invalid or date cannot be completed
    """
    if isinstance(date_input, datetime.date):
        return date_input
    elif isinstance(date_input, NullableDate):
        return _complete_nullable_date(date_input, day, date_position)
    elif isinstance(date_input, str):
        # Parse string into NullableDate first, then complete it
        parts = date_input.split('-')
        if len(parts) == 1:
            # Year only: "2023"
            try:
                year = int(parts[0])
                nullable_date = NullableDate(year=year)
                return _complete_nullable_date(nullable_date, day, date_position)
            except ValueError:
                raise ValueError(f"Invalid year format: {date_input}")
        elif len(parts) == 2:
            # Year-month: "2023-12"
            try:
                year, month = int(parts[0]), int(parts[1])
                nullable_date = NullableDate(year=year, month=month)
                return _complete_nullable_date(nullable_date, day, date_position)
            except ValueError:
                raise ValueError(f"Invalid year-month format: {date_input}")
        elif len(parts) == 3:
            # Full date: "2023-12-25"
            try:
                return datetime.datetime.strptime(date_input, "%Y-%m-%d").date()
            except ValueError:
                raise ValueError(f"Invalid date format: {date_input}. Expected YYYY-MM-DD")
        else:
            raise ValueError(f"Invalid date format: {date_input}. Expected YYYY, YYYY-MM, or YYYY-MM-DD")
    else:
        raise ValueError(f"Unsupported date input type: {type(date_input)}")


def _calculate_days_offset(days: int, include_start: bool) -> int:
    """Calculate the offset for date calculations based on include_start flag.
    
    Parameters
    ----------
    days : int
        Number of days
    include_start : bool
        Whether to include the start date in the count
        
    Returns
    -------
    int
        Offset value for timedelta calculation
    """
    return days - (1 if include_start else 0)


def calculate_days_from_dates(
    start_date: Union[datetime.date, str, NullableDate],
    end_date: Union[datetime.date, str, NullableDate],
    include_start: bool = True,
    start_day: Optional[int] = None,
    start_date_position: str = "year_mid",
    end_day: Optional[int] = None,
    end_date_position: str = "year_mid"
) -> int:
    """Calculate the number of days elapsed between start and end dates.
    
    Parameters
    ----------
    start_date : Union[datetime.date, str, NullableDate]
        The starting date (datetime.date object, YYYY/YYYY-MM/YYYY-MM-DD string, or NullableDate)
    end_date : Union[datetime.date, str, NullableDate]
        The ending date (datetime.date object, YYYY/YYYY-MM/YYYY-MM-DD string, or NullableDate)
    include_start : bool, optional
        Whether to include the start date in the count, by default True
    start_day : Optional[int], optional
        Specific day for start_date when incomplete
    start_date_position : str, optional
        Position for year-only start_date, by default "year_mid"
        Options: "year_start"/"YS", "year_mid"/"YM", "year_end"/"YE"
    end_day : Optional[int], optional
        Specific day for end_date when incomplete
    end_date_position : str, optional
        Position for year-only end_date, by default "year_mid"
        
    Returns
    -------
    int
        The number of days elapsed. If include_start is True, the count
        includes the start date. If False, it excludes the start date.
        
    Raises
    ------
    ValueError
        If start_date is after end_date or date format is invalid
        
    Examples
    --------
    >>> calculate_days_from_dates("1989-01-28", "2025-07-07", include_start=True)
    13345
    >>> calculate_days_from_dates("2023", "2024", start_date_position="year_start", end_date_position="year_start")
    366
    """
    parsed_start = _parse_date(start_date, start_day, start_date_position)
    parsed_end = _parse_date(end_date, end_day, end_date_position)
    
    dm = DatePeriod(
        start_date=parsed_start,
        end_date=parsed_end,
        include_start=include_start
    )
    
    delta = dm.end_date - dm.start_date
    return delta.days + (1 if dm.include_start else 0)


def calculate_months_from_dates(
    start_date: Union[datetime.date, str, NullableDate],
    end_date: Union[datetime.date, str, NullableDate],
    include_start: bool = True,
    start_day: Optional[int] = None,
    start_date_position: str = "year_mid",
    end_day: Optional[int] = None,
    end_date_position: str = "year_mid"
) -> int:
    """Calculate the number of months elapsed between start and end dates.
    
    Parameters
    ----------
    start_date : Union[datetime.date, str, NullableDate]
        The starting date (datetime.date object, YYYY/YYYY-MM/YYYY-MM-DD string, or NullableDate)
    end_date : Union[datetime.date, str, NullableDate]
        The ending date (datetime.date object, YYYY/YYYY-MM/YYYY-MM-DD string, or NullableDate)
    include_start : bool, optional
        Whether to include the start date in the count, by default True
    start_day : Optional[int], optional
        Specific day for start_date when incomplete
    start_date_position : str, optional
        Position for year-only start_date, by default "year_mid"
    end_day : Optional[int], optional
        Specific day for end_date when incomplete
    end_date_position : str, optional
        Position for year-only end_date, by default "year_mid"
        
    Returns
    -------
    int
        The number of months elapsed
        
    Raises
    ------
    ValueError
        If start_date is after end_date or date format is invalid
        
    Examples
    --------
    >>> calculate_months_from_dates("2023-01", "2025-07", include_start=True)
    30
    """
    parsed_start = _parse_date(start_date, start_day, start_date_position)
    parsed_end = _parse_date(end_date, end_day, end_date_position)
    
    dm = DatePeriod(
        start_date=parsed_start,
        end_date=parsed_end,
        include_start=include_start
    )
    
    delta = relativedelta(dm.end_date, dm.start_date)
    months = delta.years * 12 + delta.months
    
    # Handle partial months based on days
    if delta.days > 0:
        months += 1
    
    return months + (1 if dm.include_start and months == 0 else 0)


def calculate_years_from_dates(
    start_date: Union[datetime.date, str, NullableDate],
    end_date: Union[datetime.date, str, NullableDate],
    include_start: bool = True,
    start_day: Optional[int] = None,
    start_date_position: str = "year_mid",
    end_day: Optional[int] = None,
    end_date_position: str = "year_mid"
) -> int:
    """Calculate the number of years elapsed between start and end dates.
    
    Parameters
    ----------
    start_date : Union[datetime.date, str, NullableDate]
        The starting date (datetime.date object, YYYY/YYYY-MM/YYYY-MM-DD string, or NullableDate)
    end_date : Union[datetime.date, str, NullableDate]
        The ending date (datetime.date object, YYYY/YYYY-MM/YYYY-MM-DD string, or NullableDate)
    include_start : bool, optional
        Whether to include the start date in the count, by default True
    start_day : Optional[int], optional
        Specific day for start_date when incomplete
    start_date_position : str, optional
        Position for year-only start_date, by default "year_mid"
    end_day : Optional[int], optional
        Specific day for end_date when incomplete
    end_date_position : str, optional
        Position for year-only end_date, by default "year_mid"
        
    Returns
    -------
    int
        The number of years elapsed
        
    Raises
    ------
    ValueError
        If start_date is after end_date or date format is invalid
        
    Examples
    --------
    >>> calculate_years_from_dates("2020", "2025", start_date_position="year_start", end_date_position="year_start")
    5
    """
    parsed_start = _parse_date(start_date, start_day, start_date_position)
    parsed_end = _parse_date(end_date, end_day, end_date_position)
    
    dm = DatePeriod(
        start_date=parsed_start,
        end_date=parsed_end,
        include_start=include_start
    )
    
    delta = relativedelta(dm.end_date, dm.start_date)
    years = delta.years
    
    # Handle partial years
    if delta.months > 0 or delta.days > 0:
        years += 1
    
    return years + (1 if dm.include_start and years == 0 else 0)


def calculate_start_date(
    end_date: Union[datetime.date, str, NullableDate],
    days: int,
    include_start: bool = True,
    end_day: Optional[int] = None,
    end_date_position: str = "year_mid"
) -> datetime.date:
    """Calculate the start date given an end date and number of days.
    
    Parameters
    ----------
    end_date : Union[datetime.date, str, NullableDate]
        The ending date (datetime.date object, YYYY/YYYY-MM/YYYY-MM-DD string, or NullableDate)
    days : int
        The number of days to subtract
    include_start : bool, optional
        Whether the start date is included in the count, by default True
    end_day : Optional[int], optional
        Specific day for end_date when incomplete
    end_date_position : str, optional
        Position for year-only end_date, by default "year_mid"
        
    Returns
    -------
    datetime.date
        The calculated start date. If include_start is True, the start date
        will be end_date - (days - 1). If False, it will be end_date - days.
        
    Raises
    ------
    ValueError
        If days is negative or date format is invalid
        
    Examples
    --------
    >>> calculate_start_date("2025-07-07", 10000, include_start=True)
    datetime.date(1998, 3, 11)
    >>> calculate_start_date("2025", 365, include_start=True, end_date_position="year_end")
    datetime.date(2023, 12, 31)
    """
    parsed_end = _parse_date(end_date, end_day, end_date_position)
    
    dm = DatePeriod(
        end_date=parsed_end,
        days=days,
        include_start=include_start
    )
    
    offset = _calculate_days_offset(dm.days, dm.include_start)
    return dm.end_date - datetime.timedelta(days=offset)


def calculate_start_date_from_months(
    end_date: Union[datetime.date, str, NullableDate],
    months: int,
    include_start: bool = True,
    end_day: Optional[int] = None,
    end_date_position: str = "year_mid"
) -> datetime.date:
    """Calculate the start date given an end date and number of months.
    
    Parameters
    ----------
    end_date : Union[datetime.date, str, NullableDate]
        The ending date (datetime.date object, YYYY/YYYY-MM/YYYY-MM-DD string, or NullableDate)
    months : int
        The number of months to subtract
    include_start : bool, optional
        Whether the start date is included in the count, by default True
    end_day : Optional[int], optional
        Specific day for end_date when incomplete
    end_date_position : str, optional
        Position for year-only end_date, by default "year_mid"
        
    Returns
    -------
    datetime.date
        The calculated start date
        
    Raises
    ------
    ValueError
        If months is negative or date format is invalid
        
    Examples
    --------
    >>> calculate_start_date_from_months("2025-07", 12, include_start=True)
    datetime.date(2024, 8, 1)
    """
    parsed_end = _parse_date(end_date, end_day, end_date_position)
    
    dm = DatePeriod(
        end_date=parsed_end,
        months=months,
        include_start=include_start
    )
    
    offset_months = months - (1 if dm.include_start else 0)
    return dm.end_date - relativedelta(months=offset_months)


def calculate_start_date_from_years(
    end_date: Union[datetime.date, str, NullableDate],
    years: int,
    include_start: bool = True,
    end_day: Optional[int] = None,
    end_date_position: str = "year_mid"
) -> datetime.date:
    """Calculate the start date given an end date and number of years.
    
    Parameters
    ----------
    end_date : Union[datetime.date, str, NullableDate]
        The ending date (datetime.date object, YYYY/YYYY-MM/YYYY-MM-DD string, or NullableDate)
    years : int
        The number of years to subtract
    include_start : bool, optional
        Whether the start date is included in the count, by default True
    end_day : Optional[int], optional
        Specific day for end_date when incomplete
    end_date_position : str, optional
        Position for year-only end_date, by default "year_mid"
        
    Returns
    -------
    datetime.date
        The calculated start date
        
    Raises
    ------
    ValueError
        If years is negative or date format is invalid
        
    Examples
    --------
    >>> calculate_start_date_from_years("2025", 5, include_start=True, end_date_position="year_end")
    datetime.date(2020, 12, 31)
    """
    parsed_end = _parse_date(end_date, end_day, end_date_position)
    
    dm = DatePeriod(
        end_date=parsed_end,
        years=years,
        include_start=include_start
    )
    
    offset_years = years - (1 if dm.include_start else 0)
    return dm.end_date - relativedelta(years=offset_years)


def calculate_end_date(
    start_date: Union[datetime.date, str, NullableDate],
    days: int,
    include_start: bool = True,
    start_day: Optional[int] = None,
    start_date_position: str = "year_mid"
) -> datetime.date:
    """Calculate the end date given a start date and number of days.
    
    Parameters
    ----------
    start_date : Union[datetime.date, str, NullableDate]
        The starting date (datetime.date object, YYYY/YYYY-MM/YYYY-MM-DD string, or NullableDate)
    days : int
        The number of days to add
    include_start : bool, optional
        Whether the start date is included in the count, by default True
    start_day : Optional[int], optional
        Specific day for start_date when incomplete
    start_date_position : str, optional
        Position for year-only start_date, by default "year_mid"
        
    Returns
    -------
    datetime.date
        The calculated end date. If include_start is True, the end date
        will be start_date + (days - 1). If False, it will be 
        start_date + days.
        
    Raises
    ------
    ValueError
        If days is negative or date format is invalid
        
    Examples
    --------
    >>> calculate_end_date("1989-01-28", 10000, include_start=True)
    datetime.date(2016, 6, 14)
    >>> calculate_end_date("2023", 365, include_start=True, start_date_position="year_start")
    datetime.date(2024, 1, 1)
    """
    parsed_start = _parse_date(start_date, start_day, start_date_position)
    
    dm = DatePeriod(
        start_date=parsed_start,
        days=days,
        include_start=include_start
    )
    
    offset = _calculate_days_offset(dm.days, dm.include_start)
    return dm.start_date + datetime.timedelta(days=offset)


def calculate_end_date_from_months(
    start_date: Union[datetime.date, str, NullableDate],
    months: int,
    include_start: bool = True,
    start_day: Optional[int] = None,
    start_date_position: str = "year_mid"
) -> datetime.date:
    """Calculate the end date given a start date and number of months.
    
    Parameters
    ----------
    start_date : Union[datetime.date, str, NullableDate]
        The starting date (datetime.date object, YYYY/YYYY-MM/YYYY-MM-DD string, or NullableDate)
    months : int
        The number of months to add
    include_start : bool, optional
        Whether the start date is included in the count, by default True
    start_day : Optional[int], optional
        Specific day for start_date when incomplete
    start_date_position : str, optional
        Position for year-only start_date, by default "year_mid"
        
    Returns
    -------
    datetime.date
        The calculated end date
        
    Raises
    ------
    ValueError
        If months is negative or date format is invalid
        
    Examples
    --------
    >>> calculate_end_date_from_months("2023-01", 12, include_start=True)
    datetime.date(2024, 1, 1)
    """
    parsed_start = _parse_date(start_date, start_day, start_date_position)
    
    dm = DatePeriod(
        start_date=parsed_start,
        months=months,
        include_start=include_start
    )
    
    offset_months = months - (1 if dm.include_start else 0)
    return dm.start_date + relativedelta(months=offset_months)


def calculate_end_date_from_years(
    start_date: Union[datetime.date, str, NullableDate],
    years: int,
    include_start: bool = True,
    start_day: Optional[int] = None,
    start_date_position: str = "year_mid"
) -> datetime.date:
    """Calculate the end date given a start date and number of years.
    
    Parameters
    ----------
    start_date : Union[datetime.date, str, NullableDate]
        The starting date (datetime.date object, YYYY/YYYY-MM/YYYY-MM-DD string, or NullableDate)
    years : int
        The number of years to add
    include_start : bool, optional
        Whether the start date is included in the count, by default True
    start_day : Optional[int], optional
        Specific day for start_date when incomplete
    start_date_position : str, optional
        Position for year-only start_date, by default "year_mid"
        
    Returns
    -------
    datetime.date
        The calculated end date
        
    Raises
    ------
    ValueError
        If years is negative or date format is invalid
        
    Examples
    --------
    >>> calculate_end_date_from_years("2020", 5, include_start=True, start_date_position="year_start")
    datetime.date(2025, 1, 1)
    """
    parsed_start = _parse_date(start_date, start_day, start_date_position)
    
    dm = DatePeriod(
        start_date=parsed_start,
        years=years,
        include_start=include_start
    )
    
    offset_years = years - (1 if dm.include_start else 0)
    return dm.start_date + relativedelta(years=offset_years)