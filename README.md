# ttDays: 
A tool that calculates how many days have passed between a given start date (e.g., a person's birthday or a company's founding date) and an end date (e.g., today), or determines a specific date based on a start date and a number of elapsed days (e.g., what date it will be on the 10000th day since birth).

## Installation

```bash
pip install ttdays
```

## Quick Start

```python
from datetime import date
from ttdays import calculate_days_from_dates, calculate_end_date, calculate_start_date

# Calculate days between dates
start = date(2024, 1, 1)
end = date(2024, 1, 10)
days = calculate_days_from_dates(start, end)  # Returns 10

# Calculate end date from start date and days
project_end = calculate_end_date(start, 30)  # Returns date(2024, 1, 30)

# Calculate start date from end date and days
deadline = date(2024, 6, 15)
prep_start = calculate_start_date(deadline, 60)  # Returns date(2024, 4, 16)
```

## Reference

### Functions

#### `calculate_days_from_dates(start_date, end_date, include_start=True) -> int`
Calculate days between two dates.

#### `calculate_end_date(start_date, days, include_start=True) -> date`
Calculate end date from start date and number of days.

#### `calculate_start_date(end_date, days, include_start=True) -> date`
Calculate start date from end date and number of days.

### Parameters

- `include_start` (bool): Whether to include the start date in the count (default: True)

### Class Usage

```python
from ttdays import DateCalculator

calc = DateCalculator()
days = calc.calculate_days_from_dates(start, end)
```

## Examples

### Days Since Birth

```python
from datetime import date
from ttdays import calculate_days_from_dates

birth_date = date(1990, 5, 15)
today = date.today()
days_lived = calculate_days_from_dates(birth_date, today)
print(f"Days lived: {days_lived}")
```

### Project Duration

```python
from ttdays import calculate_end_date, calculate_start_date

# 30-day project
project_start = date(2024, 1, 1)
project_end = calculate_end_date(project_start, 30)

# Work backwards from deadline
deadline = date(2024, 6, 15)
work_start = calculate_start_date(deadline, 45)
```

### Include/Exclude Start Date

```python
start = date(2024, 1, 1)
end = date(2024, 1, 3)

# Include start date (default)
days_with_start = calculate_days_from_dates(start, end, include_start=True)  # 3

# Exclude start date
days_without_start = calculate_days_from_dates(start, end, include_start=False)  # 2
```


# Changelog

## v0.1.0 (2025-07-07)
- Initial release  
- Basic date calculation functions  
- Pydantic v2 input validation  
- Comprehensive test suite  

# License

[MIT License](LICENSE)


# Documentation

- **Documentation**: [https://ttdays.readthedocs.io/](https://ttdays.readthedocs.io/)

# Support


- **Issues**: [https://github.com/well-living/ttdays/issues](https://github.com/well-living/ttdays/issues)  
- **PyPI**: [https://pypi.org/project/ttdays/](https://pypi.org/project/ttdays/)  

---

# Author

[@well-living](https://github.com/well-living) – GitHub



# Acknowledgments

- Built with [Pydantic](https://docs.pydantic.dev/) for robust data validation  
- Inspired by common date calculation needs in business applications


