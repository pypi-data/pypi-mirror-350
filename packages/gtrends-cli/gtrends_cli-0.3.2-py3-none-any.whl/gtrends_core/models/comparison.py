"""Models for comparison data from Google Trends."""

from dataclasses import dataclass
from typing import Dict, List, Union

from gtrends_core.models.base import BaseModel, RegionInterest, TimePoint


@dataclass(frozen=True)
class InterestOverTimeResult(BaseModel):
    """Container for interest over time results."""

    topics: List[str]
    region_code: str
    region_name: str
    timeframe: Union[str, List[str]]
    category: str
    time_series: Dict[str, List[TimePoint]]


@dataclass(frozen=True)
class InterestByRegionResult(BaseModel):
    """Container for interest by region results."""

    topics: List[str]
    region_code: str
    region_name: str
    timeframe: str
    category: str
    resolution: str
    region_interest: Dict[str, List[RegionInterest]]
