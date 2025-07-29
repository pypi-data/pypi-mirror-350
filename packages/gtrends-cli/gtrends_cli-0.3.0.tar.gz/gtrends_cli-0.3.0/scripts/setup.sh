#!/bin/bash
# Setup script for Google Trends CLI/API development environment

set -e  # Exit on error

# Print colored output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Setting up Google Trends CLI/API development environment...${NC}"

# Check Python version
python_version=$(python3 --version)
echo -e "Using ${GREEN}$python_version${NC}"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    python3 -m venv venv
fi

# Activate virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
source venv/bin/activate

# Install development dependencies
echo -e "${YELLOW}Installing development dependencies...${NC}"
pip install -r requirements/development.txt

# Create necessary directories
echo -e "${YELLOW}Creating necessary directories...${NC}"
mkdir -p logs
mkdir -p gtrends-exports

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}Creating .env file from template...${NC}"
    cp .env.example .env
    echo -e "${GREEN}Created .env file. Please edit it with your configuration.${NC}"
fi

# Install the package in development mode
echo -e "${YELLOW}Installing package in development mode...${NC}"
pip install -e .

# Run tests to verify setup
echo -e "${YELLOW}Running tests to verify setup...${NC}"
pytest -xvs tests/

echo -e "${GREEN}Setup complete!${NC}"
echo -e "To activate the environment in the future, run: ${YELLOW}source venv/bin/activate${NC}"
echo -e "To run the CLI: ${YELLOW}gtrends --help${NC}"
echo -e "To run the API: ${YELLOW}python -m src.gtrends_api.main${NC}" 