"""API router for topic comparison."""

import logging
from typing import List, Optional

from fastapi import APIRouter, Depends, Query

from gtrends_api.dependencies.core import get_comparison_service
from gtrends_api.schemas.requests import ComparisonRequest
from gtrends_api.schemas.responses import InterestOverTimeResponse, TimePointResponse
from gtrends_core.services.comparison_service import ComparisonService
from gtrends_core.utils.validators import parse_timeframe, validate_region_code

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/comparison", tags=["comparison"])


@router.get(
    "/",
    response_model=InterestOverTimeResponse,
    summary="Compare interest over time between topics",
)
async def get_comparison(
    topics: List[str] = Query(..., description="List of topics to compare (up to 5)"),
    region: Optional[str] = Query(
        None, description="Region code (e.g., US, GB). Auto-detects if not specified."
    ),
    timeframe: str = Query(
        "today 3-m", description="Timeframe for data (e.g., 'today 3-m', 'today 12-m')"
    ),
    category: str = Query("0", description="Category ID to filter results"),
    service: ComparisonService = Depends(get_comparison_service),
) -> InterestOverTimeResponse:
    """Compare interest over time between multiple topics.

    This endpoint provides time series data to compare interest in multiple search terms over time.

    - **topics**: List of topics to compare (max 5)
    - **region**: Two-letter country code (e.g., US, GB, AE)
    - **timeframe**: Time range for data (e.g., 'today 3-m', 'today 12-m')
    - **category**: Category ID to filter results

    Returns time series data for each topic to enable comparison.
    """
    # Validate parameters
    if len(topics) > 5:
        topics = topics[:5]

    region_code = validate_region_code(region) if region else None
    timeframe_parsed = parse_timeframe(timeframe)

    # Get comparison data
    comparison_result = service.get_interest_over_time(
        queries=topics,
        region=region_code,
        timeframe=timeframe_parsed,
        category=category,
    )

    # Convert to API response model
    time_series = {}

    for topic in comparison_result.topics:
        if topic in comparison_result.time_series:
            points = comparison_result.time_series[topic]
            if points:
                time_points = []
                for point in points:
                    time_point = TimePointResponse(
                        date=point.date,
                        value=point.value,
                    )
                    time_points.append(time_point)
                time_series[topic] = time_points

    return InterestOverTimeResponse(
        topics=topics,
        region_code=comparison_result.region_code,
        region_name=comparison_result.region_name,
        timeframe=timeframe_parsed,
        category=category,
        time_series=time_series,
    )


@router.post(
    "/",
    response_model=InterestOverTimeResponse,
    summary="Compare interest over time between topics",
)
async def post_comparison(
    request: ComparisonRequest,
    service: ComparisonService = Depends(get_comparison_service),
) -> InterestOverTimeResponse:
    """Compare interest over time between multiple topics.

    This endpoint provides time series data to compare interest in multiple search terms over time.

    Request body:
    - **topics**: List of topics to compare (max 5)
    - **region**: Two-letter country code (e.g., US, GB, AE)
    - **timeframe**: Time range for data (e.g., 'today 3-m', 'today 12-m')
    - **category**: Category ID to filter results

    Returns time series data for each topic to enable comparison.
    """
    # Validate parameters
    topics = request.topics
    if len(topics) > 5:
        topics = topics[:5]

    region_code = validate_region_code(request.region) if request.region else None
    timeframe_parsed = parse_timeframe(request.timeframe)

    # Get comparison data
    comparison_result = service.get_interest_over_time(
        queries=topics,
        region=region_code,
        timeframe=timeframe_parsed,
        category=request.category,
    )

    # Convert to API response model
    time_series = {}

    for topic in comparison_result.topics:
        if topic in comparison_result.time_series:
            points = comparison_result.time_series[topic]
            if points:
                time_points = []
                for point in points:
                    time_point = TimePointResponse(
                        date=point.date,
                        value=point.value,
                    )
                    time_points.append(time_point)
                time_series[topic] = time_points

    return InterestOverTimeResponse(
        topics=topics,
        region_code=comparison_result.region_code,
        region_name=comparison_result.region_name,
        timeframe=timeframe_parsed,
        category=request.category,
        time_series=time_series,
    )
