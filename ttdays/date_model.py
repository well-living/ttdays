import datetime
from typing import Optional

from pydantic import BaseModel, Field, model_validator


class DateModel(BaseModel):
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
        description="Number of days for calculation (0 to 365)"
    )
    include_start: bool = Field(default=True, description="Whether to include the start date in the calculation")
    
    @model_validator(mode='after')
    def validate_date_consistency(self) -> 'DateModel':
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
