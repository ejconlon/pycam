# PyCAM Development Commands

# Default recipe - show available commands
default:
    @just --list

# Type check the entire codebase with mypy
typecheck:
    .venv/bin/python -m mypy pycam/ --show-error-codes

# Type check specific file or directory  
typecheck-file path:
    .venv/bin/python -m mypy {{path}} --show-error-codes

# Run all unit tests using unittest
test:
    @echo "Running unit tests in pycam/Test/"
    .venv/bin/python -m unittest discover -s pycam/Test -p "test_*.py" -v

# Run specific test file
test-file testfile:
    .venv/bin/python -m unittest pycam.Test.{{testfile}} -v

# Run tests that use pytest (for files that require pytest)
test-pytest:
    @echo "Installing pytest if needed..."
    .venv/bin/python -m pip install pytest > /dev/null 2>&1 || true
    @echo "Running pytest tests..."
    .venv/bin/python -m pytest pycam/Test/ -v

# Run both type checking and tests
check: typecheck test

# Install development dependencies
install-deps:
    .venv/bin/python -m pip install mypy pytest

# Clean Python cache files
clean:
    find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    find . -type f -name "*.pyc" -delete 2>/dev/null || true
    find . -type f -name "*.pyo" -delete 2>/dev/null || true

# Show mypy coverage report
typecheck-coverage:
    .venv/bin/python -m mypy pycam/ --html-report mypy-report --show-error-codes
    @echo "HTML report generated in mypy-report/"

# Run tests with coverage (if coverage is installed)
test-coverage:
    .venv/bin/python -m pip install coverage > /dev/null 2>&1 || true
    .venv/bin/python -m coverage run -m unittest discover -s pycam/Test -p "test_*.py"
    .venv/bin/python -m coverage report
    .venv/bin/python -m coverage html
    @echo "HTML coverage report generated in htmlcov/"