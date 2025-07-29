"""Configuration settings for the Google Trends Core library."""

import logging
import os
import time
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union

import pandas as pd
import requests
import trendspy

# Configure logging
logger = logging.getLogger(__name__)

# Default configurations
DEFAULT_REGION = "US"  # Will be overridden by IP-based location when possible
DEFAULT_TIMEFRAME = "today 1-d"  # Last 24 hours
DEFAULT_CATEGORY = "0"  # All categories
DEFAULT_SUGGESTIONS_COUNT = 10
DEFAULT_EXPORT_PATH = Path.home() / "gtrends-exports"

# Ensure export directory exists
os.makedirs(DEFAULT_EXPORT_PATH, exist_ok=True)

# Category mappings for content creators
CONTENT_CATEGORIES: Dict[str, str] = {
    "books": "22",  # Books & Literature
    "news": "16",  # News
    "arts": "5",  # Arts & Entertainment
    "fiction": "22",  # Books & Literature (we'll filter further in code)
    "culture": "3",  # Arts & Entertainment - Performing Arts
    "all": "0",  # All categories
}

# Region code mappings (partial list, will be expanded)
REGION_CODES: Dict[str, str] = {
    "yemen": "YE",
    "us": "US",
    "uk": "GB",
    "uae": "AE",
    "saudi": "SA",
    "egypt": "EG",
    "global": "",  # Empty string for global
}


# Time periods for showcase charts
class BatchPeriod(str, Enum):
    """Time periods for batch trend analysis."""

    Past4H = "custom_4h"
    Past24H = "custom_1d"
    Past48H = "custom_2d"
    Past7D = "custom_7d"


# API configuration
API_DEFAULT_TIMEOUT = 30  # seconds
API_MAX_RETRIES = 3
API_RATE_LIMIT = 60  # requests per minute

# CLI configuration
CLI_DEFAULT_OUTPUT_FORMAT = "text"


class TrendsClient:
    """Client for interacting with Google Trends API using TrendsPy."""

    def __init__(
        self,
        hl: str = "en-US",
        tz: int = 360,
        timeout: int = API_DEFAULT_TIMEOUT,
        retries: int = API_MAX_RETRIES,
    ):
        """Initialize the TrendsClient with language, timezone, and request settings.

        Args:
            hl: Language parameter
            tz: Timezone offset (360 corresponds to US CST)
            timeout: Request timeout in seconds
            retries: Number of request retries
        """
        self.trends = trendspy.Trends(hl=hl, tz=tz, timeout=timeout, retries=retries)
        self._session = requests.Session()
        self._last_request_time = 0

        # Cache for categories and geo data
        self._categories_cache = None
        self._geo_cache = {}

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
        except Exception:
            # Fallback to default region on any error
            return DEFAULT_REGION

    def get_categories(self, find: Optional[str] = None) -> List[Dict[str, str]]:
        """Get available Google Trends categories, optionally filtered by search term.

        Args:
            find: Optional search term to filter categories

        Returns:
            List of dictionaries with category information
        """
        if self._categories_cache is None:
            self._throttle_requests()
            self._categories_cache = self.trends.categories()

        if find:
            find = find.lower()
            return [cat for cat in self._categories_cache if find in cat["name"].lower()]

        return self._categories_cache

    def get_region_codes(self) -> pd.DataFrame:
        """Get all available region codes.

        Returns:
            DataFrame with region codes and names
        """
        self._throttle_requests()
        regions = self.trends.geo()

        # Convert to DataFrame with consistent columns
        data = []
        for region in regions:
            data.append(
                {
                    "code": region.get("country_code", ""),
                    "name": region.get("name", ""),
                }
            )

        return pd.DataFrame(data)

    def get_trending_searches(self, region: Optional[str] = None, limit: int = 20) -> pd.DataFrame:
        """Get real-time trending searches.

        Args:
            region: Two-letter country code (or None to auto-detect)
            limit: Maximum number of results to return

        Returns:
            DataFrame of trending searches
        """
        if region is None:
            region = self.get_current_region()

        self._throttle_requests()

        try:
            # Get trending searches
            trending = self.trends.trending_now(geo=region)

            # Convert TrendKeyword objects to DataFrame for consistent interface
            data = []
            for i, trend in enumerate(trending[:limit]):
                data.append(
                    {
                        "rank": i + 1,
                        "title": trend.keyword if hasattr(trend, "keyword") else str(trend),
                        "traffic": trend.volume if hasattr(trend, "volume") else "",
                        "news_tokens": trend.news_tokens if hasattr(trend, "news_tokens") else None,
                    }
                )

            return pd.DataFrame(data)
        except Exception as e:
            # Fall back to empty DataFrame if there's an error
            print(f"Error in get_trending_searches: {str(e)}")
            return pd.DataFrame(columns=["rank", "title", "traffic", "news_tokens"])

    def trending_now_by_rss(self, geo: Optional[str] = None) -> List:
        """Get trending searches with news articles using RSS feed.

        Args:
            geo: Two-letter country code (or None to auto-detect)

        Returns:
            List of trending search objects with news articles
        """
        if geo is None:
            geo = self.get_current_region()

        self._throttle_requests()

        try:
            return self.trends.trending_now_by_rss(geo=geo)
        except Exception as e:
            logger.error(f"Error in trending_now_by_rss: {str(e)}")
            return []

    def get_trending_searches_with_articles(
        self, region: Optional[str] = None, limit: int = 20
    ) -> Tuple[pd.DataFrame, Dict]:
        """Get trending searches with associated news articles.

        Args:
            region: Two-letter country code (or None to auto-detect)
            limit: Maximum number of results to return

        Returns:
            Tuple of (DataFrame of trending searches, Dictionary of news articles)
        """
        if region is None:
            region = self.get_current_region()

        self._throttle_requests()

        try:
            # Get trending searches with news
            trending = self.trends.trending_now_by_rss(geo=region)

            # Convert to DataFrame for consistent interface
            data = []
            news_articles = {}

            for i, trend in enumerate(trending[:limit]):
                data.append(
                    {
                        "rank": i + 1,
                        "title": trend.keyword,
                        "traffic": getattr(trend, "volume", ""),
                        "news_tokens": None,
                    }
                )

                # Store any news articles
                if hasattr(trend, "news") and trend.news:
                    articles = []
                    for article in trend.news:
                        articles.append(
                            {
                                "title": article.title,
                                "source": article.source,
                                "url": article.url,
                                "time_ago": getattr(article, "time_ago", ""),
                            }
                        )
                    news_articles[trend.keyword] = articles

            return pd.DataFrame(data), news_articles
        except Exception as e:
            logger.error(f"Error in get_trending_searches_with_articles: {str(e)}")
            return pd.DataFrame(columns=["rank", "title", "traffic", "news_tokens"]), {}

    def get_related_topics(
        self,
        query: str,
        region: Optional[str] = None,
        timeframe: str = DEFAULT_TIMEFRAME,
        category: str = DEFAULT_CATEGORY,
    ) -> Dict[str, pd.DataFrame]:
        """Get topics related to a query.

        Args:
            query: Search term
            region: Two-letter country code (or None to auto-detect)
            timeframe: Time range for data
            category: Category ID to filter results

        Returns:
            Dictionary with 'top' and 'rising' DataFrames
        """
        if region is None:
            region = self.get_current_region()

        self._throttle_requests()

        # Get related topics
        related = self.trends.related_topics(query, timeframe=timeframe, geo=region, cat=category)

        result = {}

        # Process top topics
        if "top" in related and related["top"] is not None:
            result["top"] = related["top"]

        # Process rising topics
        if "rising" in related and related["rising"] is not None:
            result["rising"] = related["rising"]

        return result

    def get_related_queries(
        self,
        query: str,
        region: Optional[str] = None,
        timeframe: str = DEFAULT_TIMEFRAME,
        category: str = DEFAULT_CATEGORY,
    ) -> Dict[str, pd.DataFrame]:
        """Get search queries related to a term.

        Args:
            query: Search term
            region: Two-letter country code (or None to auto-detect)
            timeframe: Time range for data
            category: Category ID to filter results

        Returns:
            Dictionary with 'top' and 'rising' DataFrames
        """
        if region is None:
            region = self.get_current_region()

        self._throttle_requests()

        # Get related queries
        related = self.trends.related_queries(query, timeframe=timeframe, geo=region, cat=category)

        result = {}

        # Process top queries
        if "top" in related and related["top"] is not None:
            result["top"] = related["top"]

        # Process rising queries
        if "rising" in related and related["rising"] is not None:
            result["rising"] = related["rising"]

        return result

    def get_interest_over_time(
        self,
        queries: Union[str, List[str]],
        region: Optional[str] = None,
        timeframe: Union[str, List[str]] = DEFAULT_TIMEFRAME,
        category: str = DEFAULT_CATEGORY,
    ) -> pd.DataFrame:
        """Get interest over time for up to 5 terms.

        Args:
            queries: Single search term or list of search terms (max 5)
            region: Two-letter country code (or None to auto-detect)
            timeframe: Time range for data
            category: Category ID to filter results

        Returns:
            DataFrame with interest over time
        """
        if region is None:
            region = self.get_current_region()

        # Ensure queries is a list
        if isinstance(queries, str):
            queries = [queries]

        # Limit to 5 queries (Google Trends limitation)
        if len(queries) > 5:
            queries = queries[:5]

        self._throttle_requests()

        # Get interest over time
        interest_df = self.trends.interest_over_time(
            queries, timeframe=timeframe, geo=region, cat=category
        )

        return interest_df

    def get_interest_by_region(
        self,
        queries: Union[str, List[str]],
        region: Optional[str] = None,
        timeframe: str = DEFAULT_TIMEFRAME,
        category: str = DEFAULT_CATEGORY,
        resolution: str = "COUNTRY",
    ) -> pd.DataFrame:
        """Get interest by geographic region.

        Args:
            queries: Single search term or list of search terms (max 5)
            region: Two-letter country code (or None to auto-detect)
            timeframe: Time range for data
            category: Category ID to filter results
            resolution: Geographic resolution (COUNTRY, REGION, CITY, etc.)

        Returns:
            DataFrame with interest by region
        """
        if region is None:
            region = self.get_current_region()

        # Ensure queries is a list
        if isinstance(queries, str):
            queries = [queries]

        # Limit to 5 queries (Google Trends limitation)
        if len(queries) > 5:
            queries = queries[:5]

        self._throttle_requests()

        # Get interest by region
        interest_df = self.trends.interest_by_region(
            queries, timeframe=timeframe, geo=region, cat=category, resolution=resolution
        )

        return interest_df

    def get_showcase_timeline(
        self, keywords: List[str], time_period: BatchPeriod = BatchPeriod.Past24H
    ) -> pd.DataFrame:
        """Get historical timeline data for many keywords with independent normalization.

        Args:
            keywords: List of keywords (up to 500+)
            time_period: Time period to analyze

        Returns:
            DataFrame with timeline data
        """
        try:
            self._throttle_requests()
            return self.trends.trending_now_showcase_timeline(keywords, timeframe=time_period)
        except Exception as e:
            logger.error(f"Error in get_showcase_timeline: {str(e)}")
            return pd.DataFrame()


def get_trends_client() -> TrendsClient:
    """Get a configured TrendsClient instance.

    Returns:
        TrendsClient: Configured client wrapper for TrendsPy
    """
    client = TrendsClient(timeout=API_DEFAULT_TIMEOUT, retries=API_MAX_RETRIES)
    return client
