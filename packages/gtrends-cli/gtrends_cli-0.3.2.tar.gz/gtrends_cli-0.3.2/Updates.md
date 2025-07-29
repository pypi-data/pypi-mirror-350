# Google Trends CLI to API Migration Guide

## Project Overview

You will be transforming the existing Google Trends CLI tool into a service-oriented architecture that supports both command-line interface and HTTP API access. This will enable PHP SDK integration and make the tool available as a web service.

## Phase 1: Project Structure Reorganization

### Step 1.1: Backup Current Project
1. Create a complete backup of your current project
2. Create a new branch in Git called `feature/api-migration`
3. Work exclusively on this branch until completion

### Step 1.2: Create New Directory Structure
Transform your current structure into this enterprise-ready layout:

```
google-trends-cli/
├── src/
│   ├── gtrends_core/              # Core business logic library
│   │   ├── __init__.py
│   │   ├── services/              # Service layer classes
│   │   │   ├── __init__.py
│   │   │   ├── trending_service.py
│   │   │   ├── related_service.py
│   │   │   ├── comparison_service.py
│   │   │   ├── suggestion_service.py
│   │   │   ├── opportunity_service.py
│   │   │   ├── growth_service.py
│   │   │   └── geo_service.py
│   │   ├── models/                # Data models and DTOs
│   │   │   ├── __init__.py
│   │   │   ├── trending.py
│   │   │   ├── related.py
│   │   │   ├── comparison.py
│   │   │   └── base.py
│   │   ├── utils/                 # Shared utilities
│   │   │   ├── __init__.py
│   │   │   ├── formatters.py
│   │   │   ├── validators.py
│   │   │   └── helpers.py
│   │   └── exceptions/            # Custom exceptions
│   │       ├── __init__.py
│   │       └── trends_exceptions.py
│   ├── gtrends_cli/               # CLI presentation layer
│   │   ├── __init__.py
│   │   ├── commands/              # Individual command modules
│   │   │   ├── __init__.py
│   │   │   ├── trending.py
│   │   │   ├── related.py
│   │   │   ├── comparison.py
│   │   │   ├── suggestions.py
│   │   │   ├── opportunities.py
│   │   │   ├── growth.py
│   │   │   └── geo.py
│   │   ├── formatters/            # CLI-specific formatters
│   │   │   ├── __init__.py
│   │   │   ├── console.py
│   │   │   └── export.py
│   │   └── main.py                # Main CLI entry point
│   └── gtrends_api/               # HTTP API layer
│       ├── __init__.py
│       ├── main.py                # FastAPI application
│       ├── routers/               # API route handlers
│       │   ├── __init__.py
│       │   ├── trending.py
│       │   ├── related.py
│       │   ├── comparison.py
│       │   ├── suggestions.py
│       │   ├── opportunities.py
│       │   ├── growth.py
│       │   └── geo.py
│       ├── middleware/            # API middleware
│       │   ├── __init__.py
│       │   ├── cors.py
│       │   ├── rate_limiting.py
│       │   └── error_handling.py
│       ├── schemas/               # Pydantic models for API
│       │   ├── __init__.py
│       │   ├── requests.py
│       │   └── responses.py
│       └── dependencies/          # Dependency injection
│           ├── __init__.py
│           └── core.py
├── tests/
│   ├── unit/                      # Unit tests
│   │   ├── test_core/
│   │   ├── test_cli/
│   │   └── test_api/
│   ├── integration/               # Integration tests
│   └── conftest.py
├── docker/                        # Docker configuration
│   ├── Dockerfile.api
│   ├── Dockerfile.cli
│   └── docker-compose.yml
├── docs/                          # Documentation
│   ├── api/
│   ├── cli/
│   └── development/
├── scripts/                       # Utility scripts
│   ├── setup.sh
│   ├── test.sh
│   └── deploy.sh
├── config/                        # Configuration files
│   ├── development.yml
│   ├── production.yml
│   └── docker.yml
├── requirements/                  # Requirements by environment
│   ├── base.txt
│   ├── development.txt
│   ├── production.txt
│   └── testing.txt
├── pyproject.toml
├── setup.py
├── Makefile
├── .env.example
├── .gitignore
├── .dockerignore
└── README.md
```

### Step 1.3: Create Directory Structure
Execute these commands in your project root:

```bash
mkdir -p src/{gtrends_core/{services,models,utils,exceptions},gtrends_cli/{commands,formatters},gtrends_api/{routers,middleware,schemas,dependencies}}
mkdir -p tests/{unit/{test_core,test_cli,test_api},integration}
mkdir -p {docker,docs/{api,cli,development},scripts,config,requirements}
```

## Phase 2: Core Library Extraction

### Step 2.1: Create Base Models and DTOs
Start by defining data transfer objects that represent your data structures. This ensures type safety and clear contracts between layers.

#### Best Practices for Models:
- Use dataclasses or Pydantic models for automatic validation
- Keep models immutable where possible
- Include proper type hints
- Add docstrings for complex fields
- Implement `__str__` and `__repr__` methods

### Step 2.2: Create Custom Exceptions
Design a hierarchy of custom exceptions for better error handling:

#### Exception Design Principles:
- Inherit from appropriate base exceptions
- Include helpful error messages
- Add error codes for API responses
- Include context information
- Make exceptions serializable for API responses

### Step 2.3: Extract Service Layer Classes
Transform each CLI command into a service class following these principles:

#### Service Layer Best Practices:
- One service class per major feature area
- Each service should be stateless
- Use dependency injection for external dependencies
- Implement proper error handling and logging
- Return domain models, not raw API responses
- Include comprehensive input validation

#### Service Extraction Process:
1. **Trending Service**: Extract logic from `gtrends trending` command
2. **Related Service**: Extract logic from `gtrends related` command
3. **Comparison Service**: Extract logic from `gtrends compare` command
4. **Suggestion Service**: Extract logic from `gtrends suggest-topics` command
5. **Opportunity Service**: Extract logic from `gtrends writing-opportunities` command
6. **Growth Service**: Extract logic from `gtrends topic-growth` command
7. **Geo Service**: Extract logic from `gtrends geo-interest` and `gtrends geo` commands

#### Each Service Should Include:
- Constructor with dependency injection
- Input validation methods
- Core business logic methods
- Error handling with appropriate exceptions
- Logging for debugging and monitoring
- Unit testable methods

### Step 2.4: Create Utility Modules
Move shared functionality into utility modules:

#### Formatters Utility:
- Data transformation functions
- Export format handlers (CSV, JSON, Excel)
- Data normalization functions

#### Validators Utility:
- Input validation functions
- Region code validation
- Timeframe validation
- Category validation

#### Helpers Utility:
- Common helper functions
- Configuration management
- Constants and enums

### Step 2.5: Implement Configuration Management
Create a robust configuration system:

#### Configuration Best Practices:
- Use environment variables for sensitive data
- Support multiple configuration environments
- Implement configuration validation
- Use YAML or JSON for complex configurations
- Provide sensible defaults

## Phase 3: CLI Layer Refactoring

### Step 3.1: Create Command Modules
Split your monolithic CLI into focused command modules:

#### Command Module Structure:
Each command module should:
- Import the appropriate service from core layer
- Handle Click argument parsing
- Perform CLI-specific validation
- Call the service layer method
- Format and display results
- Handle CLI-specific errors

#### Best Practices for CLI Commands:
- Keep commands thin - delegate to services
- Use consistent error handling patterns
- Implement proper logging
- Support all export formats consistently
- Provide helpful error messages
- Include progress indicators for long operations

### Step 3.2: Create CLI-Specific Formatters
Develop formatters specifically for console output:

#### Console Formatter Features:
- Rich text formatting with colors
- Table formatting for structured data
- Progress bars for operations
- Interactive prompts when needed
- Consistent styling across commands

#### Export Formatter Features:
- Support for CSV, JSON, and Excel formats
- Proper file path handling
- Error handling for file operations
- Metadata inclusion in exports

### Step 3.3: Update Main CLI Entry Point
Restructure your main CLI file:

#### Main CLI Responsibilities:
- Register all command modules
- Set up global error handling
- Configure logging
- Handle global options
- Provide version information

## Phase 4: API Layer Development

### Step 4.1: Set Up FastAPI Application
Create a production-ready FastAPI application:

#### FastAPI Best Practices:
- Use dependency injection extensively
- Implement proper CORS handling
- Add request/response logging
- Include health check endpoints
- Implement rate limiting
- Add API versioning
- Include comprehensive API documentation

### Step 4.2: Create API Schemas
Develop Pydantic schemas for API contracts:

#### Schema Design Principles:
- Separate request and response schemas
- Include proper validation rules
- Add example values for documentation
- Use descriptive field names
- Include field descriptions

### Step 4.3: Implement API Routers
Create one router per service area:

#### Router Best Practices:
- Use consistent URL patterns
- Implement proper HTTP status codes
- Include comprehensive error handling
- Add request validation
- Use dependency injection for services
- Include rate limiting per endpoint
- Add request/response examples

### Step 4.4: Implement Middleware
Add essential middleware components:

#### CORS Middleware:
- Configure allowed origins
- Set appropriate headers
- Handle preflight requests

#### Rate Limiting Middleware:
- Implement per-IP rate limiting
- Add API key-based rate limiting
- Include rate limit headers in responses

#### Error Handling Middleware:
- Global exception handling
- Consistent error response format
- Logging of errors
- Security-conscious error messages

### Step 4.5: Add API Dependencies
Implement dependency injection:

#### Dependency Injection Benefits:
- Better testability
- Cleaner code separation
- Easier configuration management
- Better error handling

## Phase 5: Testing Strategy

### Step 5.1: Unit Testing
Implement comprehensive unit tests:

#### Unit Testing Best Practices:
- Test each service method independently
- Mock external dependencies
- Test error conditions
- Use parametrized tests for multiple scenarios
- Achieve high code coverage
- Test edge cases

### Step 5.2: Integration Testing
Create integration tests:

#### Integration Testing Focus:
- Test API endpoints end-to-end
- Test CLI commands with real services  
- Test database interactions if applicable
- Test external API interactions

### Step 5.3: API Testing
Implement API-specific tests:

#### API Testing Coverage:
- Test all endpoints
- Test authentication and authorization
- Test rate limiting
- Test error responses
- Test data validation
- Load testing for performance

## Phase 6: Configuration and Deployment

### Step 6.1: Environment Configuration
Set up proper environment management:

#### Configuration Requirements:
- Development environment settings
- Production environment settings
- Testing environment settings
- Docker environment settings
- Environment variable validation

### Step 6.2: Docker Configuration
Create production-ready Docker setup:

#### Docker Best Practices:
- Multi-stage builds for optimization
- Non-root user execution
- Proper port exposure
- Health check implementation
- Resource limit configuration
- Security scanning

### Step 6.3: Create Utility Scripts
Develop automation scripts:

#### Required Scripts:
- Setup script for development environment
- Testing script for automated testing
- Deployment script for production
- Database migration scripts if needed

### Step 6.4: Documentation
Create comprehensive documentation:

#### Documentation Requirements:
- API documentation (auto-generated from FastAPI)
- CLI documentation (updated from existing)
- Development setup guide
- Deployment guide
- Contributing guidelines
- Architecture documentation

## Phase 7: Package Management

### Step 7.1: Update Package Configuration
Modify your packaging setup:

#### Package Structure Updates:
- Update entry points for CLI
- Add API server entry point
- Update dependencies for different use cases
- Create separate package distributions if needed

### Step 7.2: Dependency Management
Organize dependencies properly:

#### Dependency Categories:
- Base dependencies (required for core functionality)
- CLI dependencies (for command-line interface)
- API dependencies (for web server)
- Development dependencies (for development tools)
- Testing dependencies (for test execution)

### Step 7.3: Version Management
Implement proper version management:

#### Version Strategy:
- Use semantic versioning
- Update version in single source of truth
- Tag releases appropriately
- Maintain changelog

## Phase 8: Quality Assurance

### Step 8.1: Code Quality Tools
Implement code quality tools:

#### Required Tools:
- Black for code formatting
- isort for import sorting
- flake8 for linting
- mypy for type checking
- bandit for security scanning

### Step 8.2: Pre-commit Hooks
Set up pre-commit hooks:

#### Pre-commit Configuration:
- Code formatting checks
- Linting checks
- Type checking
- Test execution
- Security scanning

### Step 8.3: Continuous Integration
Set up CI/CD pipeline:

#### CI/CD Requirements:
- Automated testing on multiple Python versions
- Code quality checks
- Security scanning
- Documentation building
- Package building and publishing

## Phase 9: Migration Execution

### Step 9.1: Migration Order
Execute the migration in this order:

1. Create new directory structure
2. Extract and implement core services
3. Refactor CLI to use core services
4. Implement API layer
5. Write comprehensive tests
6. Update documentation
7. Set up deployment infrastructure

### Step 9.2: Testing Each Phase
After each phase:

1. Run existing tests to ensure no regressions
2. Test CLI functionality manually
3. Write new tests for new functionality
4. Update documentation as needed

### Step 9.3: Validation Criteria
Before moving to next phase, ensure:

1. All existing CLI functionality works
2. All tests pass
3. Code quality metrics are met
4. Documentation is updated
5. No security vulnerabilities introduced

## Phase 10: PHP SDK Preparation

### Step 10.1: API Documentation
Ensure API documentation includes:

#### Documentation Requirements:
- OpenAPI/Swagger specification
- Request/response examples
- Authentication details
- Rate limiting information
- Error code documentation
- Usage examples

### Step 10.2: API Consistency
Ensure API design supports SDK generation:

#### API Design Principles:
- Consistent response formats
- Proper HTTP status codes
- Clear error messages
- Pagination support where needed
- Filtering and sorting support

### Step 10.3: API Testing for SDK
Create API tests that simulate SDK usage:

#### SDK-focused Testing:
- Test all endpoints that will be used by SDK
- Test error handling scenarios
- Test rate limiting behavior
- Test authentication flows
- Test data validation

## Success Criteria

Upon completion, you should have:

1. **Working CLI**: All existing CLI functionality preserved and working
2. **HTTP API**: Complete API covering all CLI functionality
3. **Clean Architecture**: Proper separation of concerns between layers
4. **Comprehensive Tests**: Unit and integration tests with good coverage
5. **Documentation**: Complete API and CLI documentation
6. **Deployment Ready**: Docker containers and deployment scripts
7. **SDK Ready**: API designed for easy SDK generation and consumption

## Important Notes

### Error Handling Strategy
- Always handle errors gracefully
- Provide meaningful error messages
- Log errors appropriately for debugging
- Return consistent error formats in API

### Security Considerations
- Input validation at all layers
- Rate limiting to prevent abuse
- Secure error messages (no sensitive data leakage)
- Regular security dependency updates

### Performance Considerations
- Implement caching where appropriate
- Use async operations for I/O bound tasks
- Optimize database queries if using databases
- Monitor API performance

### Maintainability
- Write clear, self-documenting code
- Include comprehensive comments for complex logic
- Follow consistent coding standards
- Keep functions and classes focused and small

This guide provides the complete roadmap for transforming your CLI tool into a service-oriented architecture. Follow each phase carefully, and don't hesitate to ask questions when you encounter challenges.