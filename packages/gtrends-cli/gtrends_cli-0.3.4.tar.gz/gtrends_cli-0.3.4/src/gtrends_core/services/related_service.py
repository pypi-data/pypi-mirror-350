"""Related service for fetching related topics and queries from Google Trends."""

import logging
import time
from typing import Optional

import requests

from gtrends_core.config import DEFAULT_CATEGORY, DEFAULT_REGION, DEFAULT_TIMEFRAME
from gtrends_core.exceptions.trends_exceptions import ApiRequestException, NoDataException
from gtrends_core.models.base import RelatedTopic
from gtrends_core.models.related import RelatedData, RelatedQueryResults, RelatedTopicResults
from gtrends_core.utils.helpers import format_region_name

logger = logging.getLogger(__name__)


class RelatedService:
    """Service for fetching related topics and queries from Google Trends."""

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

    def get_related_data(
        self,
        query: str,
        region: Optional[str] = None,
        timeframe: str = DEFAULT_TIMEFRAME,
        category: str = DEFAULT_CATEGORY,
    ) -> RelatedData:
        """Get both topics and queries related to a search term.

        Args:
            query: Search term
            region: Two-letter country code (or None to auto-detect)
            timeframe: Time range for data
            category: Category ID to filter results

        Returns:
            RelatedData object with both related topics and queries

        Raises:
            ApiRequestException: If API request fails
            NoDataException: If no data is available
        """
        try:
            # Get both related topics and queries
            topics_result = self.get_related_topics(query, region, timeframe, category)
            queries_result = self.get_related_queries(query, region, timeframe, category)

            # Create a combined result
            return RelatedData(
                query=query,
                region_code=topics_result.region_code,
                region_name=topics_result.region_name,
                timeframe=timeframe,
                category=category,
                topics={"top": topics_result.top_topics, "rising": topics_result.rising_topics},
                queries={
                    "top": queries_result.top_queries,
                    "rising": queries_result.rising_queries,
                },
            )

        except Exception as e:
            logger.error(f"Error fetching related data: {str(e)}")
            raise ApiRequestException(f"Failed to fetch related data: {str(e)}")

    def get_related_topics(
        self,
        query: str,
        region: Optional[str] = None,
        timeframe: str = DEFAULT_TIMEFRAME,
        category: str = DEFAULT_CATEGORY,
    ) -> RelatedTopicResults:
        """Get topics related to a query.

        Args:
            query: Search term
            region: Two-letter country code (or None to auto-detect)
            timeframe: Time range for data
            category: Category ID to filter results

        Returns:
            RelatedTopicResults object with related topics

        Raises:
            ApiRequestException: If API request fails
            NoDataException: If no data is available
        """
        try:
            if region is None:
                region = self.get_current_region()

            # Get related topics from Google Trends
            results = self.client.get_related_topics(
                query=query, region=region, timeframe=timeframe, category=category
            )

            if not results or ("top" not in results and "rising" not in results):
                raise NoDataException(f"No related topics available for '{query}'")

            # Extract top and rising topics
            top_topics = []
            if "top" in results and not results["top"].empty:
                for _, row in results["top"].iterrows():
                    top_topics.append(
                        RelatedTopic(
                            title=row.get("topic_title", ""),
                            value=float(row.get("value", 0)),
                            is_rising=False,
                        )
                    )

            rising_topics = []
            if "rising" in results and not results["rising"].empty:
                for _, row in results["rising"].iterrows():
                    # Handle "Breakout" values
                    value_text = None
                    value = 0.0

                    if isinstance(row.get("value"), str) and row.get("value").lower() == "breakout":
                        value_text = "Breakout"
                        value = 5000.0  # Arbitrary high value for sorting
                    else:
                        try:
                            value = float(row.get("value", 0))
                        except (ValueError, TypeError):
                            value = 0.0

                    rising_topics.append(
                        RelatedTopic(
                            title=row.get("topic_title", ""),
                            value=value,
                            is_rising=True,
                            rising_value_text=value_text,
                        )
                    )

            region_name = format_region_name(region)
            return RelatedTopicResults(
                query=query,
                region_code=region,
                region_name=region_name,
                timeframe=timeframe,
                category=category,
                top_topics=top_topics,
                rising_topics=rising_topics,
            )

        except NoDataException:
            raise
        except Exception as e:
            logger.error(f"Error fetching related topics: {str(e)}")
            raise ApiRequestException(f"Failed to fetch related topics: {str(e)}")

    def get_related_queries(
        self,
        query: str,
        region: Optional[str] = None,
        timeframe: str = DEFAULT_TIMEFRAME,
        category: str = DEFAULT_CATEGORY,
    ) -> RelatedQueryResults:
        """Get queries related to a search term.

        Args:
            query: Search term
            region: Two-letter country code (or None to auto-detect)
            timeframe: Time range for data
            category: Category ID to filter results

        Returns:
            RelatedQueryResults object with related queries

        Raises:
            ApiRequestException: If API request fails
            NoDataException: If no data is available
        """
        try:
            if region is None:
                region = self.get_current_region()

            # Get related queries from Google Trends
            results = self.client.get_related_queries(
                query=query, region=region, timeframe=timeframe, category=category
            )

            if not results or ("top" not in results and "rising" not in results):
                raise NoDataException(f"No related queries available for '{query}'")

            # Extract top and rising queries
            top_queries = []
            if "top" in results and not results["top"].empty:
                for _, row in results["top"].iterrows():
                    top_queries.append(
                        RelatedTopic(
                            title=row.get("query", ""),
                            value=float(row.get("value", 0)),
                            is_rising=False,
                        )
                    )

            rising_queries = []
            if "rising" in results and not results["rising"].empty:
                for _, row in results["rising"].iterrows():
                    # Handle "Breakout" values
                    value_text = None
                    value = 0.0

                    if isinstance(row.get("value"), str) and row.get("value").lower() == "breakout":
                        value_text = "Breakout"
                        value = 5000.0  # Arbitrary high value for sorting
                    else:
                        try:
                            value = float(row.get("value", 0))
                        except (ValueError, TypeError):
                            value = 0.0

                    rising_queries.append(
                        RelatedTopic(
                            title=row.get("query", ""),
                            value=value,
                            is_rising=True,
                            rising_value_text=value_text,
                        )
                    )

            region_name = format_region_name(region)
            return RelatedQueryResults(
                query=query,
                region_code=region,
                region_name=region_name,
                timeframe=timeframe,
                category=category,
                top_queries=top_queries,
                rising_queries=rising_queries,
            )

        except NoDataException:
            raise
        except Exception as e:
            logger.error(f"Error fetching related queries: {str(e)}")
            raise ApiRequestException(f"Failed to fetch related queries: {str(e)}")
