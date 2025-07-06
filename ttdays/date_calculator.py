
from datetime import date, timedelta
from typing import Union

from .date_models import DateCalculationRequest


class DateCalculator:
    """Calculator for date-related computations.
    
    This class provides methods to calculate missing date elements given
    two of the three parameters: start_date, end_date, and days.
    """
    
    def calculate_days_from_dates(
        self,
        start_date: date,
        end_date: date,
        include_start: bool = True
    ) -> int:
        """Calculate the number of days elapsed between start and end dates.
        
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
        >>> calc = DateCalculator()
        >>> start = date(2024, 1, 1)
        >>> end = date(2024, 1, 3)
        >>> calc.calculate_days_from_dates(start, end, include_start=True)
        3
        >>> calc.calculate_days_from_dates(start, end, include_start=False)
        2
        """
        request = DateCalculationRequest(
            start_date=start_date,
            end_date=end_date,
            include_start=include_start
        )
        
        delta = request.end_date - request.start_date
        days = delta.days
        
        if request.include_start:
            return days + 1
        else:
            return days
    
    def calculate_end_date(
        self,
        start_date: date,
        days: int,
        include_start: bool = True
    ) -> date:
        """Calculate the end date given a start date and number of days.
        
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
        >>> calc = DateCalculator()
        >>> start = date(2024, 1, 1)
        >>> calc.calculate_end_date(start, 3, include_start=True)
        datetime.date(2024, 1, 3)
        >>> calc.calculate_end_date(start, 3, include_start=False)
        datetime.date(2024, 1, 4)
        """
        request = DateCalculationRequest(
            start_date=start_date,
            days=days,
            include_start=include_start
        )
        
        if request.include_start:
            return request.start_date + timedelta(days=request.days - 1)
        else:
            return request.start_date + timedelta(days=request.days)
    
    def calculate_start_date(
        self,
        end_date: date,
        days: int,
        include_start: bool = True
    ) -> date:
        """Calculate the start date given an end date and number of days.
        
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
        >>> calc = DateCalculator()
        >>> end = date(2024, 1, 3)
        >>> calc.calculate_start_date(end, 3, include_start=True)
        datetime.date(2024, 1, 1)
        >>> calc.calculate_start_date(end, 3, include_start=False)
        datetime.date(2023, 12, 31)
        """
        request = DateCalculationRequest(
            end_date=end_date,
            days=days,
            include_start=include_start
        )
        
        if request.include_start:
            return request.end_date - timedelta(days=request.days - 1)
        else:
            return request.end_date - timedelta(days=request.days)