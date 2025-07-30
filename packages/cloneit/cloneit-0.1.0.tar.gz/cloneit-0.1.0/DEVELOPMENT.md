# Development Guide

This guide covers how to set up the development environment and contribute to cloneit.

## Development Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/neeraj/cloneit.git
   cd cloneit
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On Unix/macOS
   source venv/bin/activate
   ```

3. **Install development dependencies**:
   ```bash
   pip install -e ".[dev]"
   ```

## Running Tests

Run the full test suite:
```bash
pytest
```

Run tests with coverage:
```bash
pytest --cov=cloneit --cov-report=html
```

Run specific test file:
```bash
pytest tests/test_cloneit.py
pytest tests/test_integration.py
```

## Code Quality

### Formatting with Black
```bash
black src/ tests/ examples/
```

### Linting with Flake8
```bash
flake8 src/ tests/ examples/
```

### Type Checking with MyPy
```bash
mypy src/cloneit
```

## Building and Publishing

### Build the package
```bash
python -m build
```

### Upload to PyPI (maintainers only)
```bash
# Test PyPI first
python -m twine upload --repository testpypi dist/*

# Production PyPI
python -m twine upload dist/*
```

## Project Structure

```
cloneit/
├── src/cloneit/           # Main package code
│   ├── __init__.py        # Package initialization
│   ├── core.py            # Core functionality
│   └── exceptions.py      # Custom exceptions
├── tests/                 # Test files
│   ├── test_cloneit.py    # Main test suite
│   ├── test_integration.py # Framework integration tests
│   └── requirements.txt   # Test dependencies
├── examples/              # Usage examples
│   ├── basic_usage.py     # Basic usage examples
│   ├── framework_examples.py # Framework integration examples
│   └── README.md          # Examples documentation
├── docs/                  # Documentation (if added)
├── pyproject.toml         # Project configuration
├── README.md              # Main documentation
├── LICENSE                # MIT license
└── DEVELOPMENT.md         # This file
```

## Contributing

1. **Fork the repository** on GitHub
2. **Create a feature branch**: `git checkout -b feature/your-feature-name`
3. **Make your changes** following the coding standards
4. **Add tests** for new functionality
5. **Run the test suite** to ensure everything passes
6. **Commit your changes**: `git commit -am 'Add some feature'`
7. **Push to the branch**: `git push origin feature/your-feature-name`
8. **Create a Pull Request** on GitHub

## Coding Standards

- Follow PEP 8 style guidelines
- Use type hints where appropriate
- Write docstrings for public functions and classes
- Keep functions focused and small
- Use descriptive variable and function names
- Add tests for new functionality
- Update documentation when needed

## Release Process

1. Update version in `pyproject.toml`
2. Update `CHANGELOG.md` (if exists)
3. Create a git tag: `git tag v1.0.0`
4. Push tag: `git push origin v1.0.0`
5. Build and upload to PyPI
6. Create GitHub release

## Getting Help

- Open an issue on GitHub for bugs or feature requests
- Start a discussion for questions or ideas
- Check existing issues and discussions first

## License

This project is licensed under the MIT License - see the LICENSE file for details.
