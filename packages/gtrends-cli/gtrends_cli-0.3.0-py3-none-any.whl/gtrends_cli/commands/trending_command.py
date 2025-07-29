"""Command module for trending searches."""

from typing import Optional

import click
from rich.console import Console

from gtrends_cli.formatters.console import format_trending_searches
from gtrends_cli.formatters.export import export_data
from gtrends_core.config import DEFAULT_SUGGESTIONS_COUNT, get_trends_client
from gtrends_core.services.trending_service import TrendingService
from gtrends_core.utils import validate_export_path, validate_region_code

console = Console()


@click.command()
@click.option(
    "--region", "-r", help="Region code (e.g., US, GB, AE). Auto-detects if not specified."
)
@click.option(
    "--count",
    "-n",
    type=int,
    default=DEFAULT_SUGGESTIONS_COUNT,
    help=f"Number of results to display. Default: {DEFAULT_SUGGESTIONS_COUNT}",
)
@click.option("--with-news", "-w", is_flag=True, help="Include related news articles")
@click.option("--export", "-e", is_flag=True, help="Export results to file")
@click.option("--export-path", type=str, help="Directory to save exported data")
@click.option(
    "--format",
    "-f",
    type=click.Choice(["csv", "json", "xlsx"]),
    default="csv",
    help="Export format",
)
def trending_command(
    region: Optional[str],
    count: int,
    with_news: bool,
    export: bool,
    export_path: Optional[str],
    format: str = "json",
):
    """Show current trending searches on Google."""
    try:
        # Get the trends client
        client = get_trends_client()

        # Create service instance with the client
        service = TrendingService(client)

        # Validate region code if provided
        region_code = validate_region_code(region) if region else None

        # Fetch trending data
        if with_news:
            console.print("Fetching trending searches with news articles...", style="blue")
            results = service.get_trending_searches_with_articles(region=region_code, limit=count)
        else:
            console.print("Fetching trending searches...", style="blue")
            results = service.get_trending_searches(region=region_code, limit=count)

        # Display results
        region_name = results.region_name
        console.print(f"\n[bold]Trending Searches - {region_name}[/bold]\n")

        format_trending_searches(results, count=count)

        # Export if requested
        if export:
            export_path_obj = validate_export_path(export_path)
            export_file = export_path_obj / f"trending_searches_{results.region_code}.{format}"

            export_data(results, export_file, format)
            console.print(f"\nResults exported to: {export_file}")

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        raise
