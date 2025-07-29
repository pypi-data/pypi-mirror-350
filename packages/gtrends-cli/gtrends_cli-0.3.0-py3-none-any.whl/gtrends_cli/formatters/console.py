"""Console formatters for the CLI interface."""

from typing import Union

from rich.console import Console
from rich.table import Table

from gtrends_core.models.comparison import InterestByRegionResult, InterestOverTimeResult
from gtrends_core.models.related import RelatedQueryResults, RelatedTopicResults
from gtrends_core.models.trending import TrendingSearchResults

console = Console()


def format_trending_searches(results: TrendingSearchResults, count: int = 10) -> None:
    """Format trending search results for console output.

    Args:
        results: Trending search results
        count: Maximum number of results to display
    """

    # Create table for trending topics
    table = Table(show_header=True, header_style="bold blue")
    table.add_column("#", style="dim", width=4)
    table.add_column("Topic", min_width=20)

    # Check if we have volume data
    if any(hasattr(topic, "volume") and topic.volume is not None for topic in results.topics):
        table.add_column("Volume", width=12)

    # Check if we have growth percentage data
    if any(
        hasattr(topic, "volume_growth_pct") and topic.volume_growth_pct is not None
        for topic in results.topics
    ):
        table.add_column("Growth", width=10)

    # Check if we have geo data
    show_geo = any(hasattr(topic, "geo") and topic.geo for topic in results.topics)
    if show_geo:
        table.add_column("Region", width=8)

    # Add rows
    for i, topic in enumerate(results.topics[:count]):
        row = [str(topic.rank if topic.rank is not None else i + 1), topic.keyword]

        # Add volume if column exists
        if hasattr(table, "columns") and len(table.columns) > 2:
            # Convert volume to string, handling None values
            volume_str = (
                f"{topic.volume:,}" if hasattr(topic, "volume") and topic.volume is not None else ""
            )
            row.append(volume_str)

        # Add growth percentage if column exists
        if hasattr(table, "columns") and len(table.columns) > 3:
            growth_str = (
                f"{topic.volume_growth_pct:+.1f}%"
                if hasattr(topic, "volume_growth_pct") and topic.volume_growth_pct is not None
                else ""
            )
            row.append(growth_str)

        # Add region if column exists
        if hasattr(table, "columns") and len(table.columns) > 4:
            geo_str = topic.geo if hasattr(topic, "geo") and topic.geo else ""
            row.append(geo_str)

        table.add_row(*row)

    console.print(table)

    # Display trending topics details
    for i, topic in enumerate(results.topics[:count]):
        # Skip topics without additional details
        has_details = (
            (hasattr(topic, "trend_keywords") and topic.trend_keywords)
            or (hasattr(topic, "topics") and topic.topics)
            or (hasattr(topic, "news") and topic.news)
        )

        if not has_details:
            continue

        console.print(f"\n[bold]{topic.keyword}[/bold]")

        # Show trend keywords if available
        if hasattr(topic, "trend_keywords") and topic.trend_keywords:
            keywords_str = ", ".join(topic.trend_keywords[:10])
            if len(topic.trend_keywords) > 10:
                keywords_str += f"... ({len(topic.trend_keywords) - 10} more)"
            console.print(f"  Related Keywords: [italic]{keywords_str}[/italic]")

        # Show topic categories if available
        if hasattr(topic, "topics") and topic.topics:
            from gtrends_core.utils.helpers import get_topic_id_map

            topic_map = get_topic_id_map()
            topic_names = [topic_map.get(tid, f"Unknown ({tid})") for tid in topic.topics]
            topics_str = ", ".join(topic_names)
            console.print(f"  Categories: [italic]{topics_str}[/italic]")

        # Show news articles if available
        if hasattr(topic, "news") and topic.news:
            console.print("  News Articles:")
            for article in topic.news[:3]:  # Limit to 3 articles per topic
                console.print(
                    f"    • [link={article.url}]{article.title}[/link] - {article.source}"
                )

    # For backward compatibility - if news articles are in the old format
    if results.has_news and not any(
        hasattr(topic, "news") and topic.news for topic in results.topics
    ):
        console.print("\n[bold]Related News Articles[/bold]\n")

        for topic, articles in results.news_articles.items():
            if not articles:
                continue

            console.print(f"[bold]{topic}[/bold]")

            for article in articles[:3]:  # Limit to 3 articles per topic
                console.print(f"  • [link={article.url}]{article.title}[/link] - {article.source}")

            console.print()


def format_related_data(
    results: Union[RelatedTopicResults, RelatedQueryResults], count: int = 10
) -> None:
    """Format related topics or queries for console output.

    Args:
        results: Related topics or queries results
        count: Maximum number of results to display
    """
    is_topic = isinstance(results, RelatedTopicResults)
    data_type = "Topics" if is_topic else "Queries"

    # Get the appropriate lists based on the type
    if is_topic:
        top_items = results.top_topics
        rising_items = results.rising_topics
    else:
        top_items = results.top_queries
        rising_items = results.rising_queries

    # Format top items
    if top_items:
        console.print(f"\n[bold]Top {data_type}[/bold]\n")

        table = Table(show_header=True, header_style="bold blue")
        table.add_column("Rank", style="dim", width=4)
        table.add_column(data_type[:-1], min_width=20)
        table.add_column("Value", width=10)

        for i, item in enumerate(top_items[:count]):
            table.add_row(str(i + 1), item.title, f"{item.value:.0f}")

        console.print(table)

    # Format rising items
    if rising_items:
        console.print(f"\n[bold]Rising {data_type}[/bold]\n")

        table = Table(show_header=True, header_style="bold blue")
        table.add_column("Rank", style="dim", width=4)
        table.add_column(data_type[:-1], min_width=20)
        table.add_column("Value", width=10)

        for i, item in enumerate(rising_items[:count]):
            value_str = item.rising_value_text or f"{item.value:.0f}"
            table.add_row(str(i + 1), item.title, value_str)

        console.print(table)


def format_interest_over_time(results: InterestOverTimeResult) -> None:
    """Format interest over time results for console output.

    Args:
        results: Interest over time results
    """
    console.print(f"\n[bold]Interest Over Time for {', '.join(results.topics)}[/bold]\n")

    # Since time series data is complex, we'll show summary statistics
    for topic, points in results.time_series.items():
        if not points:
            continue

        # Calculate basic statistics
        values = [point.value for point in points]
        avg_value = sum(values) / len(values) if values else 0
        max_value = max(values) if values else 0
        min_value = min(values) if values else 0

        # Show date range
        start_date = min(points, key=lambda p: p.date).date if points else None
        end_date = max(points, key=lambda p: p.date).date if points else None
        date_range = (
            f"{start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}"
            if start_date and end_date
            else "N/A"
        )

        table = Table(show_header=False, box=None)
        table.add_column("Property", style="bold blue")
        table.add_column("Value")

        table.add_row("Topic", topic)
        table.add_row("Date Range", date_range)
        table.add_row("Avg. Interest", f"{avg_value:.1f}")
        table.add_row("Max. Interest", f"{max_value:.1f}")
        table.add_row("Min. Interest", f"{min_value:.1f}")
        table.add_row("Data Points", str(len(points)))

        console.print(table)
        console.print()


def format_interest_by_region(results: InterestByRegionResult, count: int = 10) -> None:
    """Format interest by region results for console output.

    Args:
        results: Interest by region results
        count: Maximum number of regions to display per topic
    """
    console.print(f"\n[bold]Interest By Region for {', '.join(results.topics)}[/bold]\n")
    console.print(f"Resolution: {results.resolution}\n")

    for topic, regions in results.region_interest.items():
        console.print(f"[bold]{topic}[/bold]")

        if not regions:
            console.print("  No data available")
            continue

        table = Table(show_header=True, header_style="bold blue")
        table.add_column("Rank", style="dim", width=4)
        table.add_column("Region", min_width=20)
        table.add_column("Interest", width=10)

        for i, region in enumerate(regions[:count]):
            table.add_row(str(i + 1), region.region_name, f"{region.value:.0f}")

        console.print(table)
        console.print()
