# Contributing to Google Trends CLI

Thank you for your interest in contributing to the Google Trends CLI tool! This document provides guidelines and instructions for contributing to the project.

## Table of Contents

- [Contributing to Google Trends CLI](#contributing-to-google-trends-cli)
  - [Table of Contents](#table-of-contents)
  - [Code of Conduct](#code-of-conduct)
  - [Getting Started](#getting-started)
  - [Development Environment](#development-environment)
    - [Prerequisites](#prerequisites)
    - [Setup](#setup)
    - [Running Tests](#running-tests)
  - [Pull Request Process](#pull-request-process)
  - [Coding Standards](#coding-standards)
    - [Code Linting and Formatting](#code-linting-and-formatting)
  - [Testing](#testing)
  - [Documentation](#documentation)
  - [Issue Reporting](#issue-reporting)
  - [Feature Requests](#feature-requests)
  - [Questions?](#questions)

## Code of Conduct

This project adheres to a Code of Conduct that establishes expectations for participation in our community. By participating, you are expected to uphold this code. Please read the [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) for details.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** to your local machine
3. **Create a branch** for your work
4. **Set up the development environment** (see next section)

## Development Environment

### Prerequisites

- Python 3.8 or higher
- Git

### Setup

```bash
# Clone your fork of the repo
git clone https://github.com/YOUR-USERNAME/google-trends-cli.git
cd google-trends-cli

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies and dev dependencies
pip install -e ".[dev]"
```

### Running Tests

```bash
# Run all tests
pytest

# Run tests with coverage report
pytest --cov=gtrends tests/
```

## Pull Request Process

1. **Create a feature branch** from the `main` branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Implement your changes**:
   - Write code that follows the project's [coding standards](#coding-standards)
   - Include appropriate tests
   - Update documentation as needed

3. **Commit your changes** using clear commit messages:
   ```bash
   git commit -m "Add feature: brief description of your change"
   ```

4. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

5. **Submit a pull request** to the `main` branch of the original repository
   - Provide a clear title and description
   - Reference any related issues

6. **Address review feedback** if requested by maintainers

## Coding Standards

- Follow [PEP 8](https://pep8.org/) style guidelines
- Use [type hints](https://docs.python.org/3/library/typing.html) for function signatures
- Write docstrings in the Google style format
- Keep functions focused and modular
- Use descriptive variable names

### Code Linting and Formatting

We use:
- `black` for code formatting
- `isort` for import sorting
- `flake8` for linting

Run these tools before submitting:

```bash
# Format code
black gtrends tests

# Sort imports
isort gtrends tests

# Run linting
flake8 gtrends tests
```

## Testing

- Write unit tests for new features and bug fixes
- Ensure all tests pass before submitting a PR
- Aim for high test coverage
- Place tests in the `tests/` directory, mirroring the structure of the code

## Documentation

- Update the README.md if your changes affect usage
- Update or add docstrings for all public functions, classes, and methods
- Consider adding examples for new features

## Issue Reporting

When reporting issues, please include:

1. A clear, descriptive title
2. Steps to reproduce the issue
3. Expected behavior
4. Actual behavior
5. Environment information (OS, Python version, package version)
6. Any relevant logs or screenshots

## Feature Requests

Feature requests are welcome! Please provide:

1. A clear, descriptive title
2. Detailed description of the proposed feature
3. Rationale: why this feature would be useful
4. If possible, outline how the feature might be implemented

## Questions?

If you have any questions about contributing, please open an issue with your question.

Thank you for contributing to Google Trends CLI!