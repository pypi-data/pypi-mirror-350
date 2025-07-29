"""API router for related topics and queries."""

import logging
from typing import Optional

from fastapi import APIRouter, Depends, Query

from gtrends_api.dependencies.core import get_related_service
from gtrends_api.schemas.requests import RelatedRequest
from gtrends_api.schemas.responses import RelatedDataResponse
from gtrends_core.services.related_service import RelatedService
from gtrends_core.utils.validators import parse_timeframe, validate_region_code

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/related", tags=["related"])


@router.get("/", response_model=RelatedDataResponse, summary="Get related topics and queries")
async def get_related_data(
    topic: str = Query(..., description="Search query to find related data for"),
    region: Optional[str] = Query(
        None, description="Region code (e.g., US, GB). Auto-detects if not specified."
    ),
    timeframe: str = Query(
        "today 3-m", description="Timeframe for data (e.g., 'today 3-m', 'today 12-m')"
    ),
    category: str = Query("0", description="Category ID to filter results"),
    service: RelatedService = Depends(get_related_service),
) -> RelatedDataResponse:
    """Get topics and queries related to a search term.

    This endpoint returns both related topics and related queries for a given search term.

    - **topic**: Search query to find related data for
    - **region**: Two-letter country code (e.g., US, GB, AE)
    - **timeframe**: Time range for data (e.g., 'today 3-m', 'today 12-m')
    - **category**: Category ID to filter results (Default: 0 - All categories)

    Returns related topics and queries with their relevance scores.
    """
    # Validate parameters
    region_code = validate_region_code(region) if region else None
    timeframe_parsed = parse_timeframe(timeframe)

    # Get related data
    related_data = service.get_related_data(
        query=topic,
        region=region_code,
        timeframe=timeframe_parsed,
        category=category,
    )

    # Convert to API response model
    response = RelatedDataResponse(
        query=topic,
        region_code=related_data.region_code,
        region_name=related_data.region_name,
        timeframe=timeframe_parsed,
        category=category,
        topics={
            "top": [
                {"title": item.title, "type": item.type, "value": item.value}
                for item in related_data.topics.get("top", [])
            ],
            "rising": [
                {"title": item.title, "type": item.type, "value": item.value}
                for item in related_data.topics.get("rising", [])
            ],
        },
        queries={
            "top": [
                {"title": item.title, "type": item.type, "value": item.value}
                for item in related_data.queries.get("top", [])
            ],
            "rising": [
                {"title": item.title, "type": item.type, "value": item.value}
                for item in related_data.queries.get("rising", [])
            ],
        },
    )

    return response


@router.post("/", response_model=RelatedDataResponse, summary="Get related topics and queries")
async def post_related_data(
    request: RelatedRequest,
    service: RelatedService = Depends(get_related_service),
) -> RelatedDataResponse:
    """Get topics and queries related to a search term.

    This endpoint returns both related topics and related queries for a given search term.

    Request body:
    - **query**: Search query to find related data for
    - **region**: Two-letter country code (e.g., US, GB, AE)
    - **timeframe**: Time range for data (e.g., 'today 3-m', 'today 12-m')
    - **category**: Category ID to filter results

    Returns related topics and queries with their relevance scores.
    """
    # Validate parameters
    region_code = validate_region_code(request.region) if request.region else None
    timeframe_parsed = parse_timeframe(request.timeframe)

    # Get related data
    related_data = service.get_related_data(
        query=request.query,
        region=region_code,
        timeframe=timeframe_parsed,
        category=request.category,
    )

    # Convert to API response model
    response = RelatedDataResponse(
        query=request.query,
        region_code=related_data.region_code,
        region_name=related_data.region_name,
        timeframe=timeframe_parsed,
        category=request.category,
        topics={
            "top": [
                {"title": item.title, "type": item.type, "value": item.value}
                for item in related_data.topics.get("top", [])
            ],
            "rising": [
                {"title": item.title, "type": item.type, "value": item.value}
                for item in related_data.topics.get("rising", [])
            ],
        },
        queries={
            "top": [
                {"title": item.title, "type": item.type, "value": item.value}
                for item in related_data.queries.get("top", [])
            ],
            "rising": [
                {"title": item.title, "type": item.type, "value": item.value}
                for item in related_data.queries.get("rising", [])
            ],
        },
    )

    return response
