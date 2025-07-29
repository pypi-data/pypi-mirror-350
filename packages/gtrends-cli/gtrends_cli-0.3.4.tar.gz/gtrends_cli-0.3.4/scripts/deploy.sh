#!/bin/bash
# Deployment script for Google Trends CLI/API

set -e  # Exit on error

# Print colored output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Default values
DEPLOY_TARGET="docker"  # Options: docker, server
ENVIRONMENT="production"
SKIP_TESTS=false
SKIP_BUILD=false
SKIP_PUSH=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
        --target)
            DEPLOY_TARGET="$2"
            shift 2
            ;;
        --env)
            ENVIRONMENT="$2"
            shift 2
            ;;
        --skip-tests)
            SKIP_TESTS=true
            shift
            ;;
        --skip-build)
            SKIP_BUILD=true
            shift
            ;;
        --skip-push)
            SKIP_PUSH=true
            shift
            ;;
        --help)
            echo "Usage: $0 [options]"
            echo ""
            echo "Options:"
            echo "  --target TARGET    Deployment target (docker, server)"
            echo "  --env ENV          Environment (production, staging)"
            echo "  --skip-tests       Skip running tests"
            echo "  --skip-build       Skip building images"
            echo "  --skip-push        Skip pushing images"
            echo "  --help             Show this help message"
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $key${NC}"
            echo "Use --help for usage information."
            exit 1
            ;;
    esac
done

# Validate deploy target
if [[ "$DEPLOY_TARGET" != "docker" && "$DEPLOY_TARGET" != "server" ]]; then
    echo -e "${RED}Invalid deploy target: $DEPLOY_TARGET${NC}"
    echo "Valid targets are: docker, server"
    exit 1
fi

# Validate environment
if [[ "$ENVIRONMENT" != "production" && "$ENVIRONMENT" != "staging" ]]; then
    echo -e "${RED}Invalid environment: $ENVIRONMENT${NC}"
    echo "Valid environments are: production, staging"
    exit 1
fi

echo -e "${YELLOW}Deploying Google Trends CLI/API to $DEPLOY_TARGET in $ENVIRONMENT environment...${NC}"

# Run tests if not skipped
if [ "$SKIP_TESTS" = false ]; then
    echo -e "${YELLOW}Running tests...${NC}"
    ./scripts/test.sh
    echo -e "${GREEN}Tests passed!${NC}"
fi

# Set version number from package
VERSION=$(grep -E "^version\s*=" pyproject.toml | awk -F'"' '{print $2}')
echo -e "${YELLOW}Deploying version $VERSION${NC}"

# Docker deployment
if [ "$DEPLOY_TARGET" = "docker" ]; then
    if [ "$SKIP_BUILD" = false ]; then
        echo -e "${YELLOW}Building Docker images...${NC}"
        
        # Build API image
        echo -e "${YELLOW}Building API image...${NC}"
        docker build -t gtrends-api:$VERSION -t gtrends-api:latest \
            -f docker/Dockerfile.api .
        
        # Build CLI image
        echo -e "${YELLOW}Building CLI image...${NC}"
        docker build -t gtrends-cli:$VERSION -t gtrends-cli:latest \
            -f docker/Dockerfile.cli .
            
        echo -e "${GREEN}Docker images built successfully!${NC}"
    fi
    
    if [ "$SKIP_PUSH" = false ]; then
        echo -e "${YELLOW}Pushing Docker images...${NC}"
        
        # Set registry based on environment
        if [ "$ENVIRONMENT" = "production" ]; then
            REGISTRY="your-registry.com/production"
        else
            REGISTRY="your-registry.com/staging"
        fi
        
        # Tag images
        docker tag gtrends-api:$VERSION $REGISTRY/gtrends-api:$VERSION
        docker tag gtrends-api:latest $REGISTRY/gtrends-api:latest
        docker tag gtrends-cli:$VERSION $REGISTRY/gtrends-cli:$VERSION
        docker tag gtrends-cli:latest $REGISTRY/gtrends-cli:latest
        
        # Push images
        docker push $REGISTRY/gtrends-api:$VERSION
        docker push $REGISTRY/gtrends-api:latest
        docker push $REGISTRY/gtrends-cli:$VERSION
        docker push $REGISTRY/gtrends-cli:latest
        
        echo -e "${GREEN}Docker images pushed successfully!${NC}"
    fi
    
    echo -e "${YELLOW}Deploying with docker-compose...${NC}"
    
    # Set environment variables file
    ENV_FILE="config/.env.$ENVIRONMENT"
    
    # Deploy with docker-compose
    docker-compose -f docker/docker-compose.yml --env-file $ENV_FILE up -d
    
    echo -e "${GREEN}Deployment complete!${NC}"
    
    # Show running containers
    docker-compose -f docker/docker-compose.yml ps
fi

# Server deployment
if [ "$DEPLOY_TARGET" = "server" ]; then
    echo -e "${YELLOW}Deploying to server...${NC}"
    
    # Set server based on environment
    if [ "$ENVIRONMENT" = "production" ]; then
        SERVER="user@production-server.com"
        SERVER_DIR="/opt/gtrends"
    else
        SERVER="user@staging-server.com"
        SERVER_DIR="/opt/gtrends-staging"
    fi
    
    # Build package
    echo -e "${YELLOW}Building package...${NC}"
    python -m build
    
    # Deploy to server
    echo -e "${YELLOW}Copying package to server...${NC}"
    scp dist/gtrends_cli-$VERSION.tar.gz $SERVER:$SERVER_DIR/
    
    # Install on server
    echo -e "${YELLOW}Installing package on server...${NC}"
    ssh $SERVER "cd $SERVER_DIR && \
        source venv/bin/activate && \
        pip install --upgrade gtrends_cli-$VERSION.tar.gz && \
        systemctl restart gtrends-api"
    
    echo -e "${GREEN}Deployment complete!${NC}"
fi

echo -e "${GREEN}Google Trends CLI/API version $VERSION has been successfully deployed to $DEPLOY_TARGET in $ENVIRONMENT environment!${NC}" 