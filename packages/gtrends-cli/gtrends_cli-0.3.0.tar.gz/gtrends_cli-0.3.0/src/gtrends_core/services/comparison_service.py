"""Comparison service for comparing interest in multiple topics from Google Trends."""

import logging
import time
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Union

import pandas as pd
import requests

from gtrends_core.config import DEFAULT_CATEGORY, DEFAULT_REGION, DEFAULT_TIMEFRAME
from gtrends_core.exceptions.trends_exceptions import ApiRequestException, NoDataException
from gtrends_core.models.base import RegionInterest, TimePoint
from gtrends_core.models.comparison import InterestByRegionResult, InterestOverTimeResult
from gtrends_core.utils.helpers import ensure_list, format_region_name

logger = logging.getLogger(__name__)


class ComparisonService:
    """Service for comparing interest across different topics."""

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

    def get_interest_over_time(
        self,
        queries: Union[str, List[str]],
        region: Optional[str] = None,
        timeframe: Union[str, List[str]] = DEFAULT_TIMEFRAME,
        category: str = DEFAULT_CATEGORY,
    ) -> InterestOverTimeResult:
        """Get interest over time for multiple queries.

        Args:
            queries: Search term or list of search terms
            region: Two-letter country code (or None to auto-detect)
            timeframe: Time range for data or list of time ranges
            category: Category ID to filter results

        Returns:
            InterestOverTimeResult with time series data for each query

        Raises:
            ApiRequestException: If API request fails
            NoDataException: If no data is available
        """
        try:
            if region is None:
                region = self.get_current_region()

            # Ensure queries is a list
            queries_list = ensure_list(queries)

            # Get interest over time data
            results_df = self.client.get_interest_over_time(
                queries=queries_list, region=region, timeframe=timeframe, category=category
            )

            if results_df is None or results_df.empty:
                raise NoDataException(f"No interest data available for {queries_list}")

            # Convert to our data model
            time_series = {}
            for topic in queries_list:
                if topic not in results_df.columns:
                    continue

                points = []
                for date, row in results_df.iterrows():
                    if isinstance(date, str):
                        try:
                            date_obj = datetime.strptime(date, "%Y-%m-%d")
                        except ValueError:
                            # Try parsing with time
                            try:
                                date_obj = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
                            except ValueError:
                                continue
                    else:
                        date_obj = date

                    points.append(TimePoint(date=date_obj, value=float(row[topic])))
                time_series[topic] = points

            region_name = format_region_name(region)
            return InterestOverTimeResult(
                topics=queries_list,
                region_code=region,
                region_name=region_name,
                timeframe=timeframe,
                category=category,
                time_series=time_series,
            )

        except NoDataException:
            raise
        except Exception as e:
            logger.error(f"Error fetching interest over time: {str(e)}")
            raise ApiRequestException(f"Failed to fetch interest over time: {str(e)}")

    def visualize_comparison(
        self,
        comparison_result: InterestOverTimeResult,
        export_path: Optional[Union[str, Path]] = None,
    ) -> Optional[Path]:
        """Generate visualization for interest over time data.

        Args:
            comparison_result: The InterestOverTimeResult object with time series data
            export_path: Optional path to save the visualization (if None, displays it)

        Returns:
            Path where the visualization was saved, or None if displayed

        Raises:
            ImportError: If matplotlib is not installed
            Exception: For other visualization errors
        """
        try:
            import matplotlib.pyplot as plt
            from rich.console import Console

            console = Console()

            # Convert time series data to DataFrame for plotting
            data = {}
            dates = set()

            # Collect all dates and values
            for topic, points in comparison_result.time_series.items():
                topic_data = {}
                for point in points:
                    dates.add(point.date)
                    topic_data[point.date] = point.value
                data[topic] = topic_data

            # Sort dates
            sorted_dates = sorted(dates)

            # Create DataFrame
            plot_data = pd.DataFrame(index=sorted_dates)
            for topic, topic_data in data.items():
                plot_data[topic] = [topic_data.get(date, None) for date in sorted_dates]

            # Create plot
            plt.figure(figsize=(12, 6))
            for topic in comparison_result.topics:
                if topic in plot_data.columns:
                    plt.plot(plot_data.index, plot_data[topic], label=topic, linewidth=2)

            # Add details
            plt.title(f"Interest Comparison - {comparison_result.region_name}")
            plt.xlabel("Date")
            plt.ylabel("Interest")
            plt.legend(loc="best")
            plt.grid(True, alpha=0.3)

            # Format date labels
            plt.gcf().autofmt_xdate()

            # Save or show the plot
            if export_path:
                if isinstance(export_path, str):
                    export_path = Path(export_path)

                # Ensure directory exists
                export_path.parent.mkdir(parents=True, exist_ok=True)

                plt.savefig(export_path, dpi=300, bbox_inches="tight")
                console.print(f"[green]Visualization saved to: {export_path}[/green]")
                return export_path
            else:
                plt.show()
                return None

        except ImportError:
            from rich.console import Console

            console = Console()
            console.print(
                "[yellow]Matplotlib is required for visuals. run: pip install matplotlib[/yellow]"
            )
            raise
        except Exception as e:
            logger.error(f"Error creating visualization: {str(e)}")
            raise

    def get_interest_by_region(
        self,
        queries: Union[str, List[str]],
        region: Optional[str] = None,
        timeframe: str = DEFAULT_TIMEFRAME,
        category: str = DEFAULT_CATEGORY,
        resolution: str = "COUNTRY",
    ) -> InterestByRegionResult:
        """Get interest by geographic region for multiple queries.

        Args:
            queries: Search term or list of search terms
            region: Two-letter country code (or None to auto-detect)
            timeframe: Time range for data
            category: Category ID to filter results
            resolution: Geographic resolution (COUNTRY, REGION, CITY, DMA)

        Returns:
            InterestByRegionResult with regional interest data

        Raises:
            ApiRequestException: If API request fails
            NoDataException: If no data is available
        """
        try:
            if region is None:
                region = self.get_current_region()

            # Ensure queries is a list
            queries_list = ensure_list(queries)

            # Get interest by region data
            results_df = self.client.get_interest_by_region(
                queries=queries_list,
                region=region,
                timeframe=timeframe,
                category=category,
                resolution=resolution,
            )

            if results_df is None or results_df.empty:
                raise NoDataException(f"No regional interest data available for {queries_list}")

            # Convert to our data model
            region_interest = {}

            for query in queries_list:
                if query not in results_df.columns:
                    continue

                regions = []
                for idx, row in results_df.iterrows():
                    region_code = idx  # The index should be the region code/name
                    region_name = idx  # We might need a mapping function here

                    regions.append(
                        RegionInterest(
                            region_code=region_code,
                            region_name=region_name,
                            value=float(row[query]),
                        )
                    )

                # Sort by value descending
                regions.sort(key=lambda x: x.value, reverse=True)
                region_interest[query] = regions

            region_name = format_region_name(region)
            return InterestByRegionResult(
                topics=queries_list,
                region_code=region,
                region_name=region_name,
                timeframe=timeframe,
                category=category,
                resolution=resolution,
                region_interest=region_interest,
            )

        except NoDataException:
            raise
        except Exception as e:
            logger.error(f"Error fetching interest by region: {str(e)}")
            raise ApiRequestException(f"Failed to fetch interest by region: {str(e)}")
