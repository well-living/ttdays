# Contributing to ttdays

Thank you for considering contributing to this project.  
We welcome bug reports, feature suggestions, documentation improvements, and pull requests.

## Development Setup

### 1. Clone the repository

'''
git clone https://github.com/your-username/ttdays.git
cd ttdays
'''

### 2. Create and activate a virtual environment

Using `uv`:

'''
uv venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
'''

### 3. Install development dependencies

'''
uv pip install -e .[dev]
'''

### 4. Install and run pre-commit (optional but recommended)

'''
pre-commit install
pre-commit run --all-files
'''

### 5. Run tests

'''
pytest
'''

---

## Linting

This project uses [Ruff](https://docs.astral.sh/ruff/) for linting and formatting.

To run Ruff manually:

'''
ruff check .
'''

Ruff is configured via the `[tool.ruff]` section in `pyproject.toml`. Here is what each setting means:

```
[tool.ruff]
line-length = 88              # Maximum line length (PEP8 default is 79, Black uses 88)
target-version = "py311"      # Code is written for Python 3.11
select = ["E", "F", "I"]      # Enable specific rule sets:
                             # - "E": pycodestyle (style errors)
                             # - "F": pyflakes (undefined variables, imports, etc.)
                             # - "I": isort (import order and grouping)
ignore = ["D203", "D213"]     # Ignore specific docstring rules that conflict with each other
```

We recommend using `pre-commit` to run Ruff and format code automatically before committing.

---

## Testing

We use `pytest` and `pytest-cov` for testing and coverage.

To run all tests with coverage:

'''
pytest --cov=ttdays
'''

Tests are located in the `tests/` directory.

---

## Build System

We use **Hatchling** as the build backend, defined in `pyproject.toml`:

```
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

### Why Hatchling?

Hatchling was chosen over alternatives like `setuptools`, `flit`, and `poetry` for its:

- Minimal configuration
- PEP 621 compliance
- Speed and simplicity
- Lightweight nature, suitable for small to medium-sized libraries

### Building the package (optional):

'''
python -m build
'''

### Publishing to PyPI (optional):

'''
twine upload dist/*
'''

---

## Branch Naming Convention

| Type     | Prefix      | Example               |
|----------|-------------|-----------------------|
| Feature  | feature/    | feature/add-function  |
| Bugfix   | fix/        | fix/parse-error       |
| Docs     | docs/       | docs/update-readme    |
| Refactor | refactor/   | refactor/cleanup-code |

---

## Pull Request Guidelines

- Create branches from `main`
- Keep PRs focused (one purpose per PR)
- Use clear titles and descriptions
- Link related issues (e.g., `Closes #42`)
- Ensure pre-commit and tests pass locally before pushing
- Use the PR template and follow the style of existing code

---

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
