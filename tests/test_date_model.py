# test_date_model.py
import datetime
import pytest
from pydantic import ValidationError

from date_model import DateModel


class TestDateModel:
    """Test suite for DateModel class."""
    
    def test_default_values(self):
        """Test that default values are set correctly."""
        # Test with minimum required fields (start_date and end_date)
        model = DateModel(
            start_date=datetime.date(2023, 1, 1),
            end_date=datetime.date(2023, 1, 10)
        )
        assert model.start_date == datetime.date(2023, 1, 1)
        assert model.end_date == datetime.date(2023, 1, 10)
        assert model.days is None
        assert model.include_start is True
    
    @pytest.mark.parametrize("start_date,end_date,days,include_start", [
        # Test with start_date and end_date
        (datetime.date(2023, 1, 1), datetime.date(2023, 1, 10), None, True),
        (datetime.date(2023, 1, 1), datetime.date(2023, 1, 10), None, False),
        
        # Test with start_date and days
        (datetime.date(2023, 1, 1), None, 10, True),
        (datetime.date(2023, 1, 1), None, 0, False),
        
        # Test with end_date and days
        (None, datetime.date(2023, 1, 10), 5, True),
        (None, datetime.date(2023, 1, 10), 1000000, False),
        
        # Test with all three fields
        (datetime.date(2023, 1, 1), datetime.date(2023, 1, 10), 9, True),
    ])
    def test_valid_field_combinations(self, start_date, end_date, days, include_start):
        """Test valid combinations of input fields."""
        model = DateModel(
            start_date=start_date,
            end_date=end_date,
            days=days,
            include_start=include_start
        )
        assert model.start_date == start_date
        assert model.end_date == end_date
        assert model.days == days
        assert model.include_start == include_start
    
    def test_same_start_and_end_date(self):
        """Test that same start and end dates are valid."""
        same_date = datetime.date(2023, 1, 1)
        model = DateModel(start_date=same_date, end_date=same_date)
        assert model.start_date == same_date
        assert model.end_date == same_date
    
    def test_date_consistency_validation_failure(self):
        """Test that start_date after end_date raises ValueError."""
        with pytest.raises(ValidationError) as exc_info:
            DateModel(
                start_date=datetime.date(2023, 1, 10),
                end_date=datetime.date(2023, 1, 1)
            )
        
        # Check that the error message contains the expected validation error
        error_details = str(exc_info.value)
        assert "Start date cannot be after end date" in error_details
    
    @pytest.mark.parametrize("start_date,end_date,days", [
        # Only one field provided
        (datetime.date(2023, 1, 1), None, None),
        (None, datetime.date(2023, 1, 10), None),
        (None, None, 5),
        
        # No fields provided
        (None, None, None),
    ])
    def test_required_fields_validation_failure(self, start_date, end_date, days):
        """Test that providing less than two fields raises ValueError."""
        with pytest.raises(ValidationError) as exc_info:
            DateModel(
                start_date=start_date,
                end_date=end_date,
                days=days
            )
        
        error_details = str(exc_info.value)
        assert "At least two of start_date, end_date, or days must be provided" in error_details
    
    @pytest.mark.parametrize("invalid_days", [
        -1,      # Below minimum
        -100,    # Far below minimum
        1000001, # Above maximum
        2000000, # Far above maximum
    ])
    def test_days_field_validation_failure(self, invalid_days):
        """Test that invalid days values raise ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            DateModel(
                start_date=datetime.date(2023, 1, 1),
                days=invalid_days
            )
        
        error_details = str(exc_info.value)
        # Check for constraint violation in the error message
        assert "Input should be greater than or equal to 0" in error_details or \
               "Input should be less than or equal to 1000000" in error_details
    
    def test_days_boundary_values(self):
        """Test boundary values for days field."""
        # Test minimum boundary (0)
        model_min = DateModel(
            start_date=datetime.date(2023, 1, 1),
            days=0
        )
        assert model_min.days == 0
        
        # Test maximum boundary (1000000)
        model_max = DateModel(
            start_date=datetime.date(2023, 1, 1),
            days=1000000
        )
        assert model_max.days == 1000000
    
    def test_model_immutability(self):
        """Test that the model is immutable (frozen=True)."""
        model = DateModel(
            start_date=datetime.date(2023, 1, 1),
            end_date=datetime.date(2023, 1, 10)
        )
        
        # Attempt to modify a field should raise an error
        with pytest.raises(ValidationError):
            model.start_date = datetime.date(2023, 1, 2)
    
    def test_extra_fields_forbidden(self):
        """Test that extra fields are not allowed (extra='forbid')."""
        with pytest.raises(ValidationError) as exc_info:
            DateModel(
                start_date=datetime.date(2023, 1, 1),
                end_date=datetime.date(2023, 1, 10),
                extra_field="not_allowed"
            )
        
        error_details = str(exc_info.value)
        assert "Extra inputs are not permitted" in error_details
    
    def test_field_descriptions(self):
        """Test that field descriptions are correctly set."""
        # Access the model's field info to verify descriptions
        fields = DateModel.model_fields
        
        assert fields['start_date'].description == "The start date of the range"
        assert fields['end_date'].description == "The end date of the range"
        assert fields['days'].description == "Number of days for calculation (0 to 1000000)"
        assert fields['include_start'].description == "Whether to include the start date in the calculation"
    
    def test_model_config(self):
        """Test that model configuration is correctly applied."""
        # Test that the model is frozen
        assert DateModel.model_config['frozen'] is True
        
        # Test that extra fields are forbidden
        assert DateModel.model_config['extra'] == 'forbid'
    
    @pytest.mark.parametrize("date_str,expected_date", [
        ("2023-01-01", datetime.date(2023, 1, 1)),
        ("2023-12-31", datetime.date(2023, 12, 31)),
        ("2024-02-29", datetime.date(2024, 2, 29)),  # Leap year
    ])
    def test_date_string_parsing(self, date_str, expected_date):
        """Test that date strings are correctly parsed."""
        model = DateModel(
            start_date=date_str,
            end_date=expected_date
        )
        assert model.start_date == expected_date
        assert model.end_date == expected_date
    
    def test_invalid_date_string(self):
        """Test that invalid date strings raise ValidationError."""
        with pytest.raises(ValidationError):
            DateModel(
                start_date="invalid-date",
                end_date=datetime.date(2023, 1, 10)
            )
    
    def test_model_serialization(self):
        """Test that the model can be serialized to dict."""
        model = DateModel(
            start_date=datetime.date(2023, 1, 1),
            end_date=datetime.date(2023, 1, 10),
            days=9,
            include_start=False
        )
        
        result = model.model_dump()
        expected = {
            'start_date': datetime.date(2023, 1, 1),
            'end_date': datetime.date(2023, 1, 10),
            'days': 9,
            'include_start': False
        }
        
        assert result == expected
    
    def test_model_json_serialization(self):
        """Test that the model can be serialized to JSON."""
        model = DateModel(
            start_date=datetime.date(2023, 1, 1),
            end_date=datetime.date(2023, 1, 10)
        )
        
        json_str = model.model_dump_json()
        assert isinstance(json_str, str)
        assert "2023-01-01" in json_str
        assert "2023-01-10" in json_str