"""API router for geographical interest analysis."""

import logging
from typing import Optional

from fastapi import APIRouter, Depends, Path, Query

from gtrends_api.dependencies.core import get_geo_service
from gtrends_api.schemas.requests import GeoInterestRequest
from gtrends_api.schemas.responses import GeoInterestResponse, GeoRegionItem, RegionCodeResponse
from gtrends_core.services.geo_service import GeoService
from gtrends_core.utils.validators import parse_timeframe, validate_region_code

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/geo", tags=["geo"])


@router.get(
    "/interest/{query}",
    response_model=GeoInterestResponse,
    summary="Get geographical interest data",
)
async def get_geo_interest(
    query: str = Path(..., description="Search query to analyze geographical interest for"),
    region: Optional[str] = Query(
        None, description="Region code (e.g., US, GB). Auto-detects if not specified."
    ),
    resolution: str = Query(
        "COUNTRY", description="Geographic resolution level (COUNTRY, REGION, CITY, DMA)"
    ),
    timeframe: str = Query("today 12-m", description="Timeframe for data (e.g., 'today 12-m')"),
    category: str = Query("0", description="Category ID to filter results"),
    limit: int = Query(20, ge=1, le=50, description="Maximum number of regions to return"),
    service: GeoService = Depends(get_geo_service),
) -> GeoInterestResponse:
    """Get geographical interest data for a search query.

    This endpoint provides data on relative interest \
        in a search term across different geographic regions.

    - **query**: Search query to analyze geographical interest for
    - **region**: Two-letter country code (e.g., US, GB, AE)
    - **resolution**: Geographic resolution level (COUNTRY, REGION, CITY, DMA)
    - **timeframe**: Time range for data (e.g., 'today 12-m')
    - **category**: Category ID to filter results
    - **limit**: Maximum number of regions to return (1-50)

    Returns geographical interest data with interest values and levels.
    """
    # Validate parameters
    region_code = validate_region_code(region) if region else None
    timeframe_parsed = parse_timeframe(timeframe)

    # Get geographical interest data
    geo_data = service.get_interest_by_region(
        query=query,
        region=region_code,
        resolution=resolution,
        timeframe=timeframe_parsed,
        category=category,
        count=limit,
    )

    # Convert to API response model
    regions = []

    if not geo_data.empty:
        for _, row in geo_data.iterrows():
            geo_region = GeoRegionItem(
                name=row["geoName"],
                code=row["geoCode"],
                value=int(row["value"]),
                interest_level=row["interest_level"],
                percentile=float(row["percentile"]),
            )
            regions.append(geo_region)

    # Get region name if region is specified
    region_name = None
    if region_code:
        from gtrends_core.utils.helpers import format_region_name

        region_name = format_region_name(region_code)

    return GeoInterestResponse(
        query=query,
        region_code=region_code,
        region_name=region_name,
        resolution=resolution,
        timeframe=timeframe_parsed,
        category=category,
        regions=regions,
    )


@router.post(
    "/interest", response_model=GeoInterestResponse, summary="Get geographical interest data"
)
async def post_geo_interest(
    request: GeoInterestRequest,
    service: GeoService = Depends(get_geo_service),
) -> GeoInterestResponse:
    """Get geographical interest data for a search query.

    This endpoint provides data on relative interest \
        in a search term across different geographic regions.

    Request body:
    - **query**: Search query to analyze geographical interest for
    - **region**: Two-letter country code (e.g., US, GB, AE)
    - **resolution**: Geographic resolution level (COUNTRY, REGION, CITY, DMA)
    - **timeframe**: Time range for data (e.g., 'today 12-m')
    - **category**: Category ID to filter results
    - **limit**: Maximum number of regions to return (1-50)

    Returns geographical interest data with interest values and levels.
    """
    # Validate parameters
    region_code = validate_region_code(request.region) if request.region else None
    timeframe_parsed = parse_timeframe(request.timeframe)

    # Get geographical interest data
    geo_data = service.get_interest_by_region(
        query=request.query,
        region=region_code,
        resolution=request.resolution,
        timeframe=timeframe_parsed,
        category=request.category,
        count=request.limit,
    )

    # Convert to API response model
    regions = []

    if not geo_data.empty:
        for _, row in geo_data.iterrows():
            geo_region = GeoRegionItem(
                name=row["geoName"],
                code=row["geoCode"],
                value=int(row["value"]),
                interest_level=row["interest_level"],
                percentile=float(row["percentile"]),
            )
            regions.append(geo_region)

    # Get region name if region is specified
    region_name = None
    if region_code:
        from gtrends_core.utils.helpers import format_region_name

        region_name = format_region_name(region_code)

    return GeoInterestResponse(
        query=request.query,
        region_code=region_code,
        region_name=region_name,
        resolution=request.resolution,
        timeframe=timeframe_parsed,
        category=request.category,
        regions=regions,
    )


@router.get(
    "/codes/{search_term}", response_model=RegionCodeResponse, summary="Search for region codes"
)
async def get_region_codes(
    search_term: str = Path(..., description="Search term to find matching region codes"),
    service: GeoService = Depends(get_geo_service),
) -> RegionCodeResponse:
    """Search for country/region codes matching a search term.

    This endpoint helps find region codes that can be used in other API calls.

    - **search_term**: Search term to find matching region codes

    Returns matching region codes and names.
    """
    # Get region codes
    geo_codes = service.get_geo_codes_by_search(search_term)

    # Convert to API response model
    codes = []

    if not geo_codes.empty:
        for _, row in geo_codes.iterrows():
            codes.append(
                {
                    "code": row["code"],
                    "name": row["name"],
                }
            )

    return RegionCodeResponse(
        search_term=search_term,
        results=codes,
    )
