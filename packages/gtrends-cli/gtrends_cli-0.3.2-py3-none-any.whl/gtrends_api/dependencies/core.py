"""Core dependencies for the API."""

from gtrends_core.config import get_trends_client
from gtrends_core.services.comparison_service import ComparisonService
from gtrends_core.services.geo_service import GeoService
from gtrends_core.services.growth_service import GrowthService
from gtrends_core.services.opportunity_service import OpportunityService
from gtrends_core.services.related_service import RelatedService
from gtrends_core.services.suggestion_service import SuggestionService
from gtrends_core.services.trending_service import TrendingService


def get_trending_service() -> TrendingService:
    """Get trending service instance.

    Returns:
        TrendingService: Service for trending searches
    """
    client = get_trends_client()
    return TrendingService(client)


def get_related_service() -> RelatedService:
    """Get related service instance.

    Returns:
        RelatedService: Service for related topics and queries
    """
    client = get_trends_client()
    return RelatedService(client)


def get_comparison_service() -> ComparisonService:
    """Get comparison service instance.

    Returns:
        ComparisonService: Service for comparing interest across topics
    """
    client = get_trends_client()
    return ComparisonService(client)


def get_suggestion_service() -> SuggestionService:
    """Get suggestion service instance.

    Returns:
        SuggestionService: Service for topic suggestions
    """
    client = get_trends_client()
    return SuggestionService(client)


def get_opportunity_service() -> OpportunityService:
    """Get opportunity service instance.

    Returns:
        OpportunityService: Service for finding writing opportunities
    """
    client = get_trends_client()
    return OpportunityService(client)


def get_growth_service() -> GrowthService:
    """Get growth service instance.

    Returns:
        GrowthService: Service for analyzing topic growth
    """
    client = get_trends_client()
    return GrowthService(client)


def get_geo_service() -> GeoService:
    """Get geo service instance.

    Returns:
        GeoService: Service for geographical interest analysis
    """
    client = get_trends_client()
    return GeoService(client)
