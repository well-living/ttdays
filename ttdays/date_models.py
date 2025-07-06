from datetime import date
from typing import Optional

from pydantic import BaseModel, field_validator, model_validator


class DateCalculationRequest(BaseModel):
    """Request model for date calculations with validation."""
    
    model_config = {"frozen": True, "extra": "forbid"}
    
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    days: Optional[int] = None
    include_start: bool = True
    
    @field_validator('days')
    @classmethod
    def validate_days(cls, v: Optional[int]) -> Optional[int]:
        """Validate that days is non-negative when provided.
        
        Parameters
        ----------
        v : Optional[int]
            The days value to validate
            
        Returns
        -------
        Optional[int]
            The validated days value
            
        Raises
        ------
        ValueError
            If days is negative
        """
        if v is not None and v < 0:
            raise ValueError("Days must be non-negative")
        return v
    
    @model_validator(mode='after')
    def validate_date_consistency(self) -> 'DateCalculationRequest':
        """Validate that start_date is not after end_date when both are provided.
        
        Returns
        -------
        DateCalculationRequest
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
