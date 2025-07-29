"""API router for topic suggestions."""

import logging
from typing import Optional

from fastapi import APIRouter, Depends, Query

from gtrends_api.dependencies.core import get_suggestion_service
from gtrends_api.schemas.requests import SuggestionRequest
from gtrends_api.schemas.responses import TopicSuggestionItem, TopicSuggestionsResponse
from gtrends_core.services.suggestion_service import SuggestionService
from gtrends_core.utils.validators import parse_timeframe, validate_category, validate_region_code

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/suggestions", tags=["suggestions"])


@router.get("/", response_model=TopicSuggestionsResponse, summary="Get topic suggestions")
async def get_topic_suggestions(
    category: str = Query("0", description="Category ID (0 for all categories, or a numeric ID)"),
    keyword: str = Query(None, description="Keyword to get suggestions for"),
    region: Optional[str] = Query(
        None, description="Region code (e.g., US, GB). Auto-detects if not specified."
    ),
    timeframe: str = Query(
        "today 7-d", description="Timeframe for data (e.g., 'today 7-d', 'today 1-m')"
    ),
    limit: int = Query(10, ge=1, le=100, description="Maximum number of suggestions to return"),
    service: SuggestionService = Depends(get_suggestion_service),
) -> TopicSuggestionsResponse:
    """Get topic suggestions for content creators.

    This endpoint suggests topics for content creation \
        based on trending searches and category relevance.

    - **category**: Category ID (0 for all categories, or a numeric ID)
    - **keyword**: Keyword to get suggestions for
    - **region**: Two-letter country code (e.g., US, GB, AE)
    - **timeframe**: Time range for data (e.g., 'today 7-d', 'today 1-m')
    - **limit**: Maximum number of suggestions to return (1-100)

    Returns a list of suggested topics with relevance scores.
    """
    # Validate parameters
    region_code = validate_region_code(region) if region else None
    category_validated = validate_category(category)
    timeframe_parsed = parse_timeframe(timeframe)

    # Get suggestions
    suggestions_df = service.get_topic_suggestions(
        category=category_validated,
        region=region_code,
        timeframe=timeframe_parsed,
        count=limit,
    )

    # Convert to API response model
    suggestions = []

    if not suggestions_df.empty:
        for _, row in suggestions_df.iterrows():
            suggestion = TopicSuggestionItem(
                topic=row["topic"],
                relevance_score=float(row["relevance_score"]),
                is_rising=bool(row["rising"]),
                source=row["source"],
                category=row["category"],
            )
            suggestions.append(suggestion)

    # Get current region if not specified
    if not region_code:
        try:
            region_code = service.client.get_current_region()
        except (AttributeError, Exception):
            region_code = "US"

    from gtrends_core.utils.helpers import format_region_name

    region_name = format_region_name(region_code)

    return TopicSuggestionsResponse(
        category=category_validated,
        region_code=region_code,
        region_name=region_name,
        timeframe=timeframe_parsed,
        suggestions=suggestions,
    )


@router.post("/", response_model=TopicSuggestionsResponse, summary="Get topic suggestions")
async def post_topic_suggestions(
    request: SuggestionRequest,
    service: SuggestionService = Depends(get_suggestion_service),
) -> TopicSuggestionsResponse:
    """Get topic suggestions for content creators.

    This endpoint suggests topics for content creation based on trending \
        searches and category relevance.

    Request body:
    - **category**: Content category (books, news, arts, fiction, culture)
    - **region**: Two-letter country code (e.g., US, GB, AE)
    - **timeframe**: Time range for data (e.g., 'today 7-d', 'today 1-m')
    - **limit**: Maximum number of suggestions to return (1-100)

    Returns a list of suggested topics with relevance scores.
    """
    # Validate parameters
    region_code = validate_region_code(request.region) if request.region else None
    category_validated = validate_category(request.category)
    timeframe_parsed = parse_timeframe(request.timeframe)

    # Get suggestions
    suggestions_df = service.get_topic_suggestions(
        category=category_validated,
        region=region_code,
        timeframe=timeframe_parsed,
        count=request.count,
    )

    # Convert to API response model
    suggestions = []

    if not suggestions_df.empty:
        for _, row in suggestions_df.iterrows():
            suggestion = TopicSuggestionItem(
                topic=row["topic"],
                relevance_score=float(row["relevance_score"]),
                is_rising=bool(row["rising"]),
                source=row["source"],
                category=row["category"],
            )
            suggestions.append(suggestion)

    # Get current region if not specified
    if not region_code:
        try:
            region_code = service.client.get_current_region()
        except (AttributeError, Exception):
            region_code = "US"

    from gtrends_core.utils.helpers import format_region_name

    region_name = format_region_name(region_code)

    return TopicSuggestionsResponse(
        category=category_validated,
        region_code=region_code,
        region_name=region_name,
        timeframe=timeframe_parsed,
        suggestions=suggestions,
    )
