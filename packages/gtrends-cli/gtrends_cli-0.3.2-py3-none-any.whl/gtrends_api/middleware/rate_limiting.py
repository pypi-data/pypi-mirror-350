"""Rate limiting middleware for the API."""

import time
from typing import Callable, Dict, Optional

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from gtrends_core.config import API_RATE_LIMIT
from gtrends_core.exceptions.trends_exceptions import RateLimitException


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Middleware for rate limiting API requests."""

    def __init__(
        self, app, rate_limit_per_minute: int = API_RATE_LIMIT, exclude_paths: Optional[list] = None
    ):
        """Initialize the rate limiting middleware.

        Args:
            app: FastAPI application
            rate_limit_per_minute: Maximum number of requests per minute
            exclude_paths: List of paths to exclude from rate limiting
        """
        super().__init__(app)
        self.rate_limit = rate_limit_per_minute
        self.window_size = 60  # seconds
        self.exclude_paths = exclude_paths or ["/health", "/docs", "/redoc", "/openapi.json"]
        self.requests: Dict[str, Dict[float, int]] = {}  # client_id -> {timestamp -> count}

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process the request through the middleware.

        Args:
            request: FastAPI request
            call_next: Next middleware or endpoint handler

        Returns:
            Response object

        Raises:
            RateLimitException: If rate limit is exceeded
        """
        # Skip rate limiting for excluded paths
        if any(request.url.path.startswith(path) for path in self.exclude_paths):
            return await call_next(request)

        # Get client identifier (IP address or API key if available)
        client_id = self._get_client_id(request)

        # Check if rate limit is exceeded
        current_time = time.time()
        if self._is_rate_limited(client_id, current_time):
            retry_after = self._get_retry_after(client_id, current_time)
            raise RateLimitException(retry_after=retry_after)

        # Process the request
        response = await call_next(request)

        # Add rate limit headers
        response.headers["X-RateLimit-Limit"] = str(self.rate_limit)
        response.headers["X-RateLimit-Remaining"] = str(
            self._get_remaining(client_id, current_time)
        )
        response.headers["X-RateLimit-Reset"] = str(int(self._get_window_reset(current_time)))

        return response

    def _get_client_id(self, request: Request) -> str:
        """Get client identifier from the request.

        Args:
            request: FastAPI request

        Returns:
            Client identifier (IP or API key)
        """
        # First try to get API key from header
        api_key = request.headers.get("X-API-Key")
        if api_key:
            return f"key:{api_key}"

        # Fallback to client IP
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            # Get the first IP in the chain
            return forwarded_for.split(",")[0].strip()

        return request.client.host if request.client else "unknown"

    def _is_rate_limited(self, client_id: str, current_time: float) -> bool:
        """Check if the client has exceeded the rate limit.

        Args:
            client_id: Client identifier
            current_time: Current timestamp

        Returns:
            True if rate limited, False otherwise
        """
        # Clean up old requests
        self._cleanup_old_requests(client_id, current_time)

        # Count requests in the current window
        count = self._count_requests(client_id, current_time)

        # Add current request
        window_start = int(current_time)
        if client_id not in self.requests:
            self.requests[client_id] = {}
        if window_start not in self.requests[client_id]:
            self.requests[client_id][window_start] = 0
        self.requests[client_id][window_start] += 1

        # Check if rate limit is exceeded
        return count >= self.rate_limit

    def _cleanup_old_requests(self, client_id: str, current_time: float) -> None:
        """Remove outdated request records.

        Args:
            client_id: Client identifier
            current_time: Current timestamp
        """
        if client_id not in self.requests:
            return

        cutoff = current_time - self.window_size
        self.requests[client_id] = {
            ts: count for ts, count in self.requests[client_id].items() if ts > cutoff
        }

    def _count_requests(self, client_id: str, current_time: float) -> int:
        """Count requests in the current time window.

        Args:
            client_id: Client identifier
            current_time: Current timestamp

        Returns:
            Number of requests in the window
        """
        if client_id not in self.requests:
            return 0

        cutoff = current_time - self.window_size
        return sum(count for ts, count in self.requests[client_id].items() if ts > cutoff)

    def _get_remaining(self, client_id: str, current_time: float) -> int:
        """Get remaining requests allowed in the current window.

        Args:
            client_id: Client identifier
            current_time: Current timestamp

        Returns:
            Remaining request count
        """
        count = self._count_requests(client_id, current_time)
        return max(0, self.rate_limit - count)

    def _get_window_reset(self, current_time: float) -> float:
        """Get time when the current rate limit window resets.

        Args:
            current_time: Current timestamp

        Returns:
            Timestamp when window resets
        """
        window_start = int(current_time)
        return window_start + self.window_size

    def _get_retry_after(self, client_id: str, current_time: float) -> int:
        """Get retry after seconds for rate limited requests.

        Args:
            client_id: Client identifier
            current_time: Current timestamp

        Returns:
            Seconds to wait before retrying
        """
        if client_id not in self.requests:
            return 1

        # Find oldest timestamp in window
        oldest = min(self.requests[client_id].keys())
        return max(1, int(oldest + self.window_size - current_time))
