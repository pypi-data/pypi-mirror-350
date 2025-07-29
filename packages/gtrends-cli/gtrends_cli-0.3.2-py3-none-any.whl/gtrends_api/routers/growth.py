"""API router for topic growth analysis."""

import logging
from typing import List

from fastapi import APIRouter, Depends, Query

from gtrends_api.dependencies.core import get_growth_service
from gtrends_api.schemas.requests import GrowthRequest
from gtrends_api.schemas.responses import GrowthItem, GrowthResponse
from gtrends_core.services.growth_service import GrowthService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/growth", tags=["growth"])


@router.get("/", response_model=GrowthResponse, summary="Get topic growth data")
async def get_topic_growth(
    topics: List[str] = Query(..., description="List of topics to analyze growth for"),
    period: str = Query("24h", description="Time period to analyze (4h, 24h, 48h, 7d)"),
    service: GrowthService = Depends(get_growth_service),
) -> GrowthResponse:
    """Analyze growth trends for topics over recent time periods.

    This endpoint provides growth analysis for multiple topics over a specified time period,
    showing how interest has changed over time.

    - **topics**: List of topics to analyze growth for (required)
    - **period**: Time period to analyze (4h, 24h, 48h, 7d)

    Returns growth data for each topic, including \
        start/end values, growth percentage, and trend categorization.
    """
    # Get topic growth data
    growth_df = service.get_topic_growth_data(
        topics=topics,
        time_period=period,
    )

    # Convert to API response model
    growth_items = []

    if not growth_df.empty:
        for _, row in growth_df.iterrows():
            growth_item = GrowthItem(
                topic=row["topic"],
                trend_direction=row["trend"],
                growth_percentage=float(row["growth_pct"]),
                volume_index=float(row.get("end_value", 50)),
                data_points=None,
            )
            growth_items.append(growth_item)

    return GrowthResponse(
        topics=topics,
        period=period,
        results=growth_items,
    )


@router.post("/", response_model=GrowthResponse, summary="Get topic growth data")
async def post_topic_growth(
    request: GrowthRequest,
    service: GrowthService = Depends(get_growth_service),
) -> GrowthResponse:
    """Analyze growth trends for topics over recent time periods.

    This endpoint provides growth analysis for multiple topics over a specified time period,
    showing how interest has changed over time.

    Request body:
    - **topics**: List of topics to analyze growth for (required)
    - **period**: Time period to analyze (4h, 24h, 48h, 7d)

    Returns growth data for each topic, including \
        start/end values, growth percentage, and trend categorization.
    """
    # Get topic growth data
    growth_df = service.get_topic_growth_data(
        topics=request.topics,
        time_period=request.period,
    )

    # Convert to API response model
    growth_items = []

    if not growth_df.empty:
        for _, row in growth_df.iterrows():
            growth_item = GrowthItem(
                topic=row["topic"],
                trend_direction=row["trend"],
                growth_percentage=float(row["growth_pct"]),
                volume_index=float(row.get("end_value", 50)),
                data_points=None,
            )
            growth_items.append(growth_item)

    return GrowthResponse(
        topics=request.topics,
        period=request.period,
        results=growth_items,
    )
