"""CORS middleware for the API."""

from typing import List, Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def add_cors_middleware(
    app: FastAPI,
    allow_origins: Optional[List[str]] = None,
    allow_origin_regex: Optional[str] = None,
    allow_methods: Optional[List[str]] = None,
    allow_headers: Optional[List[str]] = None,
    allow_credentials: bool = False,
    expose_headers: Optional[List[str]] = None,
    max_age: int = 600,
) -> None:
    """Add CORS middleware to the FastAPI application.

    Args:
        app: FastAPI application
        allow_origins: List of allowed origins
        allow_origin_regex: Regex pattern for allowed origins
        allow_methods: List of allowed HTTP methods
        allow_headers: List of allowed HTTP headers
        allow_credentials: Whether to allow credentials
        expose_headers: List of headers to expose
        max_age: Max age for CORS preflight requests
    """
    # Default values
    if allow_origins is None:
        allow_origins = ["*"]
    if allow_methods is None:
        allow_methods = ["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD", "PATCH"]
    if allow_headers is None:
        allow_headers = ["*"]
    if expose_headers is None:
        expose_headers = [
            "Content-Type",
            "X-RateLimit-Limit",
            "X-RateLimit-Remaining",
            "X-RateLimit-Reset",
        ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=allow_origins,
        allow_origin_regex=allow_origin_regex,
        allow_methods=allow_methods,
        allow_headers=allow_headers,
        allow_credentials=allow_credentials,
        expose_headers=expose_headers,
        max_age=max_age,
    )
