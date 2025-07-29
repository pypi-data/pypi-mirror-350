"""Service for identifying writing opportunities based on Google Trends data."""

import logging
import time
from typing import List, Optional

import pandas as pd
import requests

from gtrends_core.config import DEFAULT_REGION
from gtrends_core.utils.validators import validate_region_code

logger = logging.getLogger(__name__)


class OpportunityService:
    """Service for identifying content creation opportunities based on Google Trends data."""

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

    def get_writing_opportunities(
        self,
        seed_topics: List[str] = None,
        region: Optional[str] = None,
        timeframe: str = "today 1-m",
        count: int = 5,
    ) -> pd.DataFrame:
        """Find writing opportunities based on trending topics and given seed topics.

        Args:
            seed_topics: Optional list of seed topics to base suggestions on
            region: Two-letter country code (or None to auto-detect)
            timeframe: Time range for data
            count: Number of opportunities to find

        Returns:
            DataFrame with writing opportunities

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

        # Use default seed topics if none provided
        if not seed_topics or len(seed_topics) == 0:
            seed_topics = self._get_default_seeds()

        # First, try to get trending searches
        try:
            trending_df = self.client.get_trending_searches(region=region)
            if trending_df.empty or "title" not in trending_df.columns:
                trending_df = pd.DataFrame(columns=["title"])
        except Exception as e:
            logger.warning(f"Error getting trending searches: {e}")
            trending_df = pd.DataFrame(columns=["title"])

        # Second, get related topics for each seed
        related_data = []

        for seed in seed_topics:
            try:
                related_topics = self.client.get_related_topics(
                    query=seed, region=region, timeframe=timeframe
                )

                # Process rising topics (have growth potential)
                if "rising" in related_topics and not related_topics["rising"].empty:
                    rising_df = related_topics["rising"]

                    if "topic_title" in rising_df.columns:
                        for _, row in rising_df.iterrows():
                            title = row["topic_title"]
                            value = row["value"]

                            # Only add if not already in our list
                            if not any(r["topic"] == title for r in related_data):
                                related_data.append(
                                    {
                                        "topic": title,
                                        "growth_score": value,
                                        "opportunity_score": self._calculate_opportunity_score(
                                            title, trending_df, value
                                        ),
                                        "related_to": seed,
                                    }
                                )
            except Exception as e:
                logger.warning(f"Error getting related topics for {seed}: {e}")

        # Find opportunities in trending searches if we don't have enough
        if len(related_data) < count and not trending_df.empty and "title" in trending_df.columns:
            for _, row in trending_df.iterrows():
                title = row["title"]

                # Skip if already in our list
                if any(r["topic"] == title for r in related_data):
                    continue

                # Find most related seed topic
                best_seed = self._find_best_seed_match(title, seed_topics)

                # Calculate a synthetic opportunity score
                opportunity_score = 75  # Trending items start with a high base score

                related_data.append(
                    {
                        "topic": title,
                        "growth_score": 100,  # It's trending, so maximum growth score
                        "opportunity_score": opportunity_score,
                        "related_to": best_seed,
                    }
                )

                # Stop if we have enough
                if len(related_data) >= count:
                    break

        # Generate article ideas for each opportunity
        opportunity_data = []

        for item in related_data:
            topic = item["topic"]
            related_to = item["related_to"]

            # Generate a writing suggestion
            suggestion = self._generate_writing_suggestion(topic, related_to)

            opportunity_data.append(
                {
                    "topic": topic,
                    "opportunity_score": item["opportunity_score"],
                    "growth_score": item["growth_score"],
                    "article_idea": suggestion,
                    "related_to": related_to,
                }
            )

        # Create DataFrame and sort by opportunity score
        if opportunity_data:
            opportunities_df = pd.DataFrame(opportunity_data)
            opportunities_df = opportunities_df.sort_values(
                by="opportunity_score", ascending=False
            ).reset_index(drop=True)

            return opportunities_df.head(count)

        # Return empty DataFrame if no results
        return pd.DataFrame(
            columns=["topic", "opportunity_score", "growth_score", "article_idea", "related_to"]
        )

    def _get_default_seeds(self) -> List[str]:
        """Get default seed topics when none are provided.

        Returns:
            List of default seed topics
        """
        return ["technology", "business", "health", "education", "entertainment"]

    def _calculate_opportunity_score(
        self, topic: str, trending_df: pd.DataFrame, growth_value: float
    ) -> float:
        """Calculate an opportunity score for a topic.

        The score is based on growth and whether it appears in trending searches.

        Args:
            topic: The topic to score
            trending_df: DataFrame of trending searches
            growth_value: The growth value from related topics

        Returns:
            Opportunity score from 0-100
        """
        # Base score from growth value, normalized to 0-60 range
        try:
            growth_value_float = float(growth_value)
            base_score = min(60, (growth_value_float / 100) * 60)
        except (ValueError, TypeError):
            # Handle "Breakout" or other non-numeric values
            base_score = 60  # Assume maximum base score for "Breakout"

        # Check if topic is in trending searches (exact or partial match)
        trending_bonus = 0
        if not trending_df.empty and "title" in trending_df.columns:
            trending_topics = trending_df["title"].str.lower().tolist()
            topic_lower = topic.lower()

            # Check for exact match
            if topic_lower in trending_topics:
                trending_bonus = 40  # Maximum bonus
            else:
                # Check for partial matches
                for trending_topic in trending_topics:
                    if topic_lower in trending_topic or trending_topic in topic_lower:
                        trending_bonus = 20  # Partial match bonus
                        break

        # Combine scores, cap at 100
        return min(100, base_score + trending_bonus)

    def _find_best_seed_match(self, topic: str, seed_topics: List[str]) -> str:
        """Find the seed topic that best matches the given topic.

        Args:
            topic: Topic to match
            seed_topics: List of seed topics

        Returns:
            Best matching seed topic
        """
        if not seed_topics:
            return "general"

        # Simple word matching for now
        topic_lower = topic.lower()

        for seed in seed_topics:
            seed_lower = seed.lower()
            if seed_lower in topic_lower:
                return seed

        # If no match, return the first seed
        return seed_topics[0]

    def _generate_writing_suggestion(self, topic: str, seed: str) -> str:
        """Generate a writing suggestion based on the topic and seed.

        Args:
            topic: The topic to create a suggestion for
            seed: The related seed topic

        Returns:
            Writing suggestion string
        """
        # Generate standard title formulas based on topic type
        if seed.lower() in ["technology", "tech"]:
            return f"How {topic} Is Changing the Future of {seed}"
        elif seed.lower() in ["business", "finance", "money"]:
            return f"The Business Impact of {topic}: What You Need to Know"
        elif seed.lower() in ["health", "fitness", "wellness"]:
            return f"{topic}: The Health Benefits You Didn't Know About"
        elif seed.lower() in ["education", "learning", "teaching"]:
            return f"Learning About {topic}: A Beginner's Guide"
        else:
            return f"The Ultimate Guide to {topic}: Everything You Need to Know"
