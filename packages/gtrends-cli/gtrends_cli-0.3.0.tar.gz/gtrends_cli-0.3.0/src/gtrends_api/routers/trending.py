"""API router for trending searches."""

import logging
from typing import Optional

from fastapi import APIRouter, Depends, Query

from gtrends_api.dependencies.core import get_trending_service
from gtrends_api.schemas.requests import TrendingRequest
from gtrends_api.schemas.responses import (
    NewsArticleResponse,
    TrendingSearchResponse,
    TrendingTopicResponse,
)
from gtrends_core.services.trending_service import TrendingService
from gtrends_core.utils import validate_region_code

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/trending", tags=["trending"])


@router.get("/", response_model=TrendingSearchResponse, summary="Get trending searches")
async def get_trending_searches(
    region: Optional[str] = Query(
        None, description="Region code (e.g., US, GB). Auto-detects if not specified."
    ),
    limit: int = Query(10, ge=1, le=100, description="Maximum number of results to return"),
    include_news: bool = Query(False, description="Whether to include news articles"),
    service: TrendingService = Depends(get_trending_service),
) -> TrendingSearchResponse:
    """Get current trending searches on Google.

    This endpoint returns the most popular trending searches for a given region.
    If no region is specified, it auto-detects based on the client's IP.

    - **region**: Two-letter country code (e.g., US, GB, AE)
    - **limit**: Maximum number of results to return (1-100)
    - **include_news**: Whether to include related news articles

    Returns a list of trending topics and optionally related news articles.
    """
    # Validate region code if provided
    region_code = validate_region_code(region) if region else None

    # Fetch trending data
    if include_news:
        results = service.get_trending_searches_with_articles(region=region_code, limit=limit)
    else:
        results = service.get_trending_searches(region=region_code, limit=limit)

    # Convert to API response model
    topics = []
    for topic in results.topics:
        news_list = None
        if hasattr(topic, "news") and topic.news:
            news_list = [
                NewsArticleResponse(
                    title=article.title,
                    source=article.source,
                    url=article.url,
                    time=article.time,
                    picture=article.picture,
                    snippet=article.snippet,
                )
                for article in topic.news
            ]

        topics.append(
            TrendingTopicResponse(
                keyword=topic.keyword,
                rank=topic.rank,
                volume=topic.volume,
                volume_growth_pct=topic.volume_growth_pct,
                geo=topic.geo,
                trend_keywords=topic.trend_keywords,
                topics=topic.topics,
                news=news_list,
            )
        )

    # Handle news articles for backward compatibility
    news_articles = None
    if results.news_articles:
        news_articles = {
            topic: [
                NewsArticleResponse(
                    title=article.title,
                    source=article.source,
                    url=article.url,
                    time=article.time,
                    picture=article.picture,
                    snippet=article.snippet,
                )
                for article in articles
            ]
            for topic, articles in results.news_articles.items()
        }

    return TrendingSearchResponse(
        region_code=results.region_code,
        region_name=results.region_name,
        topics=topics,
        news_articles=news_articles,
    )


@router.post("/", response_model=TrendingSearchResponse, summary="Get trending searches")
async def post_trending_searches(
    request: TrendingRequest,
    service: TrendingService = Depends(get_trending_service),
) -> TrendingSearchResponse:
    """Get current trending searches on Google.

    This endpoint returns the most popular trending searches for a given region.
    If no region is specified, it auto-detects based on the client's IP.

    Request body:
    - **region**: Two-letter country code (e.g., US, GB, AE)
    - **limit**: Maximum number of results to return (1-100)
    - **include_news**: Whether to include related news articles

    Returns a list of trending topics and optionally related news articles.
    """
    # Validate region code if provided
    region_code = validate_region_code(request.region) if request.region else None

    # Fetch trending data
    if request.include_news:
        results = service.get_trending_searches_with_articles(
            region=region_code, limit=request.limit
        )
    else:
        results = service.get_trending_searches(region=region_code, limit=request.limit)

    # Convert to API response model
    topics = []
    for topic in results.topics:
        news_list = None
        if hasattr(topic, "news") and topic.news:
            news_list = [
                NewsArticleResponse(
                    title=article.title,
                    source=article.source,
                    url=article.url,
                    time=article.time,
                    picture=article.picture,
                    snippet=article.snippet,
                )
                for article in topic.news
            ]

        topics.append(
            TrendingTopicResponse(
                keyword=topic.keyword,
                rank=topic.rank,
                volume=topic.volume,
                volume_growth_pct=topic.volume_growth_pct,
                geo=topic.geo,
                trend_keywords=topic.trend_keywords,
                topics=topic.topics,
                news=news_list,
            )
        )

    # Handle news articles for backward compatibility
    news_articles = None
    if results.news_articles:
        news_articles = {
            topic: [
                NewsArticleResponse(
                    title=article.title,
                    source=article.source,
                    url=article.url,
                    time=article.time,
                    picture=article.picture,
                    snippet=article.snippet,
                )
                for article in articles
            ]
            for topic, articles in results.news_articles.items()
        }

    return TrendingSearchResponse(
        region_code=results.region_code,
        region_name=results.region_name,
        topics=topics,
        news_articles=news_articles,
    )
