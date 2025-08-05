# test_date_calculator.py
import datetime
import pytest
from pydantic import ValidationError

from ttdays.date_calculator import (
    _parse_date,
    _complete_nullable_date,
    _calculate_days_offset,
    calculate_days_from_dates,
    calculate_months_from_dates,
    calculate_years_from_dates,
    calculate_start_date,
    calculate_start_date_from_months,
    calculate_start_date_from_years,
    calculate_end_date,
    calculate_end_date_from_months,
    calculate_end_date_from_years
)
from ttdays.date_model import NullableDate


class TestHelperFunctions:
    """Test suite for helper functions."""
    
    # Tests for _complete_nullable_date function
    @pytest.mark.parametrize("nullable_date,day,date_position,expected", [
        # Complete date (should return as-is)
        (NullableDate(year=2023, month=12, day=25), None, "year_mid", datetime.date(2023, 12, 25)),
        
        # Year and month, with day parameter
        (NullableDate(year=2023, month=6), 15, "year_mid", datetime.date(2023, 6, 15)),
        (NullableDate(year=2023, month=2), 28, "year_mid", datetime.date(2023, 2, 28)),
        
        # Year and month, default day (1st)
        (NullableDate(year=2023, month=6), None, "year_mid", datetime.date(2023, 6, 1)),
        (NullableDate(year=2023, month=12), None, "year_mid", datetime.date(2023, 12, 1)),
        
        # Year only with different positions
        (NullableDate(year=2023), None, "year_start", datetime.date(2023, 1, 1)),
        (NullableDate(year=2023), None, "YS", datetime.date(2023, 1, 1)),
        (NullableDate(year=2023), None, "year_mid", datetime.date(2023, 7, 1)),
        (NullableDate(year=2023), None, "YM", datetime.date(2023, 7, 1)),
        (NullableDate(year=2023), None, "year_end", datetime.date(2023, 12, 31)),
        (NullableDate(year=2023), None, "YE", datetime.date(2023, 12, 31)),
    ])
    def test_complete_nullable_date_valid(self, nullable_date, day, date_position, expected):
        """Test _complete_nullable_date with valid inputs."""
        result = _complete_nullable_date(nullable_date, day, date_position)
        assert result == expected
    
    def test_complete_nullable_date_invalid_position(self):
        """Test _complete_nullable_date with invalid date_position."""
        nullable_date = NullableDate(year=2023)
        with pytest.raises(ValueError) as exc_info:
            _complete_nullable_date(nullable_date, None, "invalid_position")
        assert "Invalid date_position" in str(exc_info.value)
    
    def test_complete_nullable_date_invalid_day(self):
        """Test _complete_nullable_date with invalid day."""
        nullable_date = NullableDate(year=2023, month=2)
        with pytest.raises(ValueError) as exc_info:
            _complete_nullable_date(nullable_date, 30, "year_mid")  # Feb 30 doesn't exist
        assert "Invalid date" in str(exc_info.value)
    
    # Tests for _parse_date function
    @pytest.mark.parametrize("date_input,day,date_position,expected", [
        # datetime.date objects
        (datetime.date(2023, 1, 1), None, "year_mid", datetime.date(2023, 1, 1)),
        
        # Complete date strings
        ("2023-01-01", None, "year_mid", datetime.date(2023, 1, 1)),
        ("2023-12-31", None, "year_mid", datetime.date(2023, 12, 31)),
        ("2024-02-29", None, "year_mid", datetime.date(2024, 2, 29)),  # Leap year
        
        # Year-month strings
        ("2023-06", None, "year_mid", datetime.date(2023, 6, 1)),
        ("2023-06", 15, "year_mid", datetime.date(2023, 6, 15)),
        ("2023-02", 28, "year_mid", datetime.date(2023, 2, 28)),
        
        # Year-only strings
        ("2023", None, "year_start", datetime.date(2023, 1, 1)),
        ("2023", None, "year_mid", datetime.date(2023, 7, 1)),
        ("2023", None, "year_end", datetime.date(2023, 12, 31)),
        ("2023", None, "YS", datetime.date(2023, 1, 1)),
        ("2023", None, "YM", datetime.date(2023, 7, 1)),
        ("2023", None, "YE", datetime.date(2023, 12, 31)),
        
        # NullableDate objects
        (NullableDate(year=2023, month=12, day=25), None, "year_mid", datetime.date(2023, 12, 25)),
        (NullableDate(year=2023, month=6), 15, "year_mid", datetime.date(2023, 6, 15)),
        (NullableDate(year=2023), None, "year_start", datetime.date(2023, 1, 1)),
    ])
    def test_parse_date_valid_inputs(self, date_input, day, date_position, expected):
        """Test _parse_date with valid inputs."""
        result = _parse_date(date_input, day, date_position)
        assert result == expected
    
    @pytest.mark.parametrize("invalid_date", [
        "invalid-date",
        "2023-13-01",  # Invalid month
        "2023-01-32",  # Invalid day
        "23-01-01",    # Wrong format
        "2023/01/01",  # Wrong separator
        "",            # Empty string
        "2023-1-1-1",  # Too many parts
    ])
    def test_parse_date_invalid_inputs(self, invalid_date):
        """Test _parse_date with invalid string inputs."""
        with pytest.raises(ValueError) as exc_info:
            _parse_date(invalid_date)
        assert "Invalid" in str(exc_info.value)
    
    def test_parse_date_unsupported_type(self):
        """Test _parse_date with unsupported input type."""
        with pytest.raises(ValueError) as exc_info:
            _parse_date(123)  # Integer input
        assert "Unsupported date input type" in str(exc_info.value)
    
    # Tests for _calculate_days_offset function
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
        result = _calculate_days_offset(days, include_start)
        assert result == expected


class TestDateCalculationFunctions:
    """Test suite for date calculation functions."""
    
    # Tests for calculate_days_from_dates function
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
        result = calculate_days_from_dates(start_date, end_date, include_start)
        assert result == expected
    
    def test_calculate_days_from_dates_with_nullable_date(self):
        """Test calculate_days_from_dates with NullableDate inputs."""
        start_nullable = NullableDate(year=2023, month=1, day=1)
        end_nullable = NullableDate(year=2023, month=1, day=10)
        
        result = calculate_days_from_dates(start_nullable, end_nullable, include_start=True)
        assert result == 10
    
    def test_calculate_days_from_dates_with_year_positions(self):
        """Test calculate_days_from_dates with year position parameters."""
        # Year 2023 to year 2024, start to start
        result = calculate_days_from_dates(
            "2023", "2024",
            start_date_position="year_start",
            end_date_position="year_start",
            include_start=True
        )
        # From 2023-01-01 to 2024-01-01 inclusive
        expected = (datetime.date(2024, 1, 1) - datetime.date(2023, 1, 1)).days + 1
        assert result == expected
        
        # Year 2023 to year 2024, end to end
        result = calculate_days_from_dates(
            "2023", "2024",
            start_date_position="year_end",
            end_date_position="year_end",
            include_start=True
        )
        # From 2023-12-31 to 2024-12-31 inclusive
        expected = (datetime.date(2024, 12, 31) - datetime.date(2023, 12, 31)).days + 1
        assert result == expected
    
    def test_calculate_days_from_dates_with_partial_dates(self):
        """Test calculate_days_from_dates with partial date strings."""
        # Year-month strings with default day
        result = calculate_days_from_dates("2023-01", "2023-02", include_start=True)
        # From 2023-01-01 to 2023-02-01 inclusive
        expected = (datetime.date(2023, 2, 1) - datetime.date(2023, 1, 1)).days + 1
        assert result == expected
        
        # Year-month strings with specific days
        result = calculate_days_from_dates(
            "2023-01", "2023-02",
            start_day=15, end_day=15,
            include_start=True
        )
        # From 2023-01-15 to 2023-02-15 inclusive
        expected = (datetime.date(2023, 2, 15) - datetime.date(2023, 1, 15)).days + 1
        assert result == expected
    
    def test_calculate_days_from_dates_validation_error(self):
        """Test calculate_days_from_dates when DatePeriod raises ValidationError."""
        with pytest.raises(ValidationError):
            # This should fail because start_date > end_date
            calculate_days_from_dates("2023-01-10", "2023-01-01")
    
    # Tests for calculate_start_date function
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
    ])
    def test_calculate_start_date_valid(self, end_date, days, include_start, expected):
        """Test calculate_start_date with valid inputs."""
        result = calculate_start_date(end_date, days, include_start)
        assert result == expected
    
    def test_calculate_start_date_with_year_position(self):
        """Test calculate_start_date with year position parameter."""
        # End at year-end, calculate start
        result = calculate_start_date(
            "2024", 365,
            end_date_position="year_end",
            include_start=True
        )
        # From 2024-12-31, subtract 364 days (365-1 for include_start)
        expected = datetime.date(2024, 12, 31) - datetime.timedelta(days=364)
        assert result == expected
    
    def test_calculate_start_date_with_nullable_date(self):
        """Test calculate_start_date with NullableDate input."""
        end_nullable = NullableDate(year=2023, month=1, day=10)
        result = calculate_start_date(end_nullable, 5, include_start=True)
        assert result == datetime.date(2023, 1, 6)
    
    # Tests for calculate_end_date function
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
        
        # Zero days
        (datetime.date(2023, 1, 1), 0, True, datetime.date(2022, 12, 31)),
        (datetime.date(2023, 1, 1), 0, False, datetime.date(2023, 1, 1)),
    ])
    def test_calculate_end_date_valid(self, start_date, days, include_start, expected):
        """Test calculate_end_date with valid inputs."""
        result = calculate_end_date(start_date, days, include_start)
        assert result == expected
    
    def test_calculate_end_date_with_year_position(self):
        """Test calculate_end_date with year position parameter."""
        # Start at year-start, calculate end
        result = calculate_end_date(
            "2023", 365,
            start_date_position="year_start",
            include_start=True
        )
        # From 2023-01-01, add 364 days (365-1 for include_start)
        expected = datetime.date(2023, 1, 1) + datetime.timedelta(days=364)
        assert result == expected
    
    # Tests for months and years functions
    def test_calculate_months_from_dates(self):
        """Test calculate_months_from_dates function."""
        result = calculate_months_from_dates("2023-01-15", "2025-07-15", include_start=True)
        assert result >= 30  # Should be around 30 months
    
    def test_calculate_years_from_dates(self):
        """Test calculate_years_from_dates function."""
        result = calculate_years_from_dates("2020-01-15", "2025-07-15", include_start=True)
        assert result >= 5  # Should be around 5-6 years
    
    def test_calculate_start_date_from_months(self):
        """Test calculate_start_date_from_months function."""
        result = calculate_start_date_from_months("2025-07-15", 12, include_start=True)
        # Should be approximately 2024-08-15
        assert result.year == 2024
        assert result.month == 8
    
    def test_calculate_start_date_from_years(self):
        """Test calculate_start_date_from_years function."""
        result = calculate_start_date_from_years("2025-07-15", 5, include_start=True)
        # Should be approximately 2020-08-15
        assert result.year == 2020
        assert result.month == 8
    
    def test_calculate_end_date_from_months(self):
        """Test calculate_end_date_from_months function."""
        result = calculate_end_date_from_months("2023-01-15", 12, include_start=True)
        # Should be 2024-01-15
        assert result == datetime.date(2024, 1, 15)
    
    def test_calculate_end_date_from_years(self):
        """Test calculate_end_date_from_years function."""
        result = calculate_end_date_from_years("2020-01-15", 5, include_start=True)
        # Should be 2025-01-15
        assert result == datetime.date(2025, 1, 15)


class TestIntegrationAndEdgeCases:
    """Test suite for integration tests and edge cases."""
    
    def test_round_trip_calculations(self):
        """Test that calculations are consistent in round trips."""
        original_start = datetime.date(2023, 1, 1)
        original_end = datetime.date(2023, 1, 10)
        
        # Calculate days from dates
        days = calculate_days_from_dates(original_start, original_end, include_start=True)
        
        # Calculate start date from end date and days
        calculated_start = calculate_start_date(original_end, days, include_start=True)
        
        # Calculate end date from start date and days
        calculated_end = calculate_end_date(original_start, days, include_start=True)
        
        assert calculated_start == original_start
        assert calculated_end == original_end
    
    def test_leap_year_calculations(self):
        """Test calculations across leap year boundaries."""
        # Test leap year day (Feb 29, 2024)
        start_date = datetime.date(2024, 2, 28)
        end_date = datetime.date(2024, 3, 1)
        
        days = calculate_days_from_dates(start_date, end_date, include_start=True)
        assert days == 3  # Feb 28, Feb 29, Mar 1
        
        # Test non-leap year
        start_date = datetime.date(2023, 2, 28)
        end_date = datetime.date(2023, 3, 1)
        
        days = calculate_days_from_dates(start_date, end_date, include_start=True)
        assert days == 2  # Feb 28, Mar 1
    
    def test_large_days_calculation(self):
        """Test calculations with large numbers of days."""
        start_date = datetime.date(2000, 1, 1)
        large_days = 10000
        
        end_date = calculate_end_date(start_date, large_days, include_start=True)
        
        # Verify round trip
        calculated_days = calculate_days_from_dates(start_date, end_date, include_start=True)
        assert calculated_days == large_days
    
    def test_validation_errors(self):
        """Test that DatePeriod validation errors are properly raised."""
        # Negative days should raise ValidationError through DatePeriod
        with pytest.raises(ValidationError):
            calculate_end_date("2023-01-01", -5)
        
        with pytest.raises(ValidationError):
            calculate_start_date("2023-01-01", -5)
    
    def test_mixed_input_types(self):
        """Test functions with mixed input types."""
        # Mix datetime.date, string, and NullableDate
        start_datetime = datetime.date(2023, 1, 1)
        end_string = "2023-01-10"
        nullable_date = NullableDate(year=2023, month=1, day=5)
        
        # Test with different combinations
        result1 = calculate_days_from_dates(start_datetime, end_string, include_start=True)
        assert result1 == 10
        
        result2 = calculate_days_from_dates(start_datetime, nullable_date, include_start=True)
        assert result2 == 5
        
        result3 = calculate_days_from_dates(nullable_date, end_string, include_start=True)
        assert result3 == 6
    
    def test_docstring_examples(self):
        """Test the examples from function docstrings."""
        # Test calculate_days_from_dates examples
        result1 = calculate_days_from_dates("1989-01-28", "2025-07-07", include_start=True)
        result2 = calculate_days_from_dates("1989-01-28", "2025-07-07", include_start=False)
        assert result2 == result1 - 1
        
        # Test year position example
        result3 = calculate_days_from_dates(
            "2023", "2024",
            start_date_position="year_start",
            end_date_position="year_start"
        )
        assert result3 == 366  # 2024 is a leap year
        
        # Test calculate_start_date examples
        result4 = calculate_start_date("2025-07-07", 10000, include_start=True)
        result5 = calculate_start_date("2025-07-07", 10000, include_start=False)
        assert (result5 - result4).days == 1
    
    def test_error_handling_with_incomplete_dates(self):
        """Test error handling when dates cannot be completed."""
        # Test invalid day for February
        with pytest.raises(ValueError):
            calculate_days_from_dates(
                "2023-02", "2023-03",
                start_day=30  # Feb 30 doesn't exist  
            )
        
        # Test invalid date position
        with pytest.raises(ValueError):
            calculate_days_from_dates(
                "2023", "2024",
                start_date_position="invalid_position"
            )