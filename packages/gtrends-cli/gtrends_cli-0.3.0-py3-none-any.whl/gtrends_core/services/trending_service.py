"""Trending service for fetching trending search data from Google Trends."""

import logging
import time
from typing import List, Optional, Union

import pandas as pd
import requests

from gtrends_core.config import DEFAULT_REGION
from gtrends_core.exceptions.trends_exceptions import ApiRequestException, NoDataException
from gtrends_core.models.base import NewsArticle, TrendingTopic
from gtrends_core.models.trending import TrendingSearchResults
from gtrends_core.utils.helpers import format_region_name

logger = logging.getLogger(__name__)


class TrendingService:
    """Service for fetching trending search data from Google Trends."""

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

    def _convert_trending_results(
        self, trends_data: Union[List, pd.DataFrame]
    ) -> List[TrendingTopic]:
        """Convert trending data from API to TrendingTopic objects.

        Args:
            trends_data:Data from the API, either a list of TrendKeyword-like objects or a DataFrame

        Returns:
            List of TrendingTopic objects
        """
        topics = []

        # If it's a DataFrame, convert it to our model
        if isinstance(trends_data, pd.DataFrame):
            for i, row in trends_data.iterrows():
                # Create a new TrendingTopic with the available data
                topic = TrendingTopic(
                    keyword=row["title"],
                    rank=row.get("rank", i + 1),
                    volume=(
                        row.get("volume")
                        if "volume" in row
                        else (
                            int(row["traffic"].replace("+", "").replace(",", ""))
                            if isinstance(row.get("traffic"), str)
                            and row.get("traffic")
                            and any(c.isdigit() for c in row.get("traffic", ""))
                            else None
                        )
                    ),
                    volume_growth_pct=row.get("volume_growth_pct"),
                    geo=row.get("geo"),
                    trend_keywords=row.get("trend_keywords", []),
                    topics=row.get("topics", []),
                    news_tokens=row.get("news_tokens", []),
                )
                topics.append(topic)

        # If it's a list of objects, check if they look like TrendKeyword instances
        elif isinstance(trends_data, list) and trends_data:
            for i, item in enumerate(trends_data):
                # Check if the item is already a TrendingTopic
                if isinstance(item, TrendingTopic):
                    topics.append(item)
                    continue

                # Check if it looks like a TrendKeyword or TrendKeywordLite
                if hasattr(item, "keyword"):
                    # Create a TrendingTopic from the attributes of the TrendKeyword object
                    news_articles = []
                    if hasattr(item, "news") and item.news:
                        for article in item.news:
                            if hasattr(article, "to_dict"):
                                article_dict = article.to_dict()
                            else:
                                # Create a dictionary from article attributes
                                article_dict = {
                                    "title": getattr(article, "title", ""),
                                    "source": getattr(article, "source", ""),
                                    "url": getattr(article, "url", ""),
                                    "time": getattr(article, "time", None),
                                    "picture": getattr(article, "picture", None),
                                    "snippet": getattr(article, "snippet", None),
                                }
                            news_articles.append(NewsArticle.from_api(article_dict))

                    # Create the TrendingTopic with appropriate attribute mapping
                    topic = TrendingTopic(
                        keyword=item.keyword,
                        rank=i + 1,  # Assign rank based on position
                        volume=getattr(item, "volume", None),
                        volume_growth_pct=getattr(item, "volume_growth_pct", None),
                        geo=getattr(item, "geo", None),
                        started_timestamp=getattr(item, "started_timestamp", None),
                        ended_timestamp=getattr(item, "ended_timestamp", None),
                        trend_keywords=getattr(item, "trend_keywords", []),
                        topics=getattr(item, "topics", []),
                        news_tokens=getattr(item, "news_tokens", []),
                        normalized_keyword=getattr(item, "normalized_keyword", None),
                        news=news_articles,
                    )
                    topics.append(topic)

        return topics

    def get_trending_searches(
        self, region: Optional[str] = None, limit: int = 20
    ) -> TrendingSearchResults:
        """Get real-time trending searches.

        Args:
            region: Two-letter country code (or None to auto-detect)
            limit: Maximum number of results to return

        Returns:
            TrendingSearchResults object with trending search data

        Raises:
            ApiRequestException: If API request fails
            NoDataException: If no data is available
        """
        try:
            if region is None:
                region = self.get_current_region()

            # Try to get trending searches using the newer format first
            try:
                # This will attempt to use the trending_now method which return TrendKeyword objects
                trending_data = self.client.trends.trending_now(geo=region)
                topics = self._convert_trending_results(trending_data[:limit])
            except (AttributeError, Exception) as e:
                # Fall back to the older format if the newer one fails
                logger.debug(f"Falling back to legacy trending method: {str(e)}")
                print(f"Falling back to legacy trending method: {str(e)}")
                trending_df = self.client.get_trending_searches(region=region)
                topics = self._convert_trending_results(trending_df.head(limit))

            if not topics:
                raise NoDataException(f"No trending data available for region {region}")

            region_name = format_region_name(region)
            return TrendingSearchResults(
                topics=topics,
                region_code=region,
                region_name=region_name,
            )

        except NoDataException:
            raise
        except Exception as e:
            logger.error(f"Error fetching trending searches: {str(e)}")
            raise ApiRequestException(f"Failed to fetch trending searches: {str(e)}")

    def get_trending_searches_with_articles(
        self, region: Optional[str] = None, limit: int = 20
    ) -> TrendingSearchResults:
        """Get trending searches with associated news articles.

        Args:
            region: Two-letter country code (or None to auto-detect)
            limit: Maximum number of results to return

        Returns:
            TrendingSearchResults object with trending search data and news articles

        Raises:
            ApiRequestException: If API request fails
            NoDataException: If no data is available
        """
        try:
            if region is None:
                region = self.get_current_region()

            # Try to get trending searches with news using the newer format first
            try:
                # This will use trending_now_by_rss which includes news articles
                trending_data = self.client.trends.trending_now_by_rss(geo=region)
                topics = self._convert_trending_results(trending_data[:limit])
            except (AttributeError, Exception) as e:
                # Fall back to the older format if the newer one fails
                logger.debug(f"Falling back to legacy trending with articles method: {str(e)}")
                trending_df, news_articles_dict = self.client.get_trending_searches_with_articles(
                    region=region, limit=limit
                )
                topics = self._convert_trending_results(trending_df.head(limit))

                # For backward compatibility, add news articles to results
                news_articles = {}
                for keyword, articles in news_articles_dict.items():
                    news_article_models = []
                    for article_dict in articles:
                        news_article_models.append(
                            NewsArticle(
                                title=article_dict["title"],
                                source=article_dict["source"],
                                url=article_dict["url"],
                                time=article_dict.get("time"),
                                picture=article_dict.get("picture"),
                                snippet=article_dict.get("snippet"),
                            )
                        )
                    news_articles[keyword] = news_article_models

                # Check if any topics need news articles from the dictionary
                for topic in topics:
                    if topic.keyword in news_articles and not topic.news:
                        # Create a new topic with the news articles (since TrendingTopic is frozen)
                        new_topic = TrendingTopic(
                            keyword=topic.keyword,
                            rank=topic.rank,
                            volume=topic.volume,
                            volume_growth_pct=topic.volume_growth_pct,
                            geo=topic.geo,
                            started_timestamp=topic.started_timestamp,
                            ended_timestamp=topic.ended_timestamp,
                            trend_keywords=topic.trend_keywords,
                            topics=topic.topics,
                            news_tokens=topic.news_tokens,
                            normalized_keyword=topic.normalized_keyword,
                            news=news_articles[topic.keyword],
                        )
                        # Replace the topic in the list
                        idx = topics.index(topic)
                        topics[idx] = new_topic

            if not topics:
                raise NoDataException(f"No trending data available for region {region}")

            region_name = format_region_name(region)

            # Prepare news_articles dictionary for backward compatibility
            news_articles = {}
            for topic in topics:
                if hasattr(topic, "news") and topic.news:
                    news_articles[topic.keyword] = topic.news

            return TrendingSearchResults(
                topics=topics,
                region_code=region,
                region_name=region_name,
                news_articles=news_articles,
            )

        except NoDataException:
            raise
        except Exception as e:
            logger.error(f"Error fetching trending searches with articles: {str(e)}")
            raise ApiRequestException(f"Failed to fetch trending searches with articles: {str(e)}")
