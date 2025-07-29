"""Validation utilities for Google Trends functionality."""

import os
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Union

from gtrends_core.config import DEFAULT_EXPORT_PATH, BatchPeriod
from gtrends_core.exceptions.trends_exceptions import (
    InvalidParameterException,
    RegionNotFoundException,
    TimeframeParseException,
)

# Regex for timeframe validation
TIMEFRAME_PATTERN = re.compile(
    r"^(?:now|today) (\d+)-([HhdmMy])$|"
    r"^(\d{4}-\d{2}-\d{2})(?: (\d+)-[d])?$|"
    r"^(\d{4}-\d{2}-\d{2}) (\d{4}-\d{2}-\d{2})$|"
    r"^(\d{4}-\d{2}-\d{2}T\d{1,2}) (\d{4}-\d{2}-\d{2}T\d{1,2})$|"
    r"^all$"
)


def validate_region_code(region_code: str) -> str:
    """Validate a region code.

    Args:
        region_code: Two-letter region code

    Returns:
        Validated region code (uppercase)

    Raises:
        RegionNotFoundException: If region code is invalid
    """
    # This is a simplified validation, just checking format
    # In a real implementation, we would check against a list of valid codes
    if not region_code or not isinstance(region_code, str):
        raise InvalidParameterException("Region code must be a string", param_name="region_code")

    region_code = region_code.upper()
    if not re.match(r"^[A-Z]{2}$", region_code):
        raise RegionNotFoundException(region_code)

    return region_code


def convert_timeframe(timeframe: str) -> str:
    """Convert a timeframe string to Google Trends API format.

    Args:
        timeframe: Timeframe string in various formats

    Returns:
        Timeframe string in Google Trends API format

    Raises:
        TimeframeParseException: If timeframe format is invalid
    """
    # Check for common patterns
    if timeframe.lower() in ("now", "today"):
        return "now 1-H"

    # Check for period formats like "now 7-d" or "today 12-m"
    period_match = re.match(r"^(now|today) (\d+)-([HhdmMy])$", timeframe, re.IGNORECASE)
    if period_match:
        base, value, unit = period_match.groups()
        unit = unit.lower()
        return f"{base.lower()} {value}-{unit}"

    # Check for specific date formats
    date_match = re.match(r"^(\d{4}-\d{2}-\d{2})$", timeframe)
    if date_match:
        date_str = date_match.group(1)
        try:
            # Validate the date by parsing it
            datetime.strptime(date_str, "%Y-%m-%d")
            # Single date means that specific day
            tomorrow = (datetime.strptime(date_str, "%Y-%m-%d") + timedelta(days=1)).strftime(
                "%Y-%m-%d"
            )
            return f"{date_str} {tomorrow}"
        except ValueError:
            raise TimeframeParseException(timeframe)

    # Check for date range format like "2020-01-01 2020-12-31"
    range_match = re.match(r"^(\d{4}-\d{2}-\d{2}) (\d{4}-\d{2}-\d{2})$", timeframe)
    if range_match:
        start, end = range_match.groups()
        try:
            # Validate the dates by parsing them
            start_date = datetime.strptime(start, "%Y-%m-%d")
            end_date = datetime.strptime(end, "%Y-%m-%d")
            if start_date >= end_date:
                raise TimeframeParseException(f"Start date {start} must be before end date {end}")
            return f"{start} {end}"
        except ValueError:
            raise TimeframeParseException(timeframe)

    # Check for "all" timeframe
    if timeframe.lower() == "all":
        return "all"

    # If we got here, the format is invalid
    raise TimeframeParseException(timeframe)


def check_timeframe_resolution(timeframe: str) -> str:
    """Check if a timeframe has the right resolution based on its duration.

    Args:
        timeframe: Timeframe string

    Returns:
        Valid timeframe string with adjusted resolution if needed

    Raises:
        TimeframeParseException: If timeframe is invalid
    """
    try:
        # First make sure it's a valid timeframe
        timeframe = convert_timeframe(timeframe)

        # Handle special cases
        if timeframe == "all":
            return timeframe

        # Process relative timeframes (now X-unit or today X-unit)
        period_match = re.match(r"^(now|today) (\d+)-([HhdmMy])$", timeframe, re.IGNORECASE)
        if period_match:
            _, value, unit = period_match.groups()
            value = int(value)
            unit = unit.lower()

            # Adjust resolution based on timespan
            if unit == "h" and value > 4:
                # For hourly data, max resolution is 4 hours, then we need to use daily
                return f"today {value // 24 + 1}-d"
            elif unit == "d" and value > 90:
                # For daily data, max resolution is ~90 days, then we need monthly
                return f"today {value // 30 + 1}-m"
            elif unit == "m" and value > 36:
                # For monthly data, max resolution is ~36 months, then we need yearly
                return f"today {value // 12 + 1}-y"

            # Otherwise, the resolution is fine
            return timeframe

        # Process date range timeframes
        range_match = re.match(r"^(\d{4}-\d{2}-\d{2}) (\d{4}-\d{2}-\d{2})$", timeframe)
        if range_match:
            start, end = range_match.groups()
            start_date = datetime.strptime(start, "%Y-%m-%d")
            end_date = datetime.strptime(end, "%Y-%m-%d")
            days_diff = (end_date - start_date).days

            # Adjust resolution based on range
            if days_diff <= 1:
                # For very short ranges, we need hourly data
                return f"now {days_diff * 24}-H"
            elif days_diff <= 90:
                # Keep daily resolution for up to 90 days
                return timeframe
            elif days_diff <= 1095:  # ~3 years
                # For longer ranges, monthly resolution is better
                months = days_diff // 30
                return f"today {months}-m"
            else:
                # For very long ranges, yearly resolution
                years = days_diff // 365
                return f"today {years}-y"

        # We shouldn't get here with a valid timeframe
        raise TimeframeParseException(timeframe)

    except Exception as e:
        if isinstance(e, TimeframeParseException):
            raise
        raise TimeframeParseException(str(e))


def parse_timeframe(timeframe: str) -> str:
    """Parse and validate a timeframe string.

    Args:
        timeframe: Timeframe string

    Returns:
        Validated timeframe string

    Raises:
        TimeframeParseException: If timeframe is invalid
    """
    if not timeframe or not isinstance(timeframe, str):
        raise InvalidParameterException("Timeframe must be a string", param_name="timeframe")

    try:
        return convert_timeframe(timeframe)
    except TimeframeParseException:
        # If conversion fails, check if it matches the raw pattern
        match = TIMEFRAME_PATTERN.match(timeframe)
        if not match:
            raise TimeframeParseException(timeframe)
        return timeframe


def validate_batch_period(period: Union[str, BatchPeriod]) -> BatchPeriod:
    """Validate a batch period value.

    Args:
        period: BatchPeriod enum value or string

    Returns:
        BatchPeriod enum value

    Raises:
        InvalidParameterException: If period is invalid
    """
    # If it's already a BatchPeriod, return it
    if isinstance(period, BatchPeriod):
        return period

    # Try to convert from string
    try:
        return BatchPeriod(period)
    except (ValueError, TypeError):
        # Try as a direct enum name
        try:
            return getattr(BatchPeriod, period)
        except (AttributeError, TypeError):
            valid_periods = ", ".join([p.value for p in BatchPeriod])
            raise InvalidParameterException(
                f"Period must be one of: {valid_periods}", param_name="period"
            )


def validate_category(category: str) -> str:
    """Validate a category ID.

    Args:
        category: Category ID

    Returns:
        Validated category ID

    Raises:
        InvalidParameterException: If category ID is invalid
    """
    # This is a simplified validation, just checking format
    # In a real implementation, we would check against a list of valid categories
    if not category or not isinstance(category, str):
        raise InvalidParameterException("Category must be a string", param_name="category")

    # Check if it's a valid category format (all or a number)
    if category != "0" and not (category == "all" or category.isdigit()):
        raise InvalidParameterException(
            "Category must be 'all' or a numeric ID", param_name="category"
        )

    return category


def validate_trend_keyword(keyword: Any) -> bool:
    """Validate if an object is a valid TrendKeyword or TrendKeywordLite.

    Args:
        keyword: Object to validate

    Returns:
        True if valid, False otherwise
    """
    # Check if it has the essential attributes of a TrendKeyword/TrendKeywordLite
    essential_attrs = ["keyword"]
    return hasattr(keyword, "__dict__") and all(hasattr(keyword, attr) for attr in essential_attrs)


def validate_resolution(resolution: str) -> str:
    """Validate a geographic resolution value.

    Args:
        resolution: Resolution string (COUNTRY, REGION, CITY, DMA)

    Returns:
        Validated resolution string

    Raises:
        InvalidParameterException: If resolution is invalid
    """
    valid_resolutions = ["COUNTRY", "REGION", "CITY", "DMA"]
    if resolution not in valid_resolutions:
        raise InvalidParameterException(
            f"Resolution must be one of: {', '.join(valid_resolutions)}", param_name="resolution"
        )

    return resolution


def validate_export_path(export_path: Union[str, Path, None] = None) -> Path:
    """Validate and convert export path to Path object.

    Args:
        export_path: Export path string or Path object

    Returns:
        Validated Path object

    Raises:
        InvalidParameterException: If export path is invalid
    """
    if export_path is None:
        # Use default if not provided
        export_path = DEFAULT_EXPORT_PATH
    elif isinstance(export_path, str):
        # Convert string to Path and expand user directory
        export_path = Path(os.path.expanduser(export_path))
    elif not isinstance(export_path, Path):
        raise InvalidParameterException(
            "Export path must be a string or Path object", param_name="export_path"
        )

    # Ensure path exists
    os.makedirs(export_path, exist_ok=True)

    # Check if path is writable
    if not os.access(export_path, os.W_OK):
        raise InvalidParameterException(
            f"Export path '{export_path}' is not writable", param_name="export_path"
        )

    return export_path
