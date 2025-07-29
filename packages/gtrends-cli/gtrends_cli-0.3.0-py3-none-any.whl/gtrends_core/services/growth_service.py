"""Service for analyzing topic growth trends over time."""

import logging
import time
from typing import List, Tuple

import pandas as pd
import requests
from trendspy import BatchPeriod

from gtrends_core.config import DEFAULT_REGION
from gtrends_core.exceptions.trends_exceptions import InvalidParameterException

logger = logging.getLogger(__name__)


class GrowthService:
    """Service for analyzing growth trends of topics over time."""

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

    def get_topic_growth_data(self, topics: List[str], time_period: str = "24h") -> pd.DataFrame:
        """Get growth data for multiple topics over a specified time period.

        Args:
            topics: List of topics to analyze
            time_period: Time period to analyze (4h, 24h, 48h, 7d)

        Returns:
            DataFrame with growth data for each topic

        Raises:
            InvalidParameterException: If the time period is invalid
        """
        # Validate time period and convert to BatchPeriod enum
        batch_period = self._convert_to_batch_period(time_period)

        # Create a default empty results dataframe
        empty_df = pd.DataFrame(
            columns=["topic", "start_value", "end_value", "growth_pct", "trend", "period"]
        )

        try:
            # Fetch real-time data for all topics
            growth_data = self.client.get_showcase_timeline(
                keywords=topics, time_period=batch_period
            )

            if growth_data.empty:
                logger.warning("No growth data returned from the API")
                return empty_df

            # Process results
            result_data = []

            # Calculate metrics for each topic
            for topic in topics:
                try:
                    # Filter data for this topic
                    if topic in growth_data.columns:
                        topic_data = growth_data[topic].reset_index()
                    else:
                        topic_df = (
                            growth_data[growth_data["query"] == topic]
                            if "query" in growth_data.columns
                            else pd.DataFrame()
                        )
                        if topic_df.empty:
                            continue
                        topic_data = topic_df.reset_index()

                    if not topic_data.empty:
                        # Calculate growth metrics
                        start_value, end_value, growth_pct = self._calculate_growth_metrics(
                            topic_data
                        )

                        # Add to results
                        result_data.append(
                            {
                                "topic": topic,
                                "start_value": start_value,
                                "end_value": end_value,
                                "growth_pct": growth_pct,
                                "trend": self._determine_trend(growth_pct),
                                "period": time_period,
                            }
                        )
                except Exception as e:
                    logger.warning(f"Error processing growth data for topic {topic}: {e}")

            # Create DataFrame with results
            if result_data:
                result_df = pd.DataFrame(result_data)

                # Sort by growth percentage in descending order
                result_df = result_df.sort_values(by="growth_pct", ascending=False).reset_index(
                    drop=True
                )
                return result_df

            return empty_df

        except Exception as e:
            logger.error(f"Error getting topic growth data: {e}")
            return empty_df

    def _convert_to_batch_period(self, period: str) -> BatchPeriod:
        """Convert a string time period to a BatchPeriod enum.

        Args:
            period: Time period string (4h, 24h, 48h, 7d)

        Returns:
            BatchPeriod enum value

        Raises:
            InvalidParameterException: If the period is invalid
        """
        period_map = {
            "4h": BatchPeriod.Past4H,
            "24h": BatchPeriod.Past24H,
            "48h": BatchPeriod.Past48H,
            "7d": BatchPeriod.Past7D,
        }

        if period not in period_map:
            raise InvalidParameterException(
                f"Invalid time period: {period}. Must be one of: 4h, 24h, 48h, 7d"
            )

        return period_map[period]

    def _batch_period_to_timeframe(self, batch_period: BatchPeriod) -> str:
        """Convert a BatchPeriod enum to a timeframe string.

        Args:
            batch_period: BatchPeriod enum value

        Returns:
            Timeframe string
        """
        period_map = {
            BatchPeriod.Past4H: "now 4-H",
            BatchPeriod.Past24H: "now 1-d",
            BatchPeriod.Past48H: "now 2-d",
            BatchPeriod.Past7D: "now 7-d",
        }

        return period_map.get(batch_period, "now 1-d")

    def _calculate_growth_metrics(self, topic_data: pd.DataFrame) -> Tuple[float, float, float]:
        """Calculate growth metrics for a topic.

        Args:
            topic_data: DataFrame containing the topic's data over time

        Returns:
            Tuple containing (start_value, end_value, growth_percentage)
        """
        # Find the value column
        value_column = None
        for col in topic_data.columns:
            if col in [
                "value",
                0,
            ]:  # The column might be named "value" or just be the first numeric column
                value_column = col
                break

        if not value_column:
            return 0.0, 0.0, 0.0

        # Sort by timestamp or date if available, otherwise use the index
        if "timestamp" in topic_data.columns:
            topic_data = topic_data.sort_values(by="timestamp")
        elif "date" in topic_data.columns:
            topic_data = topic_data.sort_values(by="date")

        # Get the first and last values
        start_value = float(topic_data[value_column].iloc[0])
        end_value = float(topic_data[value_column].iloc[-1])

        # Calculate growth percentage
        if start_value == 0:
            # Avoid division by zero
            growth_pct = 100.0 if end_value > 0 else 0.0
        else:
            growth_pct = ((end_value - start_value) / start_value) * 100.0

        return start_value, end_value, growth_pct

    def _determine_trend(self, growth_pct: float) -> str:
        """Determine the trend based on growth percentage.

        Args:
            growth_pct: Growth percentage

        Returns:
            Trend description
        """
        if growth_pct >= 50:
            return "Explosive Growth"
        elif growth_pct >= 20:
            return "Strong Growth"
        elif growth_pct >= 5:
            return "Moderate Growth"
        elif growth_pct >= -5:
            return "Stable"
        elif growth_pct >= -20:
            return "Moderate Decline"
        elif growth_pct >= -50:
            return "Strong Decline"
        else:
            return "Severe Decline"
