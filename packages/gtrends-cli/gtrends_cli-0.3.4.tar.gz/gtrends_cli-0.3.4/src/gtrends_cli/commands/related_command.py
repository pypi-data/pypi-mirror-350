"""Command module for the 'related' command."""

from typing import Optional

import click
from rich.console import Console

from gtrends_cli.formatters.console import format_related_data
from gtrends_cli.formatters.export import export_to_file
from gtrends_core.services.related_service import RelatedService
from gtrends_core.utils.helpers import format_region_name
from gtrends_core.utils.validators import parse_timeframe, validate_region_code

console = Console()


@click.command()
@click.argument("query", type=str)
@click.option(
    "--region", "-r", help="Region code (e.g., US, GB, AE). Auto-detects if not specified."
)
@click.option(
    "--timeframe",
    "-t",
    default="today 3-m",
    help="Timeframe for data (e.g., 'today 3-m', 'today 12-m')",
)
@click.option(
    "--category",
    type=str,
    default="0",
    help="Category ID to filter results. Default: 0 (All)",
)
@click.option(
    "--count",
    "-n",
    type=int,
    default=10,
    help="Number of results to display. Default: 10",
)
@click.option("--export", "-e", is_flag=True, help="Export results to file")
@click.option("--export-path", type=str, help="Directory to save exported data")
@click.option(
    "--format",
    "-f",
    type=click.Choice(["csv", "json", "xlsx"]),
    default="csv",
    help="Export format",
)
def related_command(
    query: str,
    region: Optional[str],
    timeframe: str,
    category: str,
    count: int,
    export: bool,
    export_path: Optional[str],
    format: str = "json",
):
    """Show topics and queries related to a search term."""
    try:
        from gtrends_core.config import get_trends_client

        # Get trends client
        client = get_trends_client()

        # Create service
        service = RelatedService(client)

        # Validate parameters
        region_code = validate_region_code(region) if region else None
        timeframe_parsed = parse_timeframe(timeframe)

        # Get related data
        related_data = service.get_related_data(
            query=query,
            region=region_code,
            timeframe=timeframe_parsed,
            category=category,
        )

        # Display results
        region_display = region_code if region_code else client.get_current_region()
        region_name = format_region_name(region_display)

        console.print(
            f"[bold]Related data for '{query}' in {region_name} over {timeframe_parsed}[/bold]\n"
        )

        # Format and display related topics
        format_related_data(related_data.topics, data_type="topics", count=count)

        # Format and display related queries
        format_related_data(related_data.queries, data_type="queries", count=count)

        # Export if requested
        if export:
            from gtrends_core.utils.validators import validate_export_path

            export_dir = validate_export_path(export_path)

            # Export topics
            topics_file = export_dir / f"related_topics_{query}_{region_display}.{format}"
            export_to_file(related_data.topics, topics_file, format)

            # Export queries
            queries_file = export_dir / f"related_queries_{query}_{region_display}.{format}"
            export_to_file(related_data.queries, queries_file, format)

            console.print(f"[green]Results exported to {export_dir}[/green]")

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
