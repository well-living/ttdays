# test_functions.py
import datetime
import pytest
from unittest.mock import patch, MagicMock
from pydantic import ValidationError

import functions
from functions import (
    calculate_days_from_dates,
    calculate_start_date,
    calculate_end_date,
    DEFAULT_INCLUDE_START,
    _calculator
)


class TestModuleLevelConstants:
    """Test module-level constants."""
    
    def test_default_include_start_value(self):
        """Test that DEFAULT_INCLUDE_START is True."""
        assert DEFAULT_INCLUDE_START is True
        assert isinstance(DEFAULT_INCLUDE_START, bool)
    
    def test_calculator_instance_exists(self):
        """Test that module-level calculator instance exists."""
        assert _calculator is not None
        assert hasattr(_calculator, 'calculate_days_from_dates')
        assert hasattr(_calculator, 'calculate_start_date')
        assert hasattr(_calculator, 'calculate_end_date')


class TestCalculateDaysFromDates:
    """Test suite for calculate_days_from_dates function."""
    
    @pytest.mark.parametrize("start_date,end_date,include_start,expected", [
        # Basic cases
        (datetime.date(2023, 1, 1), datetime.date(2023, 1, 10), True, 10),
        (datetime.date(2023, 1, 1), datetime.date(2023, 1, 10), False, 9),
        
        # Same date
        (datetime.date(2023, 1, 1), datetime.date(2023, 1, 1), True, 1),
        (datetime.date(2023, 1, 1), datetime.date(2023, 1, 1), False, 0),
        
        # Cross year
        (datetime.date(2022, 12, 31), datetime.date(2023, 1, 2), True, 3),
        (datetime.date(2022, 12, 31), datetime.date(2023, 1, 2), False, 2),
    ])
    def test_calculate_days_from_dates_valid(self, start_date, end_date, include_start, expected):
        """Test calculate_days_from_dates with valid inputs."""
        result = calculate_days_from_dates(start_date, end_date, include_start)
        assert result == expected
    
    def test_calculate_days_from_dates_default_include_start(self):
        """Test that default include_start parameter works correctly."""
        start = datetime.date(2023, 1, 1)
        end = datetime.date(2023, 1, 10)
        
        # Should use DEFAULT_INCLUDE_START (True)
        result = calculate_days_from_dates(start, end)
        assert result == 10
        
        # Verify it's the same as explicitly passing True
        result_explicit = calculate_days_from_dates(start, end, include_start=True)
        assert result == result_explicit
    
    def test_calculate_days_from_dates_docstring_examples(self):
        """Test the examples from the docstring."""
        start = datetime.date(1989, 1, 28)
        end = datetime.date(2025, 7, 7)
        
        # Example 1: default include_start
        result1 = calculate_days_from_dates(start, end)
        assert result1 == 13345
        
        # Example 2: include_start=False
        result2 = calculate_days_from_dates(start, end, include_start=False)
        assert result2 == 13344
    
    @patch('functions._calculator.calculate_days_from_dates')
    def test_calculate_days_from_dates_delegates_to_calculator(self, mock_calc_method):
        """Test that function delegates to the calculator instance."""
        mock_calc_method.return_value = 42
        
        start = datetime.date(2023, 1, 1)
        end = datetime.date(2023, 1, 10)
        
        result = calculate_days_from_dates(start, end, include_start=False)
        
        # Verify the calculator method was called with correct arguments
        mock_calc_method.assert_called_once_with(start, end, False)
        assert result == 42
    
    @patch('functions._calculator.calculate_days_from_dates')
    def test_calculate_days_from_dates_propagates_exceptions(self, mock_calc_method):
        """Test that exceptions from calculator are properly propagated."""
        mock_calc_method.side_effect = ValidationError.from_exception_data(
            "DateModel",
            [{"type": "value_error", "loc": (), "msg": "Start date cannot be after end date"}]
        )
        
        with pytest.raises(ValidationError):
            calculate_days_from_dates(datetime.date(2023, 1, 10), datetime.date(2023, 1, 1))


class TestCalculateStartDate:
    """Test suite for calculate_start_date function."""
    
    @pytest.mark.parametrize("end_date,days,include_start,expected", [
        # Basic cases
        (datetime.date(2023, 1, 10), 10, True, datetime.date(2023, 1, 1)),
        (datetime.date(2023, 1, 10), 10, False, datetime.date(2022, 12, 31)),
        
        # Single day
        (datetime.date(2023, 1, 1), 1, True, datetime.date(2023, 1, 1)),
        (datetime.date(2023, 1, 1), 1, False, datetime.date(2022, 12, 31)),
        
        # Cross year
        (datetime.date(2023, 1, 5), 10, True, datetime.date(2022, 12, 27)),
        (datetime.date(2023, 1, 5), 10, False, datetime.date(2022, 12, 26)),
    ])
    def test_calculate_start_date_valid(self, end_date, days, include_start, expected):
        """Test calculate_start_date with valid inputs."""
        result = calculate_start_date(end_date, days, include_start)
        assert result == expected
    
    def test_calculate_start_date_default_include_start(self):
        """Test that default include_start parameter works correctly."""
        end = datetime.date(2023, 1, 10)
        days = 5
        
        # Should use DEFAULT_INCLUDE_START (True)
        result = calculate_start_date(end, days)
        assert result == datetime.date(2023, 1, 6)
        
        # Verify it's the same as explicitly passing True
        result_explicit = calculate_start_date(end, days, include_start=True)
        assert result == result_explicit
    
    def test_calculate_start_date_docstring_examples(self):
        """Test the examples from the docstring."""
        end = datetime.date(2025, 7, 7)
        
        # Example 1: default include_start
        result1 = calculate_start_date(end, 10000)
        assert result1 == datetime.date(1998, 3, 11)
        
        # Example 2: include_start=False
        result2 = calculate_start_date(end, 10000, include_start=False)
        assert result2 == datetime.date(1998, 3, 10)
    
    @patch('functions._calculator.calculate_start_date')
    def test_calculate_start_date_delegates_to_calculator(self, mock_calc_method):
        """Test that function delegates to the calculator instance."""
        mock_calc_method.return_value = datetime.date(2023, 1, 1)
        
        end = datetime.date(2023, 1, 10)
        days = 5
        
        result = calculate_start_date(end, days, include_start=False)
        
        # Verify the calculator method was called with correct arguments
        mock_calc_method.assert_called_once_with(end, days, False)
        assert result == datetime.date(2023, 1, 1)
    
    @patch('functions._calculator.calculate_start_date')
    def test_calculate_start_date_propagates_exceptions(self, mock_calc_method):
        """Test that exceptions from calculator are properly propagated."""
        mock_calc_method.side_effect = ValidationError.from_exception_data(
            "DateModel",
            [{"type": "value_error", "loc": ("days",), "msg": "Input should be greater than or equal to 0"}]
        )
        
        with pytest.raises(ValidationError):
            calculate_start_date(datetime.date(2023, 1, 10), -1)


class TestCalculateEndDate:
    """Test suite for calculate_end_date function."""
    
    @pytest.mark.parametrize("start_date,days,include_start,expected", [
        # Basic cases
        (datetime.date(2023, 1, 1), 10, True, datetime.date(2023, 1, 10)),
        (datetime.date(2023, 1, 1), 10, False, datetime.date(2023, 1, 11)),
        
        # Single day
        (datetime.date(2023, 1, 1), 1, True, datetime.date(2023, 1, 1)),
        (datetime.date(2023, 1, 1), 1, False, datetime.date(2023, 1, 2)),
        
        # Cross year
        (datetime.date(2022, 12, 27), 10, True, datetime.date(2023, 1, 5)),
        (datetime.date(2022, 12, 27), 10, False, datetime.date(2023, 1, 6)),
    ])
    def test_calculate_end_date_valid(self, start_date, days, include_start, expected):
        """Test calculate_end_date with valid inputs."""
        result = calculate_end_date(start_date, days, include_start)
        assert result == expected
    
    def test_calculate_end_date_default_include_start(self):
        """Test that default include_start parameter works correctly."""
        start = datetime.date(2023, 1, 1)
        days = 5
        
        # Should use DEFAULT_INCLUDE_START (True)
        result = calculate_end_date(start, days)
        assert result == datetime.date(2023, 1, 5)
        
        # Verify it's the same as explicitly passing True
        result_explicit = calculate_end_date(start, days, include_start=True)
        assert result == result_explicit
    
    def test_calculate_end_date_docstring_examples(self):
        """Test the examples from the docstring."""
        start = datetime.date(1989, 1, 28)
        
        # Example 1: default include_start
        result1 = calculate_end_date(start, 10000)
        assert result1 == datetime.date(2016, 6, 14)
        
        # Example 2: include_start=False
        result2 = calculate_end_date(start, 10000, include_start=False)
        assert result2 == datetime.date(2016, 6, 15)
    
    @patch('functions._calculator.calculate_end_date')
    def test_calculate_end_date_delegates_to_calculator(self, mock_calc_method):
        """Test that function delegates to the calculator instance."""
        mock_calc_method.return_value = datetime.date(2023, 1, 10)
        
        start = datetime.date(2023, 1, 1)
        days = 5
        
        result = calculate_end_date(start, days, include_start=False)
        
        # Verify the calculator method was called with correct arguments
        mock_calc_method.assert_called_once_with(start, days, False)
        assert result == datetime.date(2023, 1, 10)
    
    @patch('functions._calculator.calculate_end_date')
    def test_calculate_end_date_propagates_exceptions(self, mock_calc_method):
        """Test that exceptions from calculator are properly propagated."""
        mock_calc_method.side_effect = ValidationError.from_exception_data(
            "DateModel",
            [{"type": "value_error", "loc": ("days",), "msg": "Input should be greater than or equal to 0"}]
        )
        
        with pytest.raises(ValidationError):
            calculate_end_date(datetime.date(2023, 1, 1), -1)


class TestIntegrationAndConsistency:
    """Test integration and consistency across functions."""
    
    def test_round_trip_consistency(self):
        """Test that functions are consistent in round-trip calculations."""
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
    
    def test_all_functions_use_same_calculator_instance(self):
        """Test that all functions use the same calculator instance."""
        # This test verifies that the module-level calculator is shared
        with patch('functions._calculator') as mock_calculator:
            mock_calculator.calculate_days_from_dates.return_value = 1
            mock_calculator.calculate_start_date.return_value = datetime.date(2023, 1, 1)
            mock_calculator.calculate_end_date.return_value = datetime.date(2023, 1, 1)
            
            # Call all functions
            calculate_days_from_dates(datetime.date(2023, 1, 1), datetime.date(2023, 1, 2))
            calculate_start_date(datetime.date(2023, 1, 2), 1)
            calculate_end_date(datetime.date(2023, 1, 1), 1)
            
            # Verify all used the same mock instance
            assert mock_calculator.calculate_days_from_dates.called
            assert mock_calculator.calculate_start_date.called
            assert mock_calculator.calculate_end_date.called
    
    def test_default_parameter_consistency(self):
        """Test that all functions use the same default for include_start."""
        start = datetime.date(2023, 1, 1)
        end = datetime.date(2023, 1, 10)
        days = 10
        
        # All functions should use DEFAULT_INCLUDE_START when parameter is omitted
        result1 = calculate_days_from_dates(start, end)
        result2 = calculate_days_from_dates(start, end, include_start=DEFAULT_INCLUDE_START)
        assert result1 == result2
        
        result3 = calculate_start_date(end, days)
        result4 = calculate_start_date(end, days, include_start=DEFAULT_INCLUDE_START)
        assert result3 == result4
        
        result5 = calculate_end_date(start, days)
        result6 = calculate_end_date(start, days, include_start=DEFAULT_INCLUDE_START)
        assert result5 == result6
    
    def test_function_signatures_consistency(self):
        """Test that function signatures follow consistent patterns."""
        # Test that all functions have include_start parameter with same default
        import inspect
        
        # Get function signatures
        sig1 = inspect.signature(calculate_days_from_dates)
        sig2 = inspect.signature(calculate_start_date)
        sig3 = inspect.signature(calculate_end_date)
        
        # All should have include_start parameter with DEFAULT_INCLUDE_START default
        assert sig1.parameters['include_start'].default == DEFAULT_INCLUDE_START
        assert sig2.parameters['include_start'].default == DEFAULT_INCLUDE_START
        assert sig3.parameters['include_start'].default == DEFAULT_INCLUDE_START
    
    def test_module_level_calculator_is_singleton(self):
        """Test that the module-level calculator behaves as a singleton."""
        # Multiple imports should reference the same calculator instance
        from functions import _calculator as calc1
        import functions
        calc2 = functions._calculator
        
        assert calc1 is calc2
        assert id(calc1) == id(calc2)


class TestErrorHandling:
    """Test error handling and edge cases."""
    
    def test_functions_handle_calculator_exceptions(self):
        """Test that functions properly handle exceptions from calculator."""
        # Test with actual invalid data that would cause DateModel validation to fail
        with pytest.raises((ValidationError, ValueError)):
            # This should fail because start_date > end_date
            calculate_days_from_dates(datetime.date(2023, 1, 10), datetime.date(2023, 1, 1))
        
        with pytest.raises((ValidationError, ValueError)):
            # This should fail because of negative days (via DateModel validation)
            calculate_start_date(datetime.date(2023, 1, 1), -1)
        
        with pytest.raises((ValidationError, ValueError)):
            # This should fail because of negative days (via DateModel validation)
            calculate_end_date(datetime.date(2023, 1, 1), -1)
    
    def test_functions_preserve_error_messages(self):
        """Test that functions preserve error messages from underlying calculator."""
        with patch('functions._calculator.calculate_days_from_dates') as mock_method:
            expected_error = ValueError("Custom error message")
            mock_method.side_effect = expected_error
            
            with pytest.raises(ValueError) as exc_info:
                calculate_days_from_dates(datetime.date(2023, 1, 1), datetime.date(2023, 1, 2))
            
            assert str(exc_info.value) == "Custom error message"