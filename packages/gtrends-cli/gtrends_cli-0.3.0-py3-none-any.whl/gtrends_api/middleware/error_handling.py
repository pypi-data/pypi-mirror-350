"""Error handling middleware for the API."""

import logging

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from gtrends_core.exceptions.trends_exceptions import (
    ApiRequestException,
    CategoryNotFoundException,
    ExportException,
    InvalidParameterException,
    NoDataException,
    RateLimitException,
    RegionNotFoundException,
    TimeframeParseException,
    TrendsException,
)

logger = logging.getLogger(__name__)


async def trends_exception_handler(request: Request, exc: TrendsException) -> JSONResponse:
    """Handle TrendsException and its subclasses.

    Args:
        request: FastAPI request
        exc: Exception instance

    Returns:
        JSONResponse with error details
    """
    # Log the error
    logger.error(f"TrendsException: {exc.message}")

    # Set appropriate status code based on exception type
    status_code = status.HTTP_400_BAD_REQUEST

    if isinstance(exc, ApiRequestException):
        status_code = status.HTTP_502_BAD_GATEWAY
    elif isinstance(exc, (RegionNotFoundException, CategoryNotFoundException)):
        status_code = status.HTTP_404_NOT_FOUND
    elif isinstance(exc, NoDataException):
        status_code = status.HTTP_404_NOT_FOUND
    elif isinstance(exc, RateLimitException):
        status_code = status.HTTP_429_TOO_MANY_REQUESTS
    elif isinstance(exc, InvalidParameterException):
        status_code = status.HTTP_400_BAD_REQUEST
    elif isinstance(exc, TimeframeParseException):
        status_code = status.HTTP_400_BAD_REQUEST
    elif isinstance(exc, ExportException):
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    # Return structured error response
    return JSONResponse(
        status_code=status_code,
        content=exc.to_dict(),
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle generic exceptions.

    Args:
        request: FastAPI request
        exc: Exception instance

    Returns:
        JSONResponse with error details
    """
    # Log the error
    logger.exception(f"Unhandled exception: {str(exc)}")

    # Return generic error response
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error_code": "INTERNAL_SERVER_ERROR",
            "message": "An internal server error occurred",
            "context": {"detail": str(exc)},
        },
    )


def add_exception_handlers(app: FastAPI) -> None:
    """Add all exception handlers to the FastAPI app.

    Args:
        app: FastAPI application instance
    """
    # Add handlers for specific exception types
    app.add_exception_handler(TrendsException, trends_exception_handler)
    app.add_exception_handler(ApiRequestException, trends_exception_handler)
    app.add_exception_handler(RegionNotFoundException, trends_exception_handler)
    app.add_exception_handler(CategoryNotFoundException, trends_exception_handler)
    app.add_exception_handler(NoDataException, trends_exception_handler)
    app.add_exception_handler(RateLimitException, trends_exception_handler)
    app.add_exception_handler(InvalidParameterException, trends_exception_handler)
    app.add_exception_handler(TimeframeParseException, trends_exception_handler)
    app.add_exception_handler(ExportException, trends_exception_handler)

    # Add handler for generic exceptions
    app.add_exception_handler(Exception, generic_exception_handler)
