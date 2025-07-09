# Testing

## Running the Tests

### Prerequisites
```bash
pip install pytest pydantic
```

### Test Execution Commands

#### Run all tests
```bash
pytest test_date_model.py test_date_calculator.py test_functions.py
```

#### Run tests with minimal output and disable warnings
```bash
pytest -q --disable-warnings test_date_model.py test_date_calculator.py test_functions.py
```

#### Run tests with verbose output
```bash
pytest -v test_date_model.py test_date_calculator.py test_functions.py
```

#### Run tests with coverage report
```bash
pip install pytest-cov
pytest --cov=date_model --cov=date_calculator --cov=functions test_date_model.py test_date_calculator.py test_functions.py
```

#### Run specific test files
```bash
pytest tests/test_date_model.py
pytest tests/test_date_calculator.py
pytest tests/test_functions.py
```

#### Run specific test methods
```bash
pytest tests/test_date_model.py::TestDateModel::test_valid_field_combinations -v
pytest tests/test_date_calculator.py::TestDateCalculator::test_calculate_days_from_dates_valid -v
pytest tests/test_functions.py::TestCalculateDaysFromDates::test_calculate_days_from_dates_valid -v
```

#### Run tests with parametrized test details
```bash
pytest -v test_date_calculator.py::TestDateCalculator::test_calculate_days_from_dates_valid
pytest -v test_functions.py::TestCalculateDaysFromDates::test_calculate_days_from_dates_valid
```

### Test Structure

The test suite covers:

#### DateModel Tests (`test_date_model.py`)
1. **Normal Cases (正常系)**
   - Valid field combinations
   - Default values
   - Boundary values for days field
   - Date string parsing
   - Model serialization

2. **Exception Cases (異常系)**
   - Invalid date ranges (start_date > end_date)
   - Missing required fields
   - Invalid days values (out of range)
   - Extra fields (forbidden)
   - Invalid date strings
   - Model immutability violations

#### DateCalculator Tests (`test_date_calculator.py`)
1. **Normal Cases (正常系)**
   - Valid date calculations for all methods
   - String and datetime.date input handling
   - Different include_start flag behaviors
   - Cross-year and leap year calculations
   - Round-trip calculation consistency

2. **Exception Cases (異常系)**
   - Invalid date string formats
   - DateModel validation errors (via mocking)
   - Negative days handling
   - Integration with DateModel validation

#### Functions Tests (`test_functions.py`)
1. **Normal Cases (正常系)**
   - Wrapper function delegation to calculator
   - Default parameter behavior
   - Docstring examples verification
   - Round-trip calculation consistency
   - Module-level constants

2. **Exception Cases (異常系)**
   - Exception propagation from calculator
   - Error message preservation
   - Invalid input handling via calculator

3. **Edge Cases**
   - Module-level calculator singleton behavior
   - Function signature consistency
   - Default parameter consistency across functions

### Test Coverage

The test suite achieves comprehensive coverage of:

#### DateModel
- All model validators
- Field constraints
- Configuration settings
- Serialization methods
- Error handling

#### DateCalculator
- All public methods (`calculate_days_from_dates`, `calculate_start_date`, `calculate_end_date`)
- Private helper methods (`_parse_date`, `_calculate_days_offset`)
- Integration with DateModel
- String and datetime.date input handling
- Round-trip calculation verification
- Error propagation from DateModel

#### Functions
- All convenience wrapper functions
- Module-level constants and calculator instance
- Function delegation and error propagation
- Consistency across function signatures and behavior
- Singleton pattern for module-level calculator