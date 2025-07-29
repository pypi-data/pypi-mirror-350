"""Formatter utilities for Google Trends data."""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Union

import pandas as pd

from gtrends_core.exceptions.trends_exceptions import ExportException


def pandas_to_records(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """Convert a pandas DataFrame to a list of dictionaries.

    Args:
        df: DataFrame to convert

    Returns:
        List of dictionaries
    """
    if df is None or df.empty:
        return []

    return df.to_dict(orient="records")


def trend_to_dict(trend) -> Dict[str, Any]:
    """Convert a TrendingTopic object to a dictionary.

    Args:
        trend: TrendingTopic object

    Returns:
        Dictionary representation of the trend
    """
    result = {k: v for k, v in trend.__dict__.items() if not k.startswith("_")}

    # Convert news articles to dictionaries
    if "news" in result and result["news"]:
        result["news"] = [
            {
                "title": article.title,
                "source": article.source,
                "url": article.url,
                "time": (
                    article.time.isoformat() if hasattr(article.time, "isoformat") else article.time
                ),
                "picture": article.picture,
                "snippet": article.snippet,
            }
            for article in result["news"]
        ]

    # Convert timestamps if needed
    for ts_field in ["started_timestamp", "ended_timestamp"]:
        if ts_field in result and result[ts_field] and isinstance(result[ts_field], tuple):
            result[f"{ts_field}_str"] = datetime.fromtimestamp(result[ts_field][0]).isoformat()

    return result


def trend_list_to_dicts(trend_list) -> List[Dict[str, Any]]:
    """Convert a TrendList object to a list of dictionaries.

    Args:
        trend_list: TrendList object

    Returns:
        List of dictionaries
    """
    return [trend_to_dict(trend) for trend in trend_list]


def trend_list_to_dataframe(trend_list) -> pd.DataFrame:
    """Convert a TrendList object to a pandas DataFrame.

    Args:
        trend_list: TrendList object

    Returns:
        DataFrame representation of the trend list
    """
    # Convert trends to dictionaries, flattening the structure
    flat_trends = []
    for trend in trend_list:
        trend_dict = trend_to_dict(trend)

        # Handle news separately to avoid nesting
        news = trend_dict.pop("news", [])
        news_count = len(news)

        # Flatten news titles and sources into comma-separated strings
        if news_count > 0:
            trend_dict["news_titles"] = ", ".join([n["title"] for n in news])
            trend_dict["news_sources"] = ", ".join([n["source"] for n in news])

        trend_dict["news_count"] = news_count

        # Convert lists to comma-separated strings
        for k, v in trend_dict.items():
            if isinstance(v, list):
                trend_dict[k] = ", ".join([str(item) for item in v])

        flat_trends.append(trend_dict)

    # Create DataFrame
    if not flat_trends:
        return pd.DataFrame()

    return pd.DataFrame(flat_trends)


def export_to_file(
    data: Union[pd.DataFrame, Dict[str, pd.DataFrame], List, object],
    file_path: Union[str, Path],
    format: str = "csv",
) -> str:
    """Export data to a file.

    Args:
        data: Data to export (DataFrame, dict of DataFrames, TrendList, or other objects)
        file_path: Path to save the file
        format: Export format (csv, json, xlsx)

    Returns:
        Path of the saved file

    Raises:
        ExportException: If export fails
    """
    file_path = Path(file_path)

    try:
        # Handle TrendList objects
        if hasattr(data, "__class__") and data.__class__.__name__ == "TrendList":
            if format.lower() == "json":
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(trend_list_to_dicts(data), f, ensure_ascii=False, indent=2)
            elif format.lower() in ["csv", "xlsx"]:
                df = trend_list_to_dataframe(data)
                if format.lower() == "csv":
                    df.to_csv(file_path, index=False)
                else:  # xlsx
                    df.to_excel(file_path, index=False)
            else:
                raise ExportException(
                    f"Unsupported export format for TrendList: {format}",
                    file_path=str(file_path),
                    format=format,
                )
            return str(file_path)

        # Handle DataFrame
        elif isinstance(data, pd.DataFrame):
            if format.lower() == "csv":
                data.to_csv(file_path, index=False)
            elif format.lower() == "json":
                data.to_json(file_path, orient="records", date_format="iso")
            elif format.lower() == "xlsx":
                data.to_excel(file_path, index=False)
            else:
                raise ExportException(
                    f"Unsupported export format: {format}", file_path=str(file_path), format=format
                )

        # Handle dictionary of DataFrames
        elif isinstance(data, dict):
            # For dictionaries of DataFrames, save multiple sheets in Excel
            # or create multiple files for CSV and JSON
            if format.lower() == "xlsx":
                with pd.ExcelWriter(file_path) as writer:
                    for sheet_name, df in data.items():
                        if not isinstance(df, pd.DataFrame):
                            continue
                        sheet_name = str(sheet_name)[:31]  # Excel limits sheet names to 31 chars
                        df.to_excel(writer, sheet_name=sheet_name, index=False)
            else:
                # Create a directory based on the file name
                dir_name = file_path.stem
                dir_path = file_path.parent / dir_name
                dir_path.mkdir(exist_ok=True)

                # Save each DataFrame to a separate file
                for key, df in data.items():
                    if not isinstance(df, pd.DataFrame):
                        continue

                    safe_key = "".join(c if c.isalnum() else "_" for c in str(key))
                    file_name = f"{safe_key}.{format.lower()}"
                    sub_path = dir_path / file_name

                    if format.lower() == "csv":
                        df.to_csv(sub_path, index=False)
                    elif format.lower() == "json":
                        df.to_json(sub_path, orient="records", date_format="iso")

                # Return the directory path
                return str(dir_path)

        # Handle lists that might contain TrendingTopic objects
        elif (
            isinstance(data, list)
            and len(data) > 0
            and hasattr(data[0], "__class__")
            and data[0].__class__.__name__ == "TrendingTopic"
        ):
            # Convert the list to a TrendList first
            from gtrends_core.models.trending import TrendList

            return export_to_file(TrendList(data), file_path, format)

        # Handle other list types
        elif isinstance(data, list):
            if format.lower() == "json":
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
            elif format.lower() in ["csv", "xlsx"]:
                # Try to convert list to DataFrame
                try:
                    df = pd.DataFrame(data)
                    if format.lower() == "csv":
                        df.to_csv(file_path, index=False)
                    else:  # xlsx
                        df.to_excel(file_path, index=False)
                except Exception as e:
                    raise ExportException(
                        f"Could not convert list to DataFrame: {str(e)}",
                        file_path=str(file_path),
                        format=format,
                    )
            else:
                raise ExportException(
                    f"Unsupported export format for list: {format}",
                    file_path=str(file_path),
                    format=format,
                )
        else:
            # If it's neither a DataFrame nor a dict of DataFrames
            raise ExportException(
                "Unsupported data type for export", file_path=str(file_path), format=format
            )

        return str(file_path)
    except Exception as e:
        if not isinstance(e, ExportException):
            raise ExportException(
                f"Failed to export data: {str(e)}", file_path=str(file_path), format=format
            )
        raise
