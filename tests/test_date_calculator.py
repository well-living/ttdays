# test_date_calculator.py
import datetime
import pytest
from unittest.mock import patch, MagicMock
from pydantic import ValidationError

from ttdays.date_calculator import DateCalculator


class TestDateCalculator:
    """Test suite for DateCalculator class."""
    
    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.calculator = DateCalculator()
    
    # Tests for _parse_date method
    @pytest.mark.parametrize("date_input,expected", [
        (datetime.date(2023, 1, 1), datetime.date(2023, 1, 1)),
        ("2023-01-01", datetime.date(2023, 1, 1)),
        ("2023-12-31", datetime.date(2023, 12, 31)),
        ("2024-02-29", datetime.date(2024, 2, 29)),  # Leap year
        ("2023-1-1", datetime.date(2023, 1, 1)),    # Single digit month/day (actually valid)
    ])
    def test_parse_date_valid_inputs(self, date_input, expected):
        """Test _parse_date with valid inputs."""
        result = self.calculator._parse_date(date_input)
        assert result == expected
    
    @pytest.mark.parametrize("invalid_date", [
        "invalid-date",
        "2023-13-01",  # Invalid month
        "2023-01-32",  # Invalid day
        "23-01-01",    # Wrong format
        "2023/01/01",  # Wrong separator
        "",            # Empty string
    ])
    def test_parse_date_invalid_inputs(self, invalid_date):
        """Test _parse_date with invalid string inputs."""
        with pytest.raises(ValueError) as exc_info:
            self.calculator._parse_date(invalid_date)
        assert "Invalid date format" in str(exc_info.value)
        assert "Expected YYYY-MM-DD" in str(exc_info.value)
    
    # Tests for _calculate_days_offset method
    @pytest.mark.parametrize("days,include_start,expected", [
        (1, True, 0),    # 1 day, include start -> offset 0
        (1, False, 1),   # 1 day, exclude start -> offset 1
        (10, True, 9),   # 10 days, include start -> offset 9
        (10, False, 10), # 10 days, exclude start -> offset 10
        (0, True, -1),   # 0 days, include start -> offset -1
        (0, False, 0),   # 0 days, exclude start -> offset 0
    ])
    def test_calculate_days_offset(self, days, include_start, expected):
        """Test _calculate_days_offset with various inputs."""
        result = self.calculator._calculate_days_offset(days, include_start)
        assert result == expected
    
    # Tests for calculate_days_from_dates method
    @pytest.mark.parametrize("start_date,end_date,include_start,expected", [
        # Same date
        (datetime.date(2023, 1, 1), datetime.date(2023, 1, 1), True, 1),
        (datetime.date(2023, 1, 1), datetime.date(2023, 1, 1), False, 0),
        
        # Different dates
        (datetime.date(2023, 1, 1), datetime.date(2023, 1, 10), True, 10),
        (datetime.date(2023, 1, 1), datetime.date(2023, 1, 10), False, 9),
        
        # String inputs
        ("2023-01-01", "2023-01-10", True, 10),
        ("2023-01-01", "2023-01-10", False, 9),
        
        # Cross year boundary
        (datetime.date(2022, 12, 31), datetime.date(2023, 1, 1), True, 2),
        (datetime.date(2022, 12, 31), datetime.date(2023, 1, 1), False, 1),
        
        # Leap year
        (datetime.date(2024, 2, 28), datetime.date(2024, 3, 1), True, 3),
        (datetime.date(2024, 2, 28), datetime.date(2024, 3, 1), False, 2),
    ])
    def test_calculate_days_from_dates_valid(self, start_date, end_date, include_start, expected):
        """Test calculate_days_from_dates with valid inputs."""
        result = self.calculator.calculate_days_from_dates(start_date, end_date, include_start)
        assert result == expected
    
    def test_calculate_days_from_dates_docstring_examples(self):
        """Test the examples from the docstring."""
        start = datetime.date(1989, 1, 28)
        end = datetime.date(2025, 7, 7)
        
        # Calculate the actual expected values
        delta = end - start
        expected_with_start = delta.days + 1
        expected_without_start = delta.days
        
        # Example 1: include_start=True
        result1 = self.calculator.calculate_days_from_dates(start, end, include_start=True)
        assert result1 == expected_with_start
        
        # Example 2: include_start=False with string inputs
        result2 = self.calculator.calculate_days_from_dates("1989-01-28", "2025-07-07", include_start=False)
        assert result2 == expected_without_start
    
    def test_calculate_days_from_dates_invalid_date_strings(self):
        """Test calculate_days_from_dates with invalid date strings."""
        with pytest.raises(ValueError) as exc_info:
            self.calculator.calculate_days_from_dates("invalid-date", "2023-01-10")
        assert "Invalid date format" in str(exc_info.value)
    
    def test_calculate_days_from_dates_validation_error(self):
        """Test calculate_days_from_dates when DateModel raises ValidationError."""
        # Test with actual invalid data that would cause DateModel validation to fail
        with pytest.raises(ValidationError):
            # This should fail because start_date > end_date
            self.calculator.calculate_days_from_dates("2023-01-10", "2023-01-01")
    
    # Tests for calculate_start_date method
    @pytest.mark.parametrize("end_date,days,include_start,expected", [
        # Basic calculations
        (datetime.date(2023, 1, 10), 10, True, datetime.date(2023, 1, 1)),
        (datetime.date(2023, 1, 10), 10, False, datetime.date(2022, 12, 31)),
        
        # String input
        ("2023-01-10", 5, True, datetime.date(2023, 1, 6)),
        ("2023-01-10", 5, False, datetime.date(2023, 1, 5)),
        
        # Single day
        (datetime.date(2023, 1, 1), 1, True, datetime.date(2023, 1, 1)),
        (datetime.date(2023, 1, 1), 1, False, datetime.date(2022, 12, 31)),
        
        # Cross year boundary
        (datetime.date(2023, 1, 5), 10, True, datetime.date(2022, 12, 27)),
        (datetime.date(2023, 1, 5), 10, False, datetime.date(2022, 12, 26)),
        
        # Leap year
        (datetime.date(2024, 3, 1), 3, True, datetime.date(2024, 2, 28)),
        (datetime.date(2024, 3, 1), 3, False, datetime.date(2024, 2, 27)),
    ])
    def test_calculate_start_date_valid(self, end_date, days, include_start, expected):
        """Test calculate_start_date with valid inputs."""
        result = self.calculator.calculate_start_date(end_date, days, include_start)
        assert result == expected
    
    def test_calculate_start_date_docstring_examples(self):
        """Test the examples from the docstring."""
        end = datetime.date(2025, 7, 7)
        
        # Calculate the actual expected values
        # Example 1: include_start=True
        result1 = self.calculator.calculate_start_date(end, 10000, include_start=True)
        expected1 = end - datetime.timedelta(days=10000-1)
        assert result1 == expected1
        
        # Example 2: include_start=False with string input
        result2 = self.calculator.calculate_start_date("2025-07-07", 10000, include_start=False)
        expected2 = end - datetime.timedelta(days=10000)
        assert result2 == expected2
    
    def test_calculate_start_date_invalid_date_string(self):
        """Test calculate_start_date with invalid date string."""
        with pytest.raises(ValueError) as exc_info:
            self.calculator.calculate_start_date("invalid-date", 10)
        assert "Invalid date format" in str(exc_info.value)
    
    def test_calculate_start_date_validation_error(self):
        """Test calculate_start_date when DateModel raises ValidationError."""
        # Test with actual invalid data that would cause DateModel validation to fail
        with pytest.raises(ValidationError):
            # This should fail because of negative days (via DateModel validation)
            self.calculator.calculate_start_date("2023-01-10", -1)
    
    # Tests for calculate_end_date method
    @pytest.mark.parametrize("start_date,days,include_start,expected", [
        # Basic calculations
        (datetime.date(2023, 1, 1), 10, True, datetime.date(2023, 1, 10)),
        (datetime.date(2023, 1, 1), 10, False, datetime.date(2023, 1, 11)),
        
        # String input
        ("2023-01-01", 5, True, datetime.date(2023, 1, 5)),
        ("2023-01-01", 5, False, datetime.date(2023, 1, 6)),
        
        # Single day
        (datetime.date(2023, 1, 1), 1, True, datetime.date(2023, 1, 1)),
        (datetime.date(2023, 1, 1), 1, False, datetime.date(2023, 1, 2)),
        
        # Cross year boundary
        (datetime.date(2022, 12, 27), 10, True, datetime.date(2023, 1, 5)),
        (datetime.date(2022, 12, 27), 10, False, datetime.date(2023, 1, 6)),
        
        # Leap year
        (datetime.date(2024, 2, 28), 3, True, datetime.date(2024, 3, 1)),
        (datetime.date(2024, 2, 28), 3, False, datetime.date(2024, 3, 2)),
        
        # Zero days
        (datetime.date(2023, 1, 1), 0, True, datetime.date(2022, 12, 31)),
        (datetime.date(2023, 1, 1), 0, False, datetime.date(2023, 1, 1)),
    ])
    def test_calculate_end_date_valid(self, start_date, days, include_start, expected):
        """Test calculate_end_date with valid inputs."""
        result = self.calculator.calculate_end_date(start_date, days, include_start)
        assert result == expected
    
    def test_calculate_end_date_docstring_examples(self):
        """Test the examples from the docstring."""
        start = datetime.date(1989, 1, 28)
        
        # Calculate the actual expected values
        # Example 1: include_start=True
        result1 = self.calculator.calculate_end_date(start, 10000, include_start=True)
        expected1 = start + datetime.timedelta(days=10000-1)
        assert result1 == expected1
        
        # Example 2: include_start=False with string input
        result2 = self.calculator.calculate_end_date("1989-01-28", 10000, include_start=False)
        expected2 = start + datetime.timedelta(days=10000)
        assert result2 == expected2
    
    def test_calculate_end_date_invalid_date_string(self):
        """Test calculate_end_date with invalid date string."""
        with pytest.raises(ValueError) as exc_info:
            self.calculator.calculate_end_date("invalid-date", 10)
        assert "Invalid date format" in str(exc_info.value)
    
    def test_calculate_end_date_validation_error(self):
        """Test calculate_end_date when DateModel raises ValidationError."""
        # Test with actual invalid data that would cause DateModel validation to fail
        with pytest.raises(ValidationError):
            # This should fail because of negative days (via DateModel validation)
            self.calculator.calculate_end_date("2023-01-01", -1)
    
    # Integration tests with actual DateModel
    def test_integration_with_date_model(self):
        """Test integration with actual DateModel validation."""
        # Test that DateModel validation is properly triggered
        with pytest.raises(ValidationError):
            # This should fail because start_date > end_date after calculation
            self.calculator.calculate_days_from_dates("2023-01-10", "2023-01-01")
    
    def test_round_trip_calculations(self):
        """Test that calculations are consistent in round trips."""
        original_start = datetime.date(2023, 1, 1)
        original_end = datetime.date(2023, 1, 10)
        
        # Calculate days from dates
        days = self.calculator.calculate_days_from_dates(original_start, original_end, include_start=True)
        
        # Calculate start date from end date and days
        calculated_start = self.calculator.calculate_start_date(original_end, days, include_start=True)
        
        # Calculate end date from start date and days
        calculated_end = self.calculator.calculate_end_date(original_start, days, include_start=True)
        
        assert calculated_start == original_start
        assert calculated_end == original_end
    
    def test_edge_case_zero_days(self):
        """Test edge case with zero days."""
        start_date = datetime.date(2023, 1, 1)
        
        # When days=0 and include_start=True, end_date should be one day before start
        end_date = self.calculator.calculate_end_date(start_date, 0, include_start=True)
        assert end_date == datetime.date(2022, 12, 31)
        
        # When days=0 and include_start=False, end_date should be same as start
        end_date = self.calculator.calculate_end_date(start_date, 0, include_start=False)
        assert end_date == start_date
    
    def test_large_days_calculation(self):
        """Test calculations with large numbers of days."""
        start_date = datetime.date(2000, 1, 1)
        large_days = 10000
        
        end_date = self.calculator.calculate_end_date(start_date, large_days, include_start=True)
        
        # Verify round trip
        calculated_days = self.calculator.calculate_days_from_dates(start_date, end_date, include_start=True)
        assert calculated_days == large_days
    
    def test_leap_year_calculations(self):
        """Test calculations across leap year boundaries."""
        # Test leap year day (Feb 29, 2024)
        start_date = datetime.date(2024, 2, 28)
        end_date = datetime.date(2024, 3, 1)
        
        days = self.calculator.calculate_days_from_dates(start_date, end_date, include_start=True)
        assert days == 3  # Feb 28, Feb 29, Mar 1
        
        # Test non-leap year
        start_date = datetime.date(2023, 2, 28)
        end_date = datetime.date(2023, 3, 1)
        
        days = self.calculator.calculate_days_from_dates(start_date, end_date, include_start=True)
        assert days == 2  # Feb 28, Mar 1
    
    def test_method_chaining_compatibility(self):
        """Test that methods can be used in sequence for complex calculations."""
        # Calculate a date 30 days from today
        today = datetime.date.today()
        future_date = self.calculator.calculate_end_date(today, 30, include_start=True)
        
        # Calculate how many days between today and that future date
        days_between = self.calculator.calculate_days_from_dates(today, future_date, include_start=True)
        
        # Should be 30 days
        assert days_between == 30
    
    def test_negative_days_handling(self):
        """Test that negative days are handled through DateModel validation."""
        # DateModel should reject negative days
        with pytest.raises(ValidationError):
            self.calculator.calculate_end_date("2023-01-01", -5)
        
        with pytest.raises(ValidationError):
            self.calculator.calculate_start_date("2023-01-01", -5)