"""Request schemas for the API."""

from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class ResolutionEnum(str, Enum):
    """Geographic resolution options."""

    COUNTRY = "COUNTRY"
    REGION = "REGION"
    CITY = "CITY"
    DMA = "DMA"


class BatchPeriodEnum(str, Enum):
    """Batch period options for trend analysis."""

    PAST_4H = "custom_4h"
    PAST_24H = "custom_1d"
    PAST_48H = "custom_2d"
    PAST_7D = "custom_7d"


class CategoryEnum(str, Enum):
    """Content category options."""

    ALL = "0"
    BOOKS = "22"
    NEWS = "16"
    ARTS = "5"
    PERFORMING_ARTS = "3"


class TrendingRequest(BaseModel):
    """Request model for trending searches endpoint."""

    region: Optional[str] = Field(
        None,
        description="Two-letter country code (e.g., US, GB, AE). Auto-detects if not specified.",
    )
    limit: int = Field(10, description="Maximum number of results to return", ge=1, le=100)
    include_news: bool = Field(False, description="Whether to include related news articles")


class RelatedRequest(BaseModel):
    """Request model for related topics and queries endpoints."""

    query: str = Field(..., description="Search term to find related topics/queries")
    region: Optional[str] = Field(
        None,
        description="Two-letter country code (e.g., US, GB, AE). Auto-detects if not specified.",
    )
    timeframe: str = Field(
        "today 1-d", description="Time range for data (e.g., 'today 1-d', 'today 3-m')"
    )
    category: str = Field("0", description="Category ID to filter results")
    limit: int = Field(10, description="Maximum number of results to return", ge=1, le=50)


class ComparisonRequest(BaseModel):
    """Request model for comparison endpoints."""

    topics: List[str] = Field(
        ..., description="List of topics to compare", min_length=1, max_length=5
    )
    region: Optional[str] = Field(
        None,
        description="Two-letter country code (e.g., US, GB, AE). Auto-detects if not specified.",
    )
    timeframe: str = Field(
        "today 3-m", description="Time range for data (e.g., 'today 3-m', 'today 12-m')"
    )
    category: str = Field("0", description="Category ID to filter results")


class InterestByRegionRequest(BaseModel):
    """Request model for interest by region endpoint."""

    topics: List[str] = Field(
        ..., description="List of topics to analyze", min_length=1, max_length=5
    )
    region: Optional[str] = Field(
        None,
        description="Two-letter country code (e.g., US, GB, AE). Auto-detects if not specified.",
    )
    timeframe: str = Field("today 12-m", description="Time range for data (e.g., 'today 12-m')")
    category: str = Field("0", description="Category ID to filter results")
    resolution: ResolutionEnum = Field(
        ResolutionEnum.COUNTRY, description="Geographic resolution level"
    )
    limit: int = Field(
        20, description="Maximum number of regions to return per topic", ge=1, le=100
    )


class TopicGrowthRequest(BaseModel):
    """Request model for topic growth endpoint."""

    topics: List[str] = Field(
        ..., description="List of topics to analyze growth for", min_length=1, max_length=50
    )
    period: BatchPeriodEnum = Field(BatchPeriodEnum.PAST_24H, description="Time period to analyze")


class GrowthRequest(BaseModel):
    """Request model for topic growth endpoint."""

    topics: List[str] = Field(
        ..., description="List of topics to analyze growth", min_length=1, max_length=10
    )
    period: str = Field("24h", description="Time period to analyze (4h, 24h, 48h, 7d)")


class SuggestionRequest(BaseModel):
    """Request model for topic suggestions endpoint."""

    category: str = Field(
        "books", description="Content category (books, news, arts, fiction, culture)"
    )
    region: Optional[str] = Field(
        None,
        description="Two-letter country code (e.g., US, GB, AE). Auto-detects if not specified.",
    )
    timeframe: str = Field(
        "today 7-d", description="Time range for data (e.g., 'today 7-d', 'today 1-m')"
    )
    count: int = Field(10, description="Number of suggestions to return", ge=1, le=50)


class GeoInterestRequest(BaseModel):
    """Request model for geographical interest endpoint."""

    query: str = Field(..., description="Search term to analyze geographic interest")
    region: Optional[str] = Field(
        None,
        description="Two-letter country code (e.g., US, GB, AE). Auto-detects if not specified.",
    )
    resolution: ResolutionEnum = Field(
        ResolutionEnum.COUNTRY, description="Geographic resolution level"
    )
    timeframe: str = Field("today 12-m", description="Time range for data (e.g., 'today 12-m')")
    category: str = Field("0", description="Category ID to filter results")
    count: int = Field(20, description="Number of regions to display", ge=1, le=100)


class OpportunityRequest(BaseModel):
    """Request model for writing opportunities endpoint."""

    seed_topics: Optional[List[str]] = Field(
        None, description="Optional list of seed topics to base suggestions on"
    )
    region: Optional[str] = Field(
        None,
        description="Two-letter country code (e.g., US, GB, AE). Auto-detects if not specified.",
    )
    timeframe: str = Field(
        "today 1-m", description="Time range for data (e.g., 'today 1-m', 'today 3-m')"
    )
    count: int = Field(5, description="Number of opportunities to find", ge=1, le=20)
