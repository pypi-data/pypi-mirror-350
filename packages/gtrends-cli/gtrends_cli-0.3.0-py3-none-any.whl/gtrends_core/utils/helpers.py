"""Common helper functions for Google Trends functionality."""

import logging
from datetime import datetime
from typing import Dict, List, Union

# Set up logging
logger = logging.getLogger(__name__)


def ensure_list(value: Union[str, List[str], List[dict]]) -> List:
    """Ensure a value is a list.

    Args:
        value: String, list of strings, or list of dictionaries

    Returns:
        List containing the value or the original list
    """
    if not isinstance(value, list):
        return [value]
    return value


def format_region_name(region_code: str) -> str:
    """Format a region code into a readable name.

    Args:
        region_code: Two-letter region code

    Returns:
        Formatted region name
    """
    # This is a simplified version, in a real implementation
    # we would use a country code mapping
    region_names = {
        "US": "United States",
        "GB": "United Kingdom",
        "CA": "Canada",
        "AU": "Australia",
        "IN": "India",
        "DE": "Germany",
        "FR": "France",
        "JP": "Japan",
        "BR": "Brazil",
        "RU": "Russia",
        "MX": "Mexico",
        "ES": "Spain",
        "IT": "Italy",
        "CN": "China",
        "AE": "United Arab Emirates",
    }
    return region_names.get(region_code, region_code)


def get_timestamp_str() -> str:
    """Get a formatted timestamp string for filenames.

    Returns:
        Timestamp string in format 'YYYYMMDD_HHMMSS'
    """
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def get_topic_id_map() -> Dict[int, str]:
    """Get a mapping of topic IDs to topic names.

    Returns:
        Dictionary mapping topic IDs (integers) to topic names (strings)
    """
    return {
        1: "Autos and Vehicles",
        2: "Beauty and Fashion",
        3: "Business and Finance",
        20: "Climate",
        4: "Entertainment",
        5: "Food and Drink",
        6: "Games",
        7: "Health",
        8: "Hobbies and Leisure",
        9: "Jobs and Education",
        10: "Law and Government",
        11: "Other",
        13: "Pets and Animals",
        14: "Politics",
        15: "Science",
        16: "Shopping",
        17: "Sports",
        18: "Technology",
        19: "Travel and Transportation",
    }


def truncate_string(s: str, max_length: int) -> str:
    """Truncate a string to a maximum length, adding ellipsis if truncated.

    Args:
        s: String to truncate
        max_length: Maximum length of the string

    Returns:
        Truncated string with ellipsis if needed
    """
    if len(s) <= max_length:
        return s
    return s[: max_length - 3] + "..."
