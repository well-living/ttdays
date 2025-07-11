# date_calculator.py
import datetime
from typing import Union

from .date_model import DatePeriod


class DateCalculator:
    """Calculator for date-related computations.
    
    This class provides methods to calculate missing date elements given
    two of the three parameters: start_date, end_date, and days.
    """
    
    def _parse_date(self, date_input: Union[datetime.date, str]) -> datetime.date:
        """Parse date input, converting string to datetime.date if necessary.
        
        Parameters
        ----------
        date_input : Union[datetime.date, str]
            Date as datetime.date object or string in YYYY-MM-DD format
            
        Returns
        -------
        datetime.date
            Parsed date object
            
        Raises
        ------
        ValueError
            If string format is invalid
        """
        if isinstance(date_input, str):
            try:
                return datetime.datetime.strptime(date_input, "%Y-%m-%d").date()
            except ValueError:
                raise ValueError(f"Invalid date format: {date_input}. Expected YYYY-MM-DD")
        return date_input
    
    def _calculate_days_offset(self, days: int, include_start: bool) -> int:
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
        self,
        start_date: Union[datetime.date, str],
        end_date: Union[datetime.date, str],
        include_start: bool = True
    ) -> int:
        """Calculate the number of days elapsed between start and end dates.
        
        Parameters
        ----------
        start_date : Union[datetime.date, str]
            The starting date (datetime.date object or YYYY-MM-DD string)
        end_date : Union[datetime.date, str]
            The ending date (datetime.date object or YYYY-MM-DD string)
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
            If start_date is after end_date or date format is invalid
            
        Examples
        --------
        >>> calc = DateCalculator()
        >>> start = datetime.date(1989, 1, 28)
        >>> end = datetime.date(2025, 7, 7)
        >>> calc.calculate_days_from_dates(start, end, include_start=True)
        13345
        >>> calc.calculate_days_from_dates("1989-01-28", "2025-07-07", include_start=False)
        13344
        """
        parsed_start = self._parse_date(start_date)
        parsed_end = self._parse_date(end_date)
        
        dm = DatePeriod(
            start_date=parsed_start,
            end_date=parsed_end,
            include_start=include_start
        )
        
        delta = dm.end_date - dm.start_date
        return delta.days + (1 if dm.include_start else 0)
    
    def calculate_start_date(
        self,
        end_date: Union[datetime.date, str],
        days: int,
        include_start: bool = True
    ) -> datetime.date:
        """Calculate the start date given an end date and number of days.
        
        Parameters
        ----------
        end_date : Union[datetime.date, str]
            The ending date (datetime.date object or YYYY-MM-DD string)
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
            If days is negative or date format is invalid
            
        Examples
        --------
        >>> calc = DateCalculator()
        >>> end = datetime.date(2025, 7, 7)
        >>> calc.calculate_start_date(end, 10000, include_start=True)
        datetime.date(1998, 3, 11)
        >>> calc.calculate_start_date("2025-07-07", 10000, include_start=False)
        datetime.date(1998, 3, 10)
        """
        parsed_end = self._parse_date(end_date)
        
        dm = DatePeriod(
            end_date=parsed_end,
            days=days,
            include_start=include_start
        )
        
        offset = self._calculate_days_offset(dm.days, dm.include_start)
        return dm.end_date - datetime.timedelta(days=offset)

    def calculate_end_date(
        self,
        start_date: Union[datetime.date, str],
        days: int,
        include_start: bool = True
    ) -> datetime.date:
        """Calculate the end date given a start date and number of days.
        
        Parameters
        ----------
        start_date : Union[datetime.date, str]
            The starting date (datetime.date object or YYYY-MM-DD string)
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
            If days is negative or date format is invalid
            
        Examples
        --------
        >>> calc = DateCalculator()
        >>> start = datetime.date(1989, 1, 28)
        >>> calc.calculate_end_date(start, 10000, include_start=True)
        datetime.date(2016, 6, 14)
        >>> calc.calculate_end_date("1989-01-28", 10000, include_start=False)
        datetime.date(2016, 6, 15)
        """
        parsed_start = self._parse_date(start_date)
        
        dm = DatePeriod(
            start_date=parsed_start,
            days=days,
            include_start=include_start
        )
        
        offset = self._calculate_days_offset(dm.days, dm.include_start)
        return dm.start_date + datetime.timedelta(days=offset)