# Google Trends CLI Tool

<p align="center">
  <img src="https://raw.githubusercontent.com/Nao-30/google-trends-cli/main/assets/gtrends-logo.png" alt="Google Trends CLI Logo" width="180"/>
</p>

<p align="center">
  <a href="https://pypi.org/project/gtrends/"><img alt="PyPI version" src="https://img.shields.io/pypi/v/gtrends.svg"></a>
  <a href="https://github.com/Nao-30/google-trends-cli/blob/main/LICENSE"><img alt="License" src="https://img.shields.io/github/license/Nao-30/google-trends-cli"></a>
  <a href="https://github.com/Nao-30/google-trends-cli/actions"><img alt="Build status" src="https://github.com/Nao-30/google-trends-cli/workflows/Tests/badge.svg"></a>
  <a href="https://pypi.org/project/gtrends/"><img alt="Python versions" src="https://img.shields.io/pypi/pyversions/gtrends.svg"></a>
</p>

A powerful tool for fetching and analyzing Google Trends data, available as both a command-line tool and an HTTP API. Specially designed for content creators looking to identify what topics are worthy of writing about right now.

> **Note:** For a list of known issues and limitations, see [KNOWN_ISSUES.md](KNOWN_ISSUES.md).

---

## ✨ Features

- 📈 **Real-time Trends**: Access trending searches with a simple command
- 🔍 **Deep Analysis**: Explore related topics and queries for any search term
- 📊 **Comparative Insights**: Compare interest across different topics and timeframes
- ✍️ **Writer Suggestions**: Get data-driven content ideas specifically for writers
- 📱 **Geographic Analysis**: See how trends vary by region, country, or city
- 📉 **Independent Normalization**: Track hundreds of topics with individual trend lines
- 📰 **News Integration**: Find trending topics with associated news articles
- 📁 **Multiple Export Formats**: Save data as CSV, JSON, or Excel files with enhanced JSON structure
- 🖼️ **Visual Reporting**: Generate high-quality trend visualizations with matplotlib
- 🌐 **HTTP API**: Access all functionality via a RESTful API
- 🔄 **Environment Configuration**: Easily configure for development, testing, or production
- 🐳 **Docker Support**: Deploy as containerized services with health checks and security
- 🧪 **Comprehensive Testing**: Extensive unit and integration test coverage
- 🛡️ **Quality Assurance**: Built-in tooling for code quality and security checks

## 🧠 Architecture

The project follows a modern service-oriented architecture with clear separation of concerns:

```
google-trends-cli/
├── src/
│   ├── gtrends_core/        # Core business logic library
│   ├── gtrends_cli/         # CLI presentation layer
│   └── gtrends_api/         # HTTP API layer
├── tests/
│   ├── unit/                # Unit tests
│   └── integration/         # Integration tests
├── config/                  # Environment configurations
├── docker/                  # Docker configuration
└── scripts/                 # Utility scripts
```

This architecture enables:
- **Independent Development**: Core logic can be tested and developed separately
- **Multiple Interfaces**: CLI and API layers share the same core logic
- **Easy Extension**: Add new interfaces without modifying business logic
- **Robust Testing**: Comprehensive test coverage across all layers

## 🌐 API Access

All functionality is available through an HTTP API, making it easy to integrate Google Trends data into your applications:

```bash
# Start the API server
gtrends-api

# By default, the API runs on http://localhost:8000
```

### API Endpoints

| Endpoint | Description |
|----------|-------------|
| `/api/v1/trending` | Get trending searches |
| `/api/v1/related/topics` | Find related topics |
| `/api/v1/related/queries` | Find related queries |
| `/api/v1/comparison` | Compare interest across topics |
| `/api/v1/suggestions` | Get content creation suggestions |
| `/api/v1/opportunities` | Find writing opportunities |
| `/api/v1/growth` | Track growth for multiple topics |
| `/api/v1/geo` | Analyze geographic distribution |
| `/api/v1/health` | API health check |
| `/api/docs` | Interactive API documentation |

For detailed API documentation, visit the `/api/docs` endpoint when the server is running.

## 🚀 Installation

### Quick Install

```bash
# Basic installation (CLI only)
pip install gtrends-cli

# Installation with API support
pip install "gtrends-cli[api]"

# Installation with all dependencies (API + production + development)
pip install "gtrends-cli[all]"
```

### Using the Setup Script

For convenience, you can use the provided setup script:

```bash
# Clone the repository
git clone https://github.com/Nao-30/google-trends-cli.git
cd google-trends-cli

# Make the script executable
chmod +x scripts/setup.sh

# Run the setup script (development environment)
./scripts/setup.sh
```

### From Source

```bash
# Clone the repository
git clone https://github.com/Nao-30/google-trends-cli.git
cd google-trends-cli

# CLI only
pip install .

# With API support
pip install ".[api]"

# With development dependencies
pip install ".[dev]"

# With production dependencies
pip install ".[prod]"

# With all dependencies
pip install ".[all]"
```

### Docker

```bash
# Using docker-compose (recommended)
cd google-trends-cli/docker
docker-compose up -d

# Or pull and run the API image directly
docker pull nao30/gtrends-api:latest
docker run -p 8000:8000 nao30/gtrends-api:latest
```

For more detailed installation instructions, see the [Installation Guide](docs/installation.md).

## 🧪 Development and Testing

The project includes comprehensive tools for development and testing:

```bash
# Setup development environment
./scripts/setup.sh

# Run all tests with coverage
./scripts/test.sh

# Run only unit tests
./scripts/test.sh --unit-only

# Run only integration tests
./scripts/test.sh --integration-only

# Run only linting checks
./scripts/test.sh --lint-only

# Deploy to production (requires configuration)
./scripts/deploy.sh --target=docker --env=production
```

## 🔧 Configuration

The project supports multiple environment configurations:

```bash
# Set environment (development, testing, production, docker)
export GTRENDS_ENV=development

# Configuration files are in the config/ directory:
# - development.yml: Development settings
# - testing.yml: Test settings
# - production.yml: Production settings
# - docker.yml: Docker deployment settings
```

## 💻 Quick Start

```bash
# Show trending searches
gtrends trending

# Get content suggestions for creators
gtrends suggest-topics

# Find writing opportunities
gtrends writing-opportunities
```

## 📖 Usage Examples

### Basic Commands

```bash
# Show trending searches
gtrends trending

# Show trending searches with news articles
gtrends trending --with-articles

# Show topics and queries related to a term
gtrends related topics "book publishing"
gtrends related queries "book publishing"

# Compare interest in multiple topics
gtrends compare "fiction books" "non-fiction books" "poetry"

# Get content suggestions for writers
gtrends suggest-topics --category=books

# Find writing opportunities
gtrends writing-opportunities "science fiction" "fantasy"

# Analyze growth patterns for topics (up to 500+ topics)
gtrends topic-growth "science fiction" "fantasy" "romance" "mystery" --period=24h

# Show geographic interest distribution
gtrends geo-interest "literature" --resolution=COUNTRY

# Search for category IDs
gtrends categories --find=book

# Search for location codes
gtrends geo "middle east"

# Show supported timeframe formats
gtrends help-timeframe
```

### For Content Creators

Commands specially designed for content creators looking to identify trending topics:

```bash
# Get topic suggestions in the books category
gtrends suggest-topics --category=books --region=US

# Find specific writing opportunities based on rising trends
gtrends writing-opportunities "book publishing" "fiction" --count=10

# Compare interest in publishing trends over time with visualization
gtrends compare "self-publishing" "traditional publishing" --visualize

# Monitor rapid growth patterns for genres (independently normalized)
gtrends topic-growth "mystery" "thriller" "romance" "sci-fi" "fantasy" --period=7d 
```

### Export Options

```bash
# Export trending searches to CSV (default)
gtrends trending --export

# Export to a specific location and format
gtrends suggest-topics --export --export-path="~/my-projects" --format=json

# Generate visualization and export data
gtrends compare "poetry" "prose" "fiction" --export --visualize

# Export comparison data with enhanced JSON structure
gtrends compare "fiction" "non-fiction" --export --format=json
```

## 📋 Available Commands

| Command | Description |
|---------|-------------|
| `trending` | Show current trending searches |
| `related` | Find related topics and queries |
| `suggest-topics` | Get content creation suggestions |
| `compare` | Compare interest across topics |
| `writing-opportunities` | Find specific writing opportunities |
| `topic-growth` | Track growth for multiple topics |
| `geo-interest` | Analyze geographic distribution |
| `categories` | List available content categories |
| `geo` | Search for location codes |
| `help-timeframe` | Show timeframe format help |

## ⚙️ Common Options

| Option | Description |
|--------|-------------|
| `--region`, `-r` | Region code (e.g., US, GB, AE) |
| `--count`, `-n` | Number of results to display |
| `--timeframe`, `-t` | Time range (e.g., 'now 1-d', 'today 3-m') |
| `--export`, `-e` | Export results to file |
| `--export-path` | Directory to save exported data |
| `--format`, `-f` | Export format (csv, json, xlsx) |
| `--visualize`, `-v` | Generate visualization |

## 🕒 Timeframe Formats

```
Standard formats:    'now 1-H', 'today 3-m', 'today 12-m'
Custom intervals:    'now 123-H', 'today 45-d', 'today 18-m'
Date-based:          '2024-02-01 10-d', '2024-01-01 2024-12-31'
Hourly precision:    '2024-03-25T12 2024-03-25T15'
All available data:  'all'
```

## 📈 Version History

For a complete list of changes, see the [Changelog](CHANGELOG.md).

- **0.3.0**: Comprehensive testing, Docker containerization, environment configuration, quality assurance
- **0.2.0**: Service-oriented architecture, API access, enhanced visualization
- **0.1.x**: Initial release with core functionality

## 👥 Contributing

Contributions are welcome! Please check the [Contributing Guide](CONTRIBUTING.md) for details.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.