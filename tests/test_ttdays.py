
from datetime import date

import pytest

from ttdays import (
    DateCalculator,
    DateCalculationRequest,
    calculate_days_from_dates,
    calculate_end_date,
    calculate_start_date
)


class TestDateCalculationRequest:
    """Test cases for DateCalculationRequest model."""
    
    def test_valid_request_creation(self):
        """Test creating a valid DateCalculationRequest."""
        request = DateCalculationRequest(
            start_date=date(2024, 1, 1),
            end_date=date(2024, 1, 3),
            days=3,
            include_start=True
        )
        assert request.start_date == date(2024, 1, 1)
        assert request.end_date == date(2024, 1, 3)
        assert request.days == 3
        assert request.include_start is True
    
    def test_negative_days_raises_error(self):
        """Test that negative days raise ValueError."""
        with pytest.raises(ValueError, match="Days must be non-negative"):
            DateCalculationRequest(days=-1)
    
    def test_start_after_end_raises_error(self):
        """Test that start_date after end_date raises ValueError."""
        with pytest.raises(ValueError, match="Start date cannot be after end date"):
            DateCalculationRequest(
                start_date=date(2024, 1, 3),
                end_date=date(2024, 1, 1)
            )
    
    def test_zero_days_allowed(self):
        """Test that zero days is allowed."""
        request = DateCalculationRequest(days=0)
        assert request.days == 0


class TestDateCalculator:
    """Test cases for DateCalculator class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.calculator = DateCalculator()
    
    def test_calculate_days_from_dates_include_start(self):
        """Test calculating days between dates with start included."""
        start = date(2024, 1, 1)
        end = date(2024, 1, 3)
        result = self.calculator.calculate_days_from_dates(start, end, include_start=True)
        assert result == 3
    
    def test_calculate_days_from_dates_exclude_start(self):
        """Test calculating days between dates with start excluded."""
        start = date(2024, 1, 1)
        end = date(2024, 1, 3)
        result = self.calculator.calculate_days_from_dates(start, end, include_start=False)
        assert result == 2
    
    def test_calculate_days_same_date_include_start(self):
        """Test calculating days for same date with start included."""
        start = date(2024, 1, 1)
        end = date(2024, 1, 1)
        result = self.calculator.calculate_days_from_dates(start, end, include_start=True)
        assert result == 1
    
    def test_calculate_days_same_date_exclude_start(self):
        """Test calculating days for same date with start excluded."""
        start = date(2024, 1, 1)
        end = date(2024, 1, 1)
        result = self.calculator.calculate_days_from_dates(start, end, include_start=False)
        assert result == 0
    
    def test_calculate_days_start_after_end_raises_error(self):
        """Test that start date after end date raises ValueError."""
        start = date(2024, 1, 3)
        end = date(2024, 1, 1)
        with pytest.raises(ValueError, match="Start date cannot be after end date"):
            self.calculator.calculate_days_from_dates(start, end)
    
    def test_calculate_end_date_include_start(self):
        """Test calculating end date with start included."""
        start = date(2024, 1, 1)
        result = self.calculator.calculate_end_date(start, 3, include_start=True)
        assert result == date(2024, 1, 3)
    
    def test_calculate_end_date_exclude_start(self):
        """Test calculating end date with start excluded."""
        start = date(2024, 1, 1)
        result = self.calculator.calculate_end_date(start, 3, include_start=False)
        assert result == date(2024, 1, 4)
    
    def test_calculate_end_date_zero_days_include_start(self):
        """Test calculating end date with zero days and start included."""
        start = date(2024, 1, 1)
        result = self.calculator.calculate_end_date(start, 0, include_start=True)
        assert result == date(2023, 12, 31)
    
    def test_calculate_end_date_zero_days_exclude_start(self):
        """Test calculating end date with zero days and start excluded."""
        start = date(2024, 1, 1)
        result = self.calculator.calculate_end_date(start, 0, include_start=False)
        assert result == date(2024, 1, 1)
    
    def test_calculate_end_date_negative_days_raises_error(self):
        """Test that negative days raise ValueError."""
        start = date(2024, 1, 1)
        with pytest.raises(ValueError, match="Days must be non-negative"):
            self.calculator.calculate_end_date(start, -1)
    
    def test_calculate_start_date_include_start(self):
        """Test calculating start date with start included."""
        end = date(2024, 1, 3)
        result = self.calculator.calculate_start_date(end, 3, include_start=True)
        assert result == date(2024, 1, 1)
    
    def test_calculate_start_date_exclude_start(self):
        """Test calculating start date with start excluded."""
        end = date(2024, 1, 3)
        result = self.calculator.calculate_start_date(end, 3, include_start=False)
        assert result == date(2023, 12, 31)
    
    def test_calculate_start_date_zero_days_include_start(self):
        """Test calculating start date with zero days and start included."""
        end = date(2024, 1, 1)
        result = self.calculator.calculate_start_date(end, 0, include_start=True)
        assert result == date(2024, 1, 2)
    
    def test_calculate_start_date_zero_days_exclude_start(self):
        """Test calculating start date with zero days and start excluded."""
        end = date(2024, 1, 1)
        result = self.calculator.calculate_start_date(end, 0, include_start=False)
        assert result == date(2024, 1, 1)
    
    def test_calculate_start_date_negative_days_raises_error(self):
        """Test that negative days raise ValueError."""
        end = date(2024, 1, 3)
        with pytest.raises(ValueError, match="Days must be non-negative"):
            self.calculator.calculate_start_date(end, -1)


class TestModuleFunctions:
    """Test cases for module-level functions."""
    
    def test_calculate_days_from_dates_function(self):
        """Test module-level calculate_days_from_dates function."""
        start = date(2024, 1, 1)
        end = date(2024, 1, 3)
        result = calculate_days_from_dates(start, end)
        assert result == 3
    
    def test_calculate_end_date_function(self):
        """Test module-level calculate_end_date function."""
        start = date(2024, 1, 1)
        result = calculate_end_date(start, 3)
        assert result == date(2024, 1, 3)
    
    def test_calculate_start_date_function(self):
        """Test module-level calculate_start_date function."""
        end = date(2024, 1, 3)
        result = calculate_start_date(end, 3)
        assert result == date(2024, 1, 1)


class TestBoundaryConditions:
    """Test boundary conditions and edge cases."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.calculator = DateCalculator()
    
    def test_leap_year_calculation(self):
        """Test calculations across leap year boundaries."""
        start = date(2024, 2, 28)  # 2024 is a leap year
        end = date(2024, 3, 1)
        result = self.calculator.calculate_days_from_dates(start, end, include_start=True)
        assert result == 3  # Feb 28, Feb 29, Mar 1
    
    def test_year_boundary_calculation(self):
        """Test calculations across year boundaries."""
        start = date(2023, 12, 31)
        end = date(2024, 1, 2)
        result = self.calculator.calculate_days_from_dates(start, end, include_start=True)
        assert result == 3  # Dec 31, Jan 1, Jan 2
    
    def test_month_boundary_calculation(self):
        """Test calculations across month boundaries."""
        start = date(2024, 1, 31)
        end = date(2024, 2, 2)
        result = self.calculator.calculate_days_from_dates(start, end, include_start=True)
        assert result == 3  # Jan 31, Feb 1, Feb 2
    
    def test_large_day_calculation(self):
        """Test calculations with large number of days."""
        start = date(2024, 1, 1)
        result = self.calculator.calculate_end_date(start, 365, include_start=True)
        assert result == date(2024, 12, 30)  # 365日目は12月30日（2024年はうるう年で366日ある）
    
    def test_roundtrip_consistency(self):
        """Test that calculations are consistent when chained."""
        start = date(2024, 1, 1)
        end = date(2024, 1, 10)
        
        # Calculate days from dates
        days = self.calculator.calculate_days_from_dates(start, end)
        
        # Calculate end date from start and days
        calculated_end = self.calculator.calculate_end_date(start, days)
        
        # Calculate start date from end and days
        calculated_start = self.calculator.calculate_start_date(end, days)
        
        assert calculated_end == end
        assert calculated_start == start
