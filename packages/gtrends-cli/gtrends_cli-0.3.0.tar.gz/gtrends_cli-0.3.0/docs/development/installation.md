# Development Installation Guide

This guide will help you set up a development environment for working on the Google Trends CLI and API project.

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git

## Clone the Repository

```bash
git clone https://github.com/Nao-30/google-trends-cli.git
cd google-trends-cli
```

## Installation Options

### 1. Development Mode Installation

This is the recommended approach for development as it creates a link to the source code:

```bash
# Install the package in development mode with all development dependencies
pip install -e ".[dev]"
```

### 2. Install with API Dependencies

If you want to work on the API portion of the project:

```bash
# Install with API dependencies
pip install -e ".[api]"
```

### 3. Full Installation

For both development and API dependencies:

```bash
# Install with all dependencies
pip install -e ".[all]"
```

## Verify Installation

After installation, you should be able to run:

```bash
# CLI Command
gtrends --help

# API Command (if API dependencies installed)
gtrends-api --help
```

## Running Tests

To run the tests:

```bash
pytest
```

To run tests with coverage:

```bash
pytest --cov=src
```

## Code Style

This project uses several tools to maintain code quality:

- Black for code formatting
- isort for import sorting
- flake8 for linting
- mypy for type checking

To run all formatting tools:

```bash
# Format code
black src tests
isort src tests

# Check for issues
flake8 src tests
mypy src
```

## Pre-commit Hooks

For a better development experience, set up pre-commit hooks:

```bash
pip install pre-commit
pre-commit install
```

This will automatically run formatting checks before each commit.

## Building Documentation

To build the documentation:

```bash
cd docs
make html
```

## Packaging

To build the package:

```bash
python -m build
```

This will create both wheel and source distributions in the `dist` directory. 