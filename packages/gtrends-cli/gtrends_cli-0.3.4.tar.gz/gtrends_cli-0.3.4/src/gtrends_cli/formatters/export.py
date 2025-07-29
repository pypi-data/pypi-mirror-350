"""Export formatters for the CLI interface."""

import json
import logging
from pathlib import Path
from typing import Dict, Union

import pandas as pd

from gtrends_core.models.base import BaseModel
from gtrends_core.models.comparison import InterestByRegionResult, InterestOverTimeResult
from gtrends_core.models.related import RelatedQueryResults, RelatedTopicResults
from gtrends_core.models.trending import TrendingSearchResults
from gtrends_core.utils.formatters import export_to_file

logger = logging.getLogger(__name__)


def model_to_dataframe(model: BaseModel) -> Union[pd.DataFrame, Dict[str, pd.DataFrame]]:
    """Convert a model to a pandas DataFrame.

    Args:
        model: Model to convert

    Returns:
        DataFrame or dict of DataFrames
    """
    # Handle different model types
    if isinstance(model, TrendingSearchResults):
        df = pd.DataFrame([topic.__dict__ for topic in model.topics])
        return df

    elif isinstance(model, RelatedTopicResults):
        top_df = pd.DataFrame([topic.__dict__ for topic in model.top_topics])
        rising_df = pd.DataFrame([topic.__dict__ for topic in model.rising_topics])
        return {"top_topics": top_df, "rising_topics": rising_df}

    elif isinstance(model, RelatedQueryResults):
        top_df = pd.DataFrame([query.__dict__ for query in model.top_queries])
        rising_df = pd.DataFrame([query.__dict__ for query in model.rising_queries])
        return {"top_queries": top_df, "rising_queries": rising_df}

    elif isinstance(model, InterestOverTimeResult):
        # For CSV and XLSX formats: Create a combined dataframe for all topics
        all_data = []
        for topic, points in model.time_series.items():
            for point in points:
                all_data.append({"topic": topic, "date": point.date, "value": point.value})

        # If there's data, return it
        if all_data:
            return pd.DataFrame(all_data)

        # If there's no data, create a simple DataFrame with model attributes
        return pd.DataFrame(
            [
                {
                    "topics": ", ".join(model.topics),
                    "region_code": model.region_code,
                    "region_name": model.region_name,
                    "timeframe": (
                        model.timeframe
                        if isinstance(model.timeframe, str)
                        else str(model.timeframe)
                    ),
                    "category": model.category,
                    "data_points": sum(len(points) for points in model.time_series.values()),
                }
            ]
        )

    elif isinstance(model, InterestByRegionResult):
        # Create a combined dataframe for all topics
        all_data = []
        for topic, regions in model.region_interest.items():
            for region in regions:
                all_data.append(
                    {
                        "topic": topic,
                        "region_code": region.region_code,
                        "region_name": region.region_name,
                        "value": region.value,
                    }
                )

        # If there's data, return it
        if all_data:
            return pd.DataFrame(all_data)

        # If there's no data, create a simple DataFrame with model attributes
        return pd.DataFrame(
            [
                {
                    "topics": ", ".join(model.topics),
                    "region_code": model.region_code,
                    "region_name": model.region_name,
                    "timeframe": model.timeframe,
                    "category": model.category,
                    "resolution": model.resolution,
                }
            ]
        )

    else:
        # Generic conversion for any BaseModel
        # First try to convert the model to a dict
        try:
            data = model.to_dict()

            # Convert nested BaseModel objects to dicts
            for key, value in data.items():
                if isinstance(value, BaseModel):
                    data[key] = value.to_dict()
                elif isinstance(value, list) and value and isinstance(value[0], BaseModel):
                    data[key] = [item.to_dict() for item in value]
                elif (
                    isinstance(value, dict)
                    and value
                    and any(isinstance(v, BaseModel) for v in value.values())
                ):
                    data[key] = {
                        k: v.to_dict() if isinstance(v, BaseModel) else v for k, v in value.items()
                    }

            # If time_series is in data and it's a dict, serialize it to JSON
            if "time_series" in data and isinstance(data["time_series"], dict):
                # Convert time points to simple dicts
                for topic, points in data["time_series"].items():
                    data["time_series"][topic] = [
                        {
                            "date": (
                                p.date.isoformat() if hasattr(p.date, "isoformat") else str(p.date)
                            ),
                            "value": p.value,
                        }
                        for p in points
                    ]

                # Serialize to JSON string for DataFrame storage
                data["time_series"] = json.dumps(data["time_series"])

            return pd.DataFrame([data])

        except Exception as e:
            logger.error(f"Error converting model to DataFrame: {e}")
            # Fallback: try to create a DataFrame from the model's __dict__
            try:
                return pd.DataFrame([model.__dict__])
            except Exception as e:
                # Last resort: create a DataFrame with just the string representation
                logger.error(f"Error converting model to DataFrame: {e}")
                return pd.DataFrame([{"data": str(model)}])


def export_data(model: BaseModel, file_path: Union[str, Path], format: str = "csv") -> str:
    """Export model data to a file.

    Args:
        model: Model to export
        file_path: Path to save the file
        format: Export format (csv, json, xlsx)

    Returns:
        Path of the saved file
    """
    df_data = model_to_dataframe(model)

    # If it's an InterestOverTimeResult and we're exporting to JSON,
    # create a more structured JSON output
    if isinstance(model, InterestOverTimeResult) and format.lower() == "json":
        file_path = Path(file_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)

        # Create a more structured JSON representation
        result = {
            "topics": model.topics,
            "region_code": model.region_code,
            "region_name": model.region_name,
            "timeframe": model.timeframe,
            "category": model.category,
            "time_series": {},
        }

        # Convert time points to dictionaries
        for topic, points in model.time_series.items():
            result["time_series"][topic] = [
                {
                    "date": (
                        point.date.isoformat()
                        if hasattr(point.date, "isoformat")
                        else str(point.date)
                    ),
                    "value": point.value,
                }
                for point in points
            ]

        # Write JSON to file
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        return str(file_path)

    return export_to_file(df_data, file_path, format)
