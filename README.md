# ttDays: Simple Date Calculation Library

A comprehensive Python library for calculating days between dates, determining specific dates based on elapsed days, and handling complex date arithmetic with precision. Perfect for applications involving birthdays, project timelines, anniversaries, and business date calculations.

## Features

- 🗓️ Calculate days between any two dates
- 📅 Find specific dates based on start date + elapsed days
- ⏮️ Calculate start dates from end dates and day counts
- 🔧 Flexible include/exclude start date options
- 📝 Support for both datetime objects and string formats
- ✅ Comprehensive input validation with Pydantic v2
- 🧪 Thoroughly tested with extensive test suite

## Installation

```bash
pip install ttdays
```

## Quick Start

```python
from datetime import date
from ttdays import calculate_days_from_dates, calculate_end_date, calculate_start_date

# Calculate days between dates
start = date(1989, 1, 28)
end = date(2025, 7, 7)
days = calculate_days_from_dates(start, end)  # Returns 13345

# Calculate end date from start date and days
milestone = calculate_end_date(start, 10000)  # Returns date(2016, 6, 14)

# Calculate start date from end date and days
deadline = date(2025, 7, 7)
prep_start = calculate_start_date(deadline, 10000)  # Returns date(1998, 3, 11)
```

## Reference

### Core Functions

#### `calculate_days_from_dates(start_date, end_date, include_start=True) -> int`
Calculate the number of days elapsed between start and end dates.

**Parameters:**
- `start_date`: Starting date (datetime.date object or YYYY-MM-DD string)
- `end_date`: Ending date (datetime.date object or YYYY-MM-DD string)
- `include_start`: Whether to include start date in count (default: True)

**Returns:** Number of days as integer

#### `calculate_end_date(start_date, days, include_start=True) -> date`
Calculate end date from start date and number of days.

**Parameters:**
- `start_date`: Starting date (datetime.date object or YYYY-MM-DD string)
- `days`: Number of days to add (integer)
- `include_start`: Whether start date is included in count (default: True)

**Returns:** Calculated end date as datetime.date

#### `calculate_start_date(end_date, days, include_start=True) -> date`
Calculate start date from end date and number of days.

**Parameters:**
- `end_date`: Ending date (datetime.date object or YYYY-MM-DD string)
- `days`: Number of days to subtract (integer)
- `include_start`: Whether start date is included in count (default: True)

**Returns:** Calculated start date as datetime.date

### DateCalculator Class

For advanced usage, you can use the `DateCalculator` class directly:

```python
from ttdays import DateCalculator

calc = DateCalculator()
days = calc.calculate_days_from_dates("1989-01-28", "2025-07-07")  # 13345
start_date = calc.calculate_start_date("2025-07-07", 10000)  # date(1998, 3, 11)
end_date = calc.calculate_end_date("1989-01-28", 10000)  # date(2016, 6, 14)
```

## Real-World Examples

### 🎂 Days Since Birth / Life Milestones

```python
from datetime import date
from ttdays import calculate_days_from_dates, calculate_end_date

# Calculate days lived
birth_date = date(1989, 1, 28)
today = date.today()
days_lived = calculate_days_from_dates(birth_date, today)
print(f"Days lived: {days_lived:,}")

# Find your 10,000th day milestone
milestone_date = calculate_end_date(birth_date, 10000)
print(f"10,000th day: {milestone_date}")  # 2016-06-14
```

### 🏢 Business & Project Planning

```python
from ttdays import calculate_end_date, calculate_start_date

# 90-day project timeline
project_start = date(2024, 1, 1)
project_end = calculate_end_date(project_start, 90)
print(f"Project completion: {project_end}")

# Work backwards from deadline
deadline = date(2025, 7, 7)
prep_start = calculate_start_date(deadline, 180)  # 6 months prep
print(f"Start preparation by: {prep_start}")
```

### 📊 Historical Analysis

```python
# Company founding to major milestone
founding_date = date(1989, 1, 28)
milestone_10k = calculate_end_date(founding_date, 10000)
days_to_today = calculate_days_from_dates(founding_date, date(2025, 7, 7))

print(f"Founded: {founding_date}")
print(f"10,000th day: {milestone_10k}")
print(f"Days in operation: {days_to_today:,}")
```

### 🔧 Include/Exclude Start Date Options

```python
start = date(1989, 1, 28)
end = date(2025, 7, 7)

# Include start date (default behavior)
days_with_start = calculate_days_from_dates(start, end, include_start=True)  # 13345

# Exclude start date
days_without_start = calculate_days_from_dates(start, end, include_start=False)  # 13344

# This affects all calculations
end_with_start = calculate_end_date(start, 10000, include_start=True)  # 2016-06-14
end_without_start = calculate_end_date(start, 10000, include_start=False)  # 2016-06-15
```

### 📝 String Format Support

```python
# Mix datetime objects and strings
days = calculate_days_from_dates("1989-01-28", date(2025, 7, 7))  # 13345
milestone = calculate_end_date("1989-01-28", 10000)  # date(2016, 6, 14)
```

## Error Handling

ttDays provides comprehensive error handling:

```python
from ttdays import calculate_days_from_dates

try:
    # Invalid date format
    days = calculate_days_from_dates("1989/01/28", "2025-07-07")
except ValueError as e:
    print(f"Date format error: {e}")

try:
    # Start date after end date
    days = calculate_days_from_dates("2025-07-07", "1989-01-28")
except ValueError as e:
    print(f"Date logic error: {e}")
```

## Performance & Reliability

- ⚡ Optimized for performance with large date ranges
- 🛡️ Robust input validation prevents common errors
- 📊 Handles edge cases like leap years automatically
- 🧪 100% test coverage with comprehensive test suite

## Use Cases

- **Personal**: Birthday countdowns, life milestones, anniversary tracking
- **Business**: Project timelines, deadline planning, employee tenure
- **Finance**: Investment periods, loan terms, fiscal year calculations
- **Healthcare**: Treatment durations, appointment scheduling
- **Education**: Academic calendars, course durations, semester planning

## Changelog

### v0.1.0 (2025-07-07)
- Initial release with core date calculation functions
- Pydantic v2 input validation and error handling
- Support for both datetime objects and string formats
- Comprehensive test suite with 100% coverage
- Include/exclude start date flexibility
- DateCalculator class for advanced usage

## License

[MIT License](LICENSE)

## Links

- **Documentation**: [https://ttdays.readthedocs.io/](https://ttdays.readthedocs.io/)
- **Issues**: [https://github.com/well-living/ttdays/issues](https://github.com/well-living/ttdays/issues)
- **PyPI**: [https://pypi.org/project/ttdays/](https://pypi.org/project/ttdays/)

## Author

[@well-living](https://github.com/well-living) – GitHub

## Acknowledgments

- Built with [Pydantic](https://docs.pydantic.dev/) for robust data validation
- Inspired by real-world date calculation needs across various industries
- Designed for both simple scripts and enterprise applications