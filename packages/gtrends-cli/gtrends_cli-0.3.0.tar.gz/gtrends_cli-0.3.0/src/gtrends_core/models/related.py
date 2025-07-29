"""Models for related queries and topics data from Google Trends."""

from dataclasses import dataclass
from typing import Dict, List

from gtrends_core.models.base import BaseModel, RelatedTopic


@dataclass(frozen=True)
class RelatedTopicResults(BaseModel):
    """Container for related topics results."""

    query: str
    region_code: str
    region_name: str
    timeframe: str
    category: str
    top_topics: List[RelatedTopic]
    rising_topics: List[RelatedTopic]


@dataclass(frozen=True)
class RelatedQueryResults(BaseModel):
    """Container for related queries results."""

    query: str
    region_code: str
    region_name: str
    timeframe: str
    category: str
    top_queries: List[RelatedTopic]
    rising_queries: List[RelatedTopic]


@dataclass(frozen=True)
class RelatedData(BaseModel):
    """Container for combined related topics and queries data."""

    query: str
    region_code: str
    region_name: str
    timeframe: str
    category: str
    topics: Dict[str, List[RelatedTopic]]
    queries: Dict[str, List[RelatedTopic]]
