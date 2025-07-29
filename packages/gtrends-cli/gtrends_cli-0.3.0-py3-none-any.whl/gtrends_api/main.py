"""Main FastAPI application for Google Trends API."""

import logging
import os
import sys
from typing import Dict

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from gtrends_api.middleware.error_handling import add_exception_handlers
from gtrends_api.routers import (
    comparison,
    geo,
    growth,
    opportunities,
    related,
    suggestions,
    trending,
)
from gtrends_core import __version__

logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Google Trends API",
    description="API for accessing Google Trends data",
    version=__version__,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add routes
app.include_router(trending.router, prefix="/api/v1", tags=["trending"])
app.include_router(related.router, prefix="/api/v1", tags=["related"])
app.include_router(comparison.router, prefix="/api/v1", tags=["comparison"])
app.include_router(suggestions.router, prefix="/api/v1", tags=["suggestions"])
app.include_router(opportunities.router, prefix="/api/v1", tags=["opportunities"])
app.include_router(growth.router, prefix="/api/v1", tags=["growth"])
app.include_router(geo.router, prefix="/api/v1", tags=["geo"])

# Add custom exception handlers
add_exception_handlers(app)


@app.get("/", tags=["health"])
async def root() -> Dict[str, str]:
    """Health check endpoint.

    Returns:
        Basic API information
    """
    return {
        "name": "Google Trends API",
        "version": __version__,
        "status": "ok",
    }


@app.get("/health", tags=["health"])
async def health_check() -> Dict[str, str]:
    """Health check endpoint.

    Returns:
        Health status
    """
    return {"status": "ok"}


def start_api():
    """Start the API server.

    This function is used as an entry point for the CLI.
    """
    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST")

    print(f"Starting Google Trends API server v{__version__}")
    print(f"API documentation available at http://localhost:{port}/docs")

    try:
        uvicorn.run("gtrends_api.main:app", host=host, port=port, reload=False)
    except Exception as e:
        print(f"Error starting API server: {e}")
        sys.exit(1)


if __name__ == "__main__":
    start_api()
