# date_model.py
import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator, model_validator, computed_field


class NullableDate(BaseModel):
    """
    A nullable date model that can handle partial date information.
    
    This model allows for incomplete date information where only year is required,
    month is optional, and day is optional but requires month to be present.
    A complete datetime.date object is automatically computed when all components
    are available.
    
    Attributes
    ----------
    year : int
        The year component (required)
    month : Optional[int]
        The month component (1-12, optional)
    day : Optional[int]
        The day component (1-31, optional, requires month)
    date : Optional[datetime.date]
        Complete date object, computed when year, month, and day are all present
    
    Examples
    --------
    >>> # Year only
    >>> partial_date = NullableDate(year=2023)
    >>> 
    >>> # Year and month
    >>> partial_date = NullableDate(year=2023, month=12)
    >>> 
    >>> # Complete date
    >>> complete_date = NullableDate(year=2023, month=12, day=25)
    >>> print(complete_date.date)  # 2023-12-25
    """
    
    year: int = Field(ge=1, le=9999)
    month: Optional[int] = Field(None, ge=1, le=12)
    day: Optional[int] = Field(None, ge=1, le=31)
    
    @field_validator('day')
    @classmethod
    def validate_day_requires_month_and_valid_date(cls, v: Optional[int], info) -> Optional[int]:
        """
        Validate that day is only provided when month is also provided,
        and that the combination forms a valid date.
        
        Parameters
        ----------
        v : Optional[int]
            The day value
        info : ValidationInfo
            Validation context containing other field values
            
        Returns
        -------
        Optional[int]
            The validated day value
            
        Raises
        ------
        ValueError
            If day is provided but month is not, or if the date is invalid
        """
        if v is not None:
            year = info.data.get('year')
            month = info.data.get('month')
            
            if month is None:
                raise ValueError('Day cannot be specified without month')
            
            # Check if the date is valid by attempting to create a datetime.date
            if year is not None and month is not None:
                try:
                    datetime.date(year, month, v)
                except ValueError:
                    raise ValueError(f'Invalid date: {year}-{month:02d}-{v:02d}')
        
        return v

    @computed_field
    @property
    def date(self) -> Optional[datetime.date]:
        """
        Compute a complete date object when all components are available.
        
        Returns
        -------
        Optional[date]
            A datetime.date object if year, month, and day are all present,
            None otherwise
            
        Raises
        ------
        ValueError
            If the date components form an invalid date
        """
        if self.year is not None and self.month is not None and self.day is not None:
            try:
                return datetime.date(self.year, self.month, self.day)
            except ValueError as e:
                raise ValueError(f"Invalid date: {e}")
        return None
    
    def __str__(self) -> str:
        """
        String representation of the flexible date.
        
        Returns
        -------
        str
            A string representation showing available date components
        """
        if self.date:
            return str(self.date)
        elif self.month:
            return f"{self.year}-{self.month:02d}"
        else:
            return str(self.year)
    
    def __repr__(self) -> str:
        """
        Detailed string representation for debugging.
        
        Returns
        -------
        str
            A detailed string representation of the object
        """
        return f"FlexibleDate(year={self.year}, month={self.month}, day={self.day})"


class DatePeriod(BaseModel):
    """Request model for date calculations with validation."""
    
    model_config = {"frozen": True, "extra": "forbid"}
    
    start_date: Optional[datetime.date] = Field(
        default=None, 
        description="The start date of the range"
    )
    end_date: Optional[datetime.date] = Field(
        default=None, 
        description="The end date of the range"
    )
    days: Optional[int] = Field(
        default=None,
        ge=0,
        le=1000000,
        description="Number of days for calculation (0 to 1000000)"
    )
    include_start: bool = Field(default=True, description="Whether to include the start date in the calculation")
    
    @model_validator(mode='after')
    def validate_date_consistency(self) -> 'DatePeriod':
        """Validate that start_date is not after end_date when both are provided.
        
        Returns
        -------
        DateModel
            The validated model instance
            
        Raises
        ------
        ValueError
            If start_date is after end_date
        """
        if (self.start_date is not None and 
            self.end_date is not None and 
            self.start_date > self.end_date):
            raise ValueError("Start date cannot be after end date")
        return self
    
    @model_validator(mode='after')
    def validate_required_fields(self) -> 'DatePeriod':
        """Validate that at least two of the three fields are provided.
        
        Returns
        -------
        DatePeriod
            The validated model instance
            
        Raises
        ------
        ValueError
            If less than two fields are provided
        """
        provided_fields = sum([
            self.start_date is not None,
            self.end_date is not None,
            self.days is not None
        ])
        
        if provided_fields < 2:
            raise ValueError("At least two of start_date, end_date, or days must be provided")
        
        return self