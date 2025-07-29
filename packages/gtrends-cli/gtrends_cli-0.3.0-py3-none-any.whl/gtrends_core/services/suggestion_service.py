"""Service for retrieving topic suggestions based on Google Trends data."""

import logging
import time
from typing import List, Optional

import pandas as pd
import requests

from gtrends_core.config import DEFAULT_REGION
from gtrends_core.utils.validators import validate_category, validate_region_code

logger = logging.getLogger(__name__)


class SuggestionService:
    """Service for generating content suggestions based on Google Trends data."""

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

    def get_topic_suggestions(
        self,
        category: str = "0",
        region: Optional[str] = None,
        timeframe: str = "today 7-d",
        count: int = 10,
        keyword: Optional[str] = None,
    ) -> pd.DataFrame:
        """Get topic suggestions for content creators.

        Args:
            category: Category ID (0 for all categories, or a numeric ID)
            region: Two-letter country code (or None to auto-detect)
            timeframe: Time range for data
            count: Number of results to return
            keyword: Optional specific keyword to get suggestions for

        Returns:
            DataFrame with topic suggestions and relevance scores

        Raises:
            InvalidParameterException: If any parameters are invalid
        """
        # Validate parameters
        if region:
            region = validate_region_code(region)
        else:
            region = self.get_current_region()

        category = validate_category(category)

        # First, try to get trending searches
        try:
            trending_df = self.client.get_trending_searches(region=region)

            # If the dataframe is empty or does not have required columns, create a base one
            if trending_df.empty or "title" not in trending_df.columns:
                trending_df = pd.DataFrame(columns=["title"])
        except Exception as e:
            logger.warning(f"Error getting trending searches: {e}")
            trending_df = pd.DataFrame(columns=["title"])

        # If keyword is provided, use it as the only seed keyword
        if keyword:
            seed_keywords = [keyword]
        else:
            # Otherwise, get category-specific seed keywords
            seed_keywords = self._get_seed_keywords(category)

        # Get related topics for each seed keyword
        topic_data = []

        for keyword in seed_keywords:
            try:
                related_topics = self.client.get_related_topics(
                    query=keyword, region=region, timeframe=timeframe, category=category
                )

                # Process rising topics
                if "rising" in related_topics and not related_topics["rising"].empty:
                    rising_df = related_topics["rising"]

                    if "topic_title" in rising_df.columns:
                        for _, row in rising_df.iterrows():
                            title = row["topic_title"]
                            value = row["value"]

                            # Skip if this topic is already in our list
                            if any(t["topic"] == title for t in topic_data):
                                continue

                            topic_data.append(
                                {
                                    "topic": title,
                                    "relevance_score": value,
                                    "source": f"Related to '{keyword}'",
                                    "category": category,
                                    "rising": True,
                                }
                            )

                # Process top topics
                if "top" in related_topics and not related_topics["top"].empty:
                    top_df = related_topics["top"]

                    if "topic_title" in top_df.columns:
                        for _, row in top_df.iterrows():
                            title = row["topic_title"]
                            value = row["value"]

                            # Skip if this topic is already in our list
                            if any(t["topic"] == title for t in topic_data):
                                continue

                            topic_data.append(
                                {
                                    "topic": title,
                                    "relevance_score": value,
                                    "source": f"Related to '{keyword}'",
                                    "category": category,
                                    "rising": False,
                                }
                            )
            except Exception as e:
                logger.warning(f"Error getting related topics for {keyword}: {e}")

        # Add trending searches that might be relevant
        if not trending_df.empty and "title" in trending_df.columns:
            for _, row in trending_df.iterrows():
                title = row["title"]

                # Skip if this topic is already in our list
                if any(t["topic"] == title for t in topic_data):
                    continue

                # Check relevance to category
                relevance = self._check_topic_relevance(title, category)

                if relevance > 30:  # Only include if somewhat relevant
                    topic_data.append(
                        {
                            "topic": title,
                            "relevance_score": relevance,
                            "source": "Trending searches",
                            "category": category,
                            "rising": True,
                        }
                    )

        # Create DataFrame and sort by relevance
        if topic_data:
            suggestions_df = pd.DataFrame(topic_data)
            suggestions_df = suggestions_df.sort_values(
                by=["rising", "relevance_score"], ascending=[False, False]
            ).reset_index(drop=True)

            return suggestions_df.head(count)

        # Return empty DataFrame if no results
        return pd.DataFrame(columns=["topic", "relevance_score", "source", "category", "rising"])

    def _get_seed_keywords(self, category: str) -> List[str]:
        """Get category-specific seed keywords for content suggestion.

        Args:
            category: Content category

        Returns:
            List of seed keywords
        """
        seed_map = {
            "books": ["books", "reading", "literature", "novel", "author"],
            "news": ["news", "current events", "headlines", "journalism"],
            "arts": ["art", "gallery", "exhibition", "artist", "creativity"],
            "fiction": ["fiction", "novel", "story", "fantasy", "science fiction"],
            "culture": ["culture", "tradition", "heritage", "identity", "customs"],
        }

        return seed_map.get(category.lower(), ["trending", "popular"])

    def _check_topic_relevance(self, topic: str, category: str) -> float:
        """Check the relevance of a topic to a specific category.

        Args:
            topic: Topic to check
            category: Category to check against

        Returns:
            Relevance score (0-100)
        """
        # Simple keyword matching for relevance
        category_keywords = {
            "books": [
                "book",
                "read",
                "author",
                "novel",
                "literature",
                "story",
                "publish",
                "fiction",
                "nonfiction",
                "writer",
                "chapter",
                "page",
                "library",
            ],
            "news": [
                "news",
                "report",
                "journalist",
                "headline",
                "article",
                "media",
                "press",
                "coverage",
                "event",
                "announcement",
                "breaking",
            ],
            "arts": [
                "art",
                "artist",
                "creative",
                "gallery",
                "exhibition",
                "museum",
                "painting",
                "sculpture",
                "design",
                "drawing",
                "photograph",
            ],
            "fiction": [
                "fiction",
                "novel",
                "fantasy",
                "scifi",
                "story",
                "plot",
                "character",
                "series",
                "chapter",
                "book",
                "author",
                "genre",
                "literature",
            ],
            "culture": [
                "culture",
                "tradition",
                "heritage",
                "identity",
                "history",
                "society",
                "community",
                "social",
                "custom",
                "practice",
                "belief",
                "ritual",
            ],
        }

        # Get keywords for this category
        keywords = category_keywords.get(category.lower(), [])
        if not keywords:
            return 0

        # Check how many keywords match
        topic_lower = topic.lower()
        matches = sum(1 for kw in keywords if kw in topic_lower)

        # Calculate relevance score
        if matches > 0:
            return min(100, matches * 25)  # Scale up to 100

        return 0

    def _get_category_id(self, category: str) -> str:
        """Get the category ID for a given category name.

        Args:
            category: Category name

        Returns:
            Category ID as string
        """
        # This function assumes you have a mapping in config
        # This should be imported from the appropriate config module
        content_categories = {
            "books": "22",
            "news": "16",
            "arts": "5",
            "fiction": "22",
            "culture": "3",
        }
        return content_categories.get(category.lower(), "0")
