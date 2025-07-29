"""API router for content writing opportunities."""

import logging
from typing import List, Optional

from fastapi import APIRouter, Depends, Query

from gtrends_api.dependencies.core import get_opportunity_service
from gtrends_api.schemas.requests import OpportunityRequest
from gtrends_api.schemas.responses import OpportunitiesResponse, OpportunityItem
from gtrends_core.services.opportunity_service import OpportunityService
from gtrends_core.utils.validators import parse_timeframe, validate_region_code

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/opportunities", tags=["opportunities"])


@router.get("/", response_model=OpportunitiesResponse, summary="Get writing opportunities")
async def get_writing_opportunities(
    region: Optional[str] = Query(
        None, description="Region code (e.g., US, GB). Auto-detects if not specified."
    ),
    timeframe: str = Query(
        "today 1-m", description="Timeframe for data (e.g., 'today 1-m', 'now 7-d')"
    ),
    seed_topics: Optional[List[str]] = Query(
        None, description="Seed topics to base opportunities on (optional)"
    ),
    limit: int = Query(5, ge=1, le=20, description="Maximum number of opportunities to return"),
    service: OpportunityService = Depends(get_opportunity_service),
) -> OpportunitiesResponse:
    """Find content writing opportunities based on trending topics and given seed topics.

    This endpoint identifies potential writing opportunities by finding trending topics and topics
    with growth potential that relate to your seed topics.

    - **region**: Two-letter country code (e.g., US, GB, AE)
    - **timeframe**: Time range for data (e.g., 'today 1-m', 'now 7-d')
    - **seed_topics**: Optional list of seed topics to base opportunities on
    - **limit**: Maximum number of opportunities to return (1-20)

    Returns a list of writing opportunities with suggested article ideas.
    """
    # Validate parameters
    region_code = validate_region_code(region) if region else None
    timeframe_parsed = parse_timeframe(timeframe)

    # Get writing opportunities
    opportunities_df = service.get_writing_opportunities(
        seed_topics=seed_topics,
        region=region_code,
        timeframe=timeframe_parsed,
        count=limit,
    )

    # Convert to API response model
    opportunities = []

    if not opportunities_df.empty:
        for _, row in opportunities_df.iterrows():
            opportunity = OpportunityItem(
                title=row["topic"],
                score=float(row["opportunity_score"]),
                volume=float(row.get("volume", 50)),
                competition=float(row.get("competition", 50)),
                potential=float(row["growth_score"]),
                description=row.get("article_idea", None),
            )
            opportunities.append(opportunity)

    # Get current region if not specified
    if not region_code:
        region_code = service.client.get_current_region()

    from gtrends_core.utils.helpers import format_region_name

    region_name = format_region_name(region_code)

    seed_topics_list = seed_topics if seed_topics else []

    return OpportunitiesResponse(
        region_code=region_code,
        region_name=region_name,
        timeframe=timeframe_parsed,
        seed_topics=seed_topics_list,
        opportunities=opportunities,
    )


@router.post("/", response_model=OpportunitiesResponse, summary="Get writing opportunities")
async def post_writing_opportunities(
    request: OpportunityRequest,
    service: OpportunityService = Depends(get_opportunity_service),
) -> OpportunitiesResponse:
    """Find content writing opportunities based on trending topics and given seed topics.

    This endpoint identifies potential writing opportunities by finding trending topics and topics
    with growth potential that relate to your seed topics.

    Request body:
    - **region**: Two-letter country code (e.g., US, GB, AE)
    - **timeframe**: Time range for data (e.g., 'today 1-m', 'now 7-d')
    - **seed_topics**: Optional list of seed topics to base opportunities on
    - **limit**: Maximum number of opportunities to return (1-20)

    Returns a list of writing opportunities with suggested article ideas.
    """
    # Validate parameters
    region_code = validate_region_code(request.region) if request.region else None
    timeframe_parsed = parse_timeframe(request.timeframe)

    # Get writing opportunities
    opportunities_df = service.get_writing_opportunities(
        seed_topics=request.seed_topics,
        region=region_code,
        timeframe=timeframe_parsed,
        count=request.count,
    )

    # Convert to API response model
    opportunities = []

    if not opportunities_df.empty:
        for _, row in opportunities_df.iterrows():
            opportunity = OpportunityItem(
                title=row["topic"],
                score=float(row["opportunity_score"]),
                volume=float(row.get("volume", 50)),
                competition=float(row.get("competition", 50)),
                potential=float(row["growth_score"]),
                description=row.get("article_idea", None),
            )
            opportunities.append(opportunity)

    # Get current region if not specified
    if not region_code:
        region_code = service.client.get_current_region()

    from gtrends_core.utils.helpers import format_region_name

    region_name = format_region_name(region_code)

    seed_topics_list = request.seed_topics if request.seed_topics else []

    return OpportunitiesResponse(
        region_code=region_code,
        region_name=region_name,
        timeframe=timeframe_parsed,
        seed_topics=seed_topics_list,
        opportunities=opportunities,
    )
