"""Custom exceptions for Google Trends functionality."""

from typing import Any, Dict, Optional


class TrendsException(Exception):
    """Base exception for all Google Trends related errors."""

    def __init__(
        self,
        message: str,
        error_code: str = "TRENDS_ERROR",
        context: Optional[Dict[str, Any]] = None,
    ):
        """Initialize the exception.

        Args:
            message: Human-readable error message
            error_code: Machine-readable error code
            context: Additional context information
        """
        self.message = message
        self.error_code = error_code
        self.context = context or {}
        super().__init__(self.message)

    def to_dict(self) -> Dict[str, Any]:
        """Convert the exception to a dictionary for API responses."""
        return {"error_code": self.error_code, "message": self.message, "context": self.context}


class ApiRequestException(TrendsException):
    """Exception raised when there's an error making a request to the Google Trends API."""

    def __init__(self, message: str, context: Optional[Dict[str, Any]] = None):
        super().__init__(message, error_code="API_REQUEST_ERROR", context=context)


class InvalidParameterException(TrendsException):
    """Exception raised when an invalid parameter is provided."""

    def __init__(self, message: str, param_name: str, context: Optional[Dict[str, Any]] = None):
        ctx = {"param_name": param_name}
        if context:
            ctx.update(context)
        super().__init__(message, error_code="INVALID_PARAMETER", context=ctx)


class RegionNotFoundException(TrendsException):
    """Exception raised when a region code is not found."""

    def __init__(self, region_code: str, context: Optional[Dict[str, Any]] = None):
        message = f"Region code '{region_code}' not found"
        ctx = {"region_code": region_code}
        if context:
            ctx.update(context)
        super().__init__(message, error_code="REGION_NOT_FOUND", context=ctx)


class CategoryNotFoundException(TrendsException):
    """Exception raised when a category is not found."""

    def __init__(self, category: str, context: Optional[Dict[str, Any]] = None):
        message = f"Category '{category}' not found"
        ctx = {"category": category}
        if context:
            ctx.update(context)
        super().__init__(message, error_code="CATEGORY_NOT_FOUND", context=ctx)


class TimeframeParseException(TrendsException):
    """Exception raised when a timeframe string cannot be parsed."""

    def __init__(self, timeframe: str, context: Optional[Dict[str, Any]] = None):
        message = f"Could not parse timeframe '{timeframe}'"
        ctx = {"timeframe": timeframe}
        if context:
            ctx.update(context)
        super().__init__(message, error_code="TIMEFRAME_PARSE_ERROR", context=ctx)


class NoDataException(TrendsException):
    """Exception raised when no data is available for the request."""

    def __init__(
        self,
        message: str = "No data available for this request",
        context: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message, error_code="NO_DATA_AVAILABLE", context=context)


class RateLimitException(TrendsException):
    """Exception raised when rate limit is exceeded."""

    def __init__(
        self,
        message: str = "Rate limit exceeded",
        retry_after: Optional[int] = None,
        context: Optional[Dict[str, Any]] = None,
    ):
        ctx = {}
        if retry_after is not None:
            ctx["retry_after"] = retry_after
        if context:
            ctx.update(context)
        super().__init__(message, error_code="RATE_LIMIT_EXCEEDED", context=ctx)


class ExportException(TrendsException):
    """Exception raised when there's an error exporting data."""

    def __init__(
        self, message: str, file_path: str, format: str, context: Optional[Dict[str, Any]] = None
    ):
        ctx = {"file_path": file_path, "format": format}
        if context:
            ctx.update(context)
        super().__init__(message, error_code="EXPORT_ERROR", context=ctx)


class TrendsQuotaExceededError(TrendsException):
    """Exception raised when the Google Trends API quota is exceeded for related queries/topics."""

    def __init__(self, context: Optional[Dict[str, Any]] = None):
        message = (
            "API quota exceeded for related queries/topics. "
            "To resolve this, you can try:\n"
            "1. Use a different referer in request headers:\n"
            "   tr.related_queries(keyword, headers={'referer': 'https://www.google.com/'})\n"
            "2. Use a different IP address by configuring a proxy:\n"
            "   tr.set_proxy('http://proxy:port')\n"
            "   # or\n"
            "   tr = Trends(proxy={'http': 'http://proxy:port', 'https': 'https://proxy:port'})\n"
            "3. Wait before making additional requests"
        )
        super().__init__(message, error_code="QUOTA_EXCEEDED", context=context)
