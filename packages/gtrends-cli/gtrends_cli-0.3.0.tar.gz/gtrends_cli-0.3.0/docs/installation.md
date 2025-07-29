# Installation Guide

This guide provides instructions for installing the Google Trends CLI and API tools.

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Installation Options

### 1. Install from PyPI (Recommended)

The simplest way to install the package is from PyPI:

```bash
# Install CLI only
pip install gtrends-cli

# Install with API support
pip install "gtrends-cli[api]"
```

### 2. Install from GitHub

You can also install the latest development version directly from GitHub:

```bash
# Install CLI only
pip install git+https://github.com/Nao-30/google-trends-cli.git

# Install with API support
pip install "git+https://github.com/Nao-30/google-trends-cli.git#egg=gtrends-cli[api]"
```

### 3. Install from Source

If you have the source code:

```bash
# Navigate to the project directory
cd google-trends-cli

# Install CLI only
pip install .

# Install with API support
pip install ".[api]"
```

## Verify Installation

After installation, you should be able to run:

```bash
# CLI Command
gtrends --help
```

If you installed with API support:

```bash
# API Command
gtrends-api --help
```

## Using Docker

If you prefer using Docker, you can run the API server with:

```bash
# Pull the image
docker pull nao30/gtrends-api:latest

# Run the API server
docker run -p 8000:8000 nao30/gtrends-api:latest
```

Then access the API at http://localhost:8000

## Troubleshooting

If you encounter issues:

1. Ensure you have the correct Python version (3.8+)
2. Try upgrading pip: `pip install --upgrade pip`
3. If you're behind a proxy, configure pip to use it
4. Check if any dependencies are conflicting with existing packages

## Uninstallation

To uninstall:

```bash
pip uninstall gtrends-cli
``` 