# cloneit Development Environment

## Quick Setup Commands

### Windows PowerShell Setup
```powershell
# Create and activate virtual environment
python -m venv venv
venv\Scripts\Activate.ps1

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest

# Run examples
python examples\basic_usage.py
python examples\framework_examples.py
```

### Package Installation
```powershell
# Install from source (development)
pip install -e .

# Install from PyPI (when published)
pip install cloneit
```

### Testing Commands
```powershell
# Run all tests
pytest

# Run with coverage
pytest --cov=cloneit --cov-report=html

# Run specific test files
pytest tests\test_cloneit.py
pytest tests\test_integration.py

# Run with verbose output
pytest -v
```

### Code Quality Commands
```powershell
# Format code
black src\ tests\ examples\

# Lint code
flake8 src\ tests\ examples\

# Type checking
mypy src\cloneit
```

### Build Commands
```powershell
# Build package
python -m build

# Check package
twine check dist\*
```
