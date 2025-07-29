#!/bin/bash
# Testing script for Google Trends CLI/API

set -e  # Exit on error

# Print colored output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Default values
UNIT_TESTS=false
INTEGRATION_TESTS=false
COVERAGE=true
LINT=true
TYPE_CHECK=false
SECURITY_CHECK=true

# Parse arguments
while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
        --no-unit)
            UNIT_TESTS=false
            shift
            ;;
        --no-integration)
            INTEGRATION_TESTS=false
            shift
            ;;
        --no-coverage)
            COVERAGE=false
            shift
            ;;
        --no-lint)
            LINT=false
            shift
            ;;
        --no-type-check)
            TYPE_CHECK=false
            shift
            ;;
        --no-security)
            SECURITY_CHECK=false
            shift
            ;;
        --unit-only)
            INTEGRATION_TESTS=false
            LINT=false
            TYPE_CHECK=false
            SECURITY_CHECK=false
            shift
            ;;
        --integration-only)
            UNIT_TESTS=false
            LINT=false
            TYPE_CHECK=false
            SECURITY_CHECK=false
            shift
            ;;
        --lint-only)
            UNIT_TESTS=false
            INTEGRATION_TESTS=false
            COVERAGE=false
            TYPE_CHECK=false
            SECURITY_CHECK=false
            shift
            ;;
        --help)
            echo "Usage: $0 [options]"
            echo ""
            echo "Options:"
            echo "  --no-unit         Skip unit tests"
            echo "  --no-integration  Skip integration tests"
            echo "  --no-coverage     Skip coverage report"
            echo "  --no-lint         Skip linting"
            echo "  --no-type-check   Skip type checking"
            echo "  --no-security     Skip security scanning"
            echo "  --unit-only       Run only unit tests"
            echo "  --integration-only Run only integration tests"
            echo "  --lint-only       Run only linting"
            echo "  --help            Show this help message"
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $key${NC}"
            echo "Use --help for usage information."
            exit 1
            ;;
    esac
done

# Set environment variables for testing
export GTRENDS_ENV=testing

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    echo -e "${YELLOW}Activating virtual environment...${NC}"
    source venv/bin/activate
fi

# Run linting
if [ "$LINT" = true ]; then
    echo -e "${YELLOW}Running linting...${NC}"
    
    echo -e "${YELLOW}Running flake8...${NC}"
    flake8 src/ tests/
    
    echo -e "${YELLOW}Running isort check...${NC}"
    isort --check-only --profile black src/ tests/
    
    echo -e "${YELLOW}Running black check...${NC}"
    black --check src/ tests/
    
    echo -e "${GREEN}Linting passed!${NC}"
fi

# Run type checking
if [ "$TYPE_CHECK" = true ]; then
    echo -e "${YELLOW}Running mypy type checking...${NC}"
    mypy src/
    echo -e "${GREEN}Type checking passed!${NC}"
fi

# Run security scanning
if [ "$SECURITY_CHECK" = true ]; then
    echo -e "${YELLOW}Running security checks...${NC}"
    bandit -r src/ -x tests/
    echo -e "${GREEN}Security checks passed!${NC}"
fi

# Function to run tests
run_tests() {
    local test_type=$1
    local test_path=$2
    
    echo -e "${YELLOW}Running $test_type tests...${NC}"
    
    if [ "$COVERAGE" = true ]; then
        python -m pytest $test_path -v --cov=src --cov-report=term --cov-report=xml:coverage.xml
    else
        python -m pytest $test_path -v
    fi
    
    echo -e "${GREEN}$test_type tests passed!${NC}"
}

# Run unit tests
if [ "$UNIT_TESTS" = true ]; then
    run_tests "unit" "tests/unit/"
fi

# Run integration tests
if [ "$INTEGRATION_TESTS" = true ]; then
    run_tests "integration" "tests/integration/"
fi

# Print summary
echo -e "${GREEN}All tests completed successfully!${NC}" 