"""Response schemas for the API."""

from datetime import datetime
from typing import Dict, List, Optional, Union

from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):
    """Error response model."""

    error_code: str = Field(..., description="Machine-readable error code")
    message: str = Field(..., description="Human-readable error message")
    context: Optional[Dict] = Field(None, description="Additional error context")


class NewsArticleResponse(BaseModel):
    """News article response model."""

    title: str = Field(..., description="Article title")
    source: str = Field(..., description="News source")
    url: str = Field(..., description="Article URL")
    time: Optional[datetime] = Field(None, description="Article time")
    picture: Optional[str] = Field(None, description="Article image URL")
    snippet: Optional[str] = Field(None, description="Article snippet")


class TrendingTopicResponse(BaseModel):
    """Trending topic response model."""

    keyword: str = Field(..., description="Trending topic keyword")
    rank: Optional[int] = Field(None, description="Rank in trending list")
    volume: Optional[int] = Field(None, description="Search volume")
    volume_growth_pct: Optional[float] = Field(
        None, description="Percentage growth in search volume"
    )
    geo: Optional[str] = Field(None, description="Geographic location code")
    trend_keywords: Optional[List[str]] = Field(None, description="Related keywords")
    topics: Optional[List[int]] = Field(None, description="Related topic IDs")
    news: Optional[List[NewsArticleResponse]] = Field(None, description="Related news articles")

    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "keyword": "example topic",
                    "rank": 1,
                    "volume": 5000,
                    "volume_growth_pct": 120.5,
                    "geo": "US",
                }
            ]
        }


class TrendingSearchResponse(BaseModel):
    """Trending search response model."""

    region_code: str = Field(..., description="Region code")
    region_name: str = Field(..., description="Region name")
    topics: List[TrendingTopicResponse] = Field(..., description="List of trending topics")
    news_articles: Optional[Dict[str, List[NewsArticleResponse]]] = Field(
        None, description="News articles by topic"
    )


class RelatedTopicResponse(BaseModel):
    """Related topic response model."""

    title: str = Field(..., description="Topic title")
    value: float = Field(..., description="Topic value (0-100)")
    is_rising: bool = Field(False, description="Whether this is a rising topic")
    rising_value_text: Optional[str] = Field(
        None, description="Rising value text (e.g., 'Breakout')"
    )


class RelatedTopicsResponse(BaseModel):
    """Related topics response model."""

    query: str = Field(..., description="Original query")
    region_code: str = Field(..., description="Region code")
    region_name: str = Field(..., description="Region name")
    timeframe: str = Field(..., description="Timeframe used")
    category: str = Field(..., description="Category used")
    top_topics: List[RelatedTopicResponse] = Field(..., description="Top related topics")
    rising_topics: List[RelatedTopicResponse] = Field(..., description="Rising related topics")


class RelatedQueriesResponse(BaseModel):
    """Related queries response model."""

    query: str = Field(..., description="Original query")
    region_code: str = Field(..., description="Region code")
    region_name: str = Field(..., description="Region name")
    timeframe: str = Field(..., description="Timeframe used")
    category: str = Field(..., description="Category used")
    top_queries: List[RelatedTopicResponse] = Field(..., description="Top related queries")
    rising_queries: List[RelatedTopicResponse] = Field(..., description="Rising related queries")


class RelatedDataItem(BaseModel):
    """Individual related data item."""

    title: str = Field(..., description="Item title")
    type: Optional[str] = Field(None, description="Item type")
    value: float = Field(..., description="Relevance value")


class RelatedDataResponse(BaseModel):
    """Combined response for related topics and queries."""

    query: str = Field(..., description="Original query")
    region_code: str = Field(..., description="Region code")
    region_name: str = Field(..., description="Region name")
    timeframe: str = Field(..., description="Timeframe used")
    category: str = Field(..., description="Category used")
    topics: Dict[str, List[RelatedDataItem]] = Field(
        ..., description="Related topics (top and rising)"
    )
    queries: Dict[str, List[RelatedDataItem]] = Field(
        ..., description="Related queries (top and rising)"
    )


class TimePointResponse(BaseModel):
    """Time point response model."""

    date: datetime = Field(..., description="Date of the data point")
    value: float = Field(..., description="Interest value (0-100)")


class InterestOverTimeResponse(BaseModel):
    """Interest over time response model."""

    topics: List[str] = Field(..., description="List of topics")
    region_code: str = Field(..., description="Region code")
    region_name: str = Field(..., description="Region name")
    timeframe: Union[str, List[str]] = Field(..., description="Timeframe used")
    category: str = Field(..., description="Category used")
    time_series: Dict[str, List[TimePointResponse]] = Field(
        ..., description="Time series data per topic"
    )


class RegionInterestResponse(BaseModel):
    """Region interest response model."""

    region_code: str = Field(..., description="Region code")
    region_name: str = Field(..., description="Region name")
    value: float = Field(..., description="Interest value (0-100)")


class InterestByRegionResponse(BaseModel):
    """Interest by region response model."""

    topics: List[str] = Field(..., description="List of topics")
    region_code: str = Field(..., description="Region code")
    region_name: str = Field(..., description="Region name")
    timeframe: str = Field(..., description="Timeframe used")
    category: str = Field(..., description="Category used")
    resolution: str = Field(..., description="Geographic resolution")
    region_interest: Dict[str, List[RegionInterestResponse]] = Field(
        ..., description="Region interest data per topic"
    )


class TopicSuggestionItem(BaseModel):
    """Topic suggestion item response model."""

    topic: str = Field(..., description="Suggested topic")
    relevance_score: float = Field(..., description="Relevance score")
    is_rising: bool = Field(False, description="Whether the topic is growing in interest")
    source: Optional[str] = Field(None, description="Source of suggestion")
    category: Optional[str] = Field(None, description="Topic category")


class TopicSuggestionsResponse(BaseModel):
    """Topic suggestions response model."""

    category: str = Field(..., description="Category requested")
    region_code: str = Field(..., description="Region code")
    region_name: str = Field(..., description="Region name")
    timeframe: str = Field(..., description="Timeframe used")
    suggestions: List[TopicSuggestionItem] = Field(..., description="Suggested topics list")


class OpportunityItem(BaseModel):
    """Writing opportunity item response model."""

    title: str = Field(..., description="Opportunity topic")
    score: float = Field(..., description="Opportunity score")
    volume: float = Field(..., description="Search volume indicator")
    competition: float = Field(..., description="Content competition level")
    potential: float = Field(..., description="Growth potential indicator")
    description: Optional[str] = Field(None, description="Description of the opportunity")


class OpportunitiesResponse(BaseModel):
    """Writing opportunities response model."""

    seed_topics: Optional[List[str]] = Field(None, description="Seed topics if provided")
    region_code: str = Field(..., description="Region code")
    region_name: str = Field(..., description="Region name")
    timeframe: str = Field(..., description="Timeframe used")
    opportunities: List[OpportunityItem] = Field(..., description="Writing opportunities list")


class GrowthItem(BaseModel):
    """Growth item response model."""

    topic: str = Field(..., description="Topic analyzed")
    trend_direction: str = Field(..., description="Trend direction (up, down, flat)")
    growth_percentage: float = Field(..., description="Growth percentage")
    volume_index: float = Field(..., description="Volume index (0-100)")
    data_points: Optional[List[TimePointResponse]] = Field(
        None, description="Historical data points"
    )


class GrowthResponse(BaseModel):
    """Growth tracking response model."""

    topics: List[str] = Field(..., description="Topics analyzed")
    period: str = Field(..., description="Time period analyzed")
    results: List[GrowthItem] = Field(..., description="Growth analysis results")


class GeoRegionItem(BaseModel):
    """Geo region item response model."""

    name: str = Field(..., description="Region name")
    code: str = Field(..., description="Region code")
    value: float = Field(..., description="Interest value (0-100)")
    interest_level: str = Field(..., description="Interest level category")
    percentile: float = Field(..., description="Interest percentile")


class GeoInterestResponse(BaseModel):
    """Geographical interest response model."""

    query: str = Field(..., description="Search query")
    region_code: Optional[str] = Field(None, description="Region code")
    region_name: Optional[str] = Field(None, description="Region name")
    resolution: str = Field(..., description="Geographic resolution level")
    timeframe: str = Field(..., description="Timeframe used")
    category: str = Field(..., description="Category used")
    regions: List[GeoRegionItem] = Field(..., description="Regions with interest data")


class RegionCodeResponse(BaseModel):
    """Region code lookup response model."""

    search_term: str = Field(..., description="Search term used")
    results: List[Dict[str, str]] = Field(..., description="Matching region codes")
