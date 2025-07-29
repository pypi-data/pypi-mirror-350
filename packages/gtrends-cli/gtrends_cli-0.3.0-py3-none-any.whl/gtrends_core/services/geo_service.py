"""Service for geographical interest analysis based on Google Trends data."""

import logging
import time
from typing import Optional

import pandas as pd
import requests

from gtrends_core.config import DEFAULT_REGION
from gtrends_core.exceptions.trends_exceptions import InvalidParameterException
from gtrends_core.utils.validators import validate_region_code

logger = logging.getLogger(__name__)


class GeoService:
    """Service for analyzing geographical interest from Google Trends data."""

    def __init__(self, trends_client):
        """Initialize with a TrendsClient instance.

        Args:
            trends_client: Initialized TrendsClient instance
        """
        self.client = trends_client
        self._session = requests.Session()
        self._last_request_time = 0

    def _throttle_requests(self, min_interval: float = 1.0):
        """Prevent sending too many requests in a short time.

        Args:
            min_interval: Minimum time between requests in seconds
        """
        current_time = time.time()
        time_since_last = current_time - self._last_request_time

        if time_since_last < min_interval:
            time.sleep(min_interval - time_since_last)

        self._last_request_time = time.time()

    def get_current_region(self) -> str:
        """Determine the user's current region based on IP.

        Returns:
            Two-letter country code
        """
        try:
            self._throttle_requests()
            response = self._session.get("https://ipinfo.io/json", timeout=5)
            data = response.json()
            return data.get("country", DEFAULT_REGION)
        except Exception as e:
            # Fallback to default region on any error
            logger.warning(f"Failed to detect region: {str(e)}")
            return DEFAULT_REGION

    def get_interest_by_region(
        self,
        query: str,
        region: Optional[str] = None,
        resolution: str = "COUNTRY",
        timeframe: str = "today 12-m",
        category: str = "0",
        count: int = 20,
    ) -> pd.DataFrame:
        """Get geographical interest data for a query.

        Args:
            query: Search term to analyze
            region: Two-letter country code (or None to auto-detect)
            resolution: Geographic resolution level (COUNTRY, REGION, CITY, DMA)
            timeframe: Time range for data
            category: Category ID to filter results
            count: Number of regions to include in results

        Returns:
            DataFrame with geographical interest data

        Raises:
            InvalidParameterException: If any parameters are invalid
        """
        # Validate parameters
        if region:
            region = validate_region_code(region)
        else:
            try:
                region = self.client.get_current_region()
            except (AttributeError, Exception):
                region = self.get_current_region()

        if resolution not in ["COUNTRY", "REGION", "CITY", "DMA"]:
            raise InvalidParameterException(
                f"Invalid resolution: {resolution}. Must be one of: COUNTRY, REGION, CITY, DMA"
            )

        # Get interest by region data
        try:
            geo_data = self.client.get_interest_by_region(
                queries=query,
                region=region,
                resolution=resolution,
                timeframe=timeframe,
                category=category,
            )

            # Process results
            if not geo_data.empty:
                # Sort by value in descending order
                geo_data = geo_data.sort_values(by="value", ascending=False).reset_index(drop=True)

                # Limit to the requested count
                if len(geo_data) > count:
                    geo_data = geo_data.head(count)

                # Add percentile ranks
                geo_data["percentile"] = self._calculate_percentiles(geo_data["value"])

                # Add interest category
                geo_data["interest_level"] = geo_data["percentile"].apply(self._categorize_interest)

                return geo_data

        except Exception as e:
            logger.error(f"Error getting interest by region: {e}")

        # Return empty DataFrame if no results or error
        columns = ["geoName", "geoCode", "value", "percentile", "interest_level"]
        return pd.DataFrame(columns=columns)

    def get_geo_codes_by_search(self, search_term: str) -> pd.DataFrame:
        """Search for region codes based on a search term.

        Args:
            search_term: Search term to find matching regions

        Returns:
            DataFrame with matching region codes and names
        """
        try:
            # Get region codes
            geo_codes = self.client.get_region_codes()

            # Filter based on search term
            if search_term and not geo_codes.empty:
                search_lower = search_term.lower()

                # Search in country names and region codes (case-insensitive)
                mask = geo_codes["name"].str.lower().str.contains(search_lower) | geo_codes[
                    "code"
                ].str.lower().str.contains(search_lower)

                geo_codes = geo_codes[mask].reset_index(drop=True)

            return geo_codes
        except Exception as e:
            logger.error(f"Error getting geo codes: {e}")
            return pd.DataFrame(columns=["code", "name"])

    def _calculate_percentiles(self, values: pd.Series) -> pd.Series:
        """Calculate percentile ranks for values.

        Args:
            values: Series of values

        Returns:
            Series of percentile ranks (0-100)
        """
        # Rank from 0 to 100
        max_val = values.max()
        if max_val > 0:
            return (values / max_val) * 100
        else:
            return pd.Series([0] * len(values))

    def _categorize_interest(self, percentile: float) -> str:
        """Categorize interest level based on percentile.

        Args:
            percentile: Percentile value (0-100)

        Returns:
            Interest level category
        """
        if percentile >= 80:
            return "Very High Interest"
        elif percentile >= 60:
            return "High Interest"
        elif percentile >= 40:
            return "Moderate Interest"
        elif percentile >= 20:
            return "Low Interest"
        else:
            return "Very Low Interest"
