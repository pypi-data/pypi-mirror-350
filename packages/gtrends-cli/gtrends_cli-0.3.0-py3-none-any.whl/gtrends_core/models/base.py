"""Base models for Google Trends data structures.

This module provides base classes that can be inherited by specific data models.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class BaseModel:
    """Base class for all data models in the application.

    Provides common functionality like string representation and dictionary conversion.
    """

    def __str__(self) -> str:
        """Return a string representation of the model."""
        attrs = [f"{key}={value}" for key, value in self.__dict__.items()]
        return f"{self.__class__.__name__}({', '.join(attrs)})"

    def __repr__(self) -> str:
        """Return a string representation of the model."""
        return self.__str__()

    def to_dict(self) -> Dict[str, Any]:
        """Convert the model to a dictionary."""
        return {key: value for key, value in self.__dict__.items()}


@dataclass(frozen=True)
class NewsArticle(BaseModel):
    """Model for a news article associated with a trending topic."""

    title: str
    source: str
    url: str
    time: Optional[datetime] = None
    picture: Optional[str] = None
    snippet: Optional[str] = None

    @classmethod
    def from_api(cls, data: Dict[str, Any]) -> "NewsArticle":
        """Create a NewsArticle instance from API response data."""
        return cls(
            title=data.get("title", ""),
            source=data.get("source", ""),
            url=data.get("url", ""),
            time=(
                datetime.fromtimestamp(data.get("time", 0), tz=timezone.utc)
                if "time" in data
                else None
            ),
            picture=data.get("picture", None),
            snippet=data.get("snippet", None),
        )


@dataclass(frozen=True)
class TrendingTopic(BaseModel):
    """Model for a trending search topic."""

    keyword: str
    rank: Optional[int] = None
    volume: Optional[int] = None
    volume_growth_pct: Optional[float] = None
    geo: Optional[str] = None
    started_timestamp: Optional[tuple] = None
    ended_timestamp: Optional[tuple] = None
    trend_keywords: List[str] = field(default_factory=list)
    topics: List[int] = field(default_factory=list)
    news_tokens: List[str] = field(default_factory=list)
    normalized_keyword: Optional[str] = None
    news: List[NewsArticle] = field(default_factory=list)

    @property
    def is_trend_finished(self) -> bool:
        """Checks if the trend is finished."""
        return self.ended_timestamp is not None

    def hours_since_started(self) -> float:
        """Returns the number of hours elapsed since the trend started."""
        if not self.started_timestamp:
            return 0
        delta = datetime.now(tz=timezone.utc) - datetime.fromtimestamp(
            self.started_timestamp[0], tz=timezone.utc
        )
        return delta.total_seconds() / 3600

    def brief_summary(self) -> str:
        """Returns an informative summary of the trend."""
        parts = [f"[{self.geo or 'GLOBAL'}] {self.keyword}"]

        if self.volume is not None:
            parts[0] += f": {self.volume:,} searches"

        additional_info = []
        if self.trend_keywords:
            additional_info.append(f"{len(self.trend_keywords)} related keywords")
        if self.topics:
            additional_info.append(f"{len(self.topics)} topics")
        if self.news:
            additional_info.append(f"{len(self.news)} news articles")

        if additional_info:
            parts.append(", ".join(additional_info))

        return ", ".join(parts)


@dataclass(frozen=True)
class RelatedTopic(BaseModel):
    """Model for a topic related to a search query."""

    title: str
    type: str
    value: float  # Top value or rising value
    is_rising: bool = False
    rising_value_text: Optional[str] = None  # For "Breakout" etc.


@dataclass(frozen=True)
class TimePoint(BaseModel):
    """Model for a point in time series data."""

    date: datetime
    value: float


@dataclass(frozen=True)
class RegionInterest(BaseModel):
    """Model for interest data by geographic region."""

    region_code: str
    region_name: str
    value: float


@dataclass(frozen=True)
class ComparisonResult(BaseModel):
    """Model for comparison results between multiple topics."""

    topics: List[str]
    time_series: Dict[str, List[TimePoint]] = field(default_factory=dict)
