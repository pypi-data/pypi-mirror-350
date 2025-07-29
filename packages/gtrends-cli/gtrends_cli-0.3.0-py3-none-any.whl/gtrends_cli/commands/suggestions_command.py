"""Command module for the 'suggest-topics' command."""

from typing import Optional

import click
from rich.console import Console
from rich.table import Table

from gtrends_cli.formatters.export import export_to_file
from gtrends_core.services.suggestion_service import SuggestionService
from gtrends_core.utils.helpers import format_region_name
from gtrends_core.utils.validators import parse_timeframe, validate_region_code

console = Console()


@click.command()
@click.option(
    "--category",
    "-c",
    default="books",
    type=click.Choice(["books", "news", "arts", "fiction", "culture"]),
    help="Content category to suggest topics for",
)
@click.option(
    "--region", "-r", help="Region code (e.g., US, GB, AE). Auto-detects if not specified."
)
@click.option(
    "--timeframe",
    "-t",
    default="today 7-d",
    help="Timeframe for data (e.g., 'today 7-d', 'today 1-m')",
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
def suggest_topics_command(
    category: str,
    region: Optional[str],
    timeframe: str,
    count: int,
    export: bool,
    export_path: Optional[str],
    format: str,
):
    """Suggest topics for content creators based on trends."""
    try:
        from gtrends_core.config import get_trends_client

        # Get trends client
        client = get_trends_client()

        # Create service
        service = SuggestionService(client)

        # Validate parameters
        region_code = validate_region_code(region) if region else None
        timeframe_parsed = parse_timeframe(timeframe)

        # Get topic suggestions
        suggestions_df = service.get_topic_suggestions(
            category=category,
            region=region_code,
            timeframe=timeframe_parsed,
            count=count,
        )

        # Display results
        region_display = region_code if region_code else client.get_current_region()
        region_name = format_region_name(region_display)

        console.print(
            f"[bold]suggestion {category} content in {region_name} over {timeframe_parsed}[/bold]\n"
        )

        # Format and display suggestions
        if not suggestions_df.empty:
            table = Table(
                title=f"Topic Suggestions - {category.title()} ({region_name})",
                show_header=True,
                header_style="bold magenta",
            )

            table.add_column("Topic", style="cyan")
            table.add_column("Relevance", style="green")
            table.add_column("Rising", style="yellow")
            table.add_column("Source", style="blue")

            for _, row in suggestions_df.iterrows():
                rising_status = "Yes" if row["rising"] else "No"
                table.add_row(
                    row["topic"],
                    str(int(row["relevance_score"])),
                    rising_status,
                    row["source"],
                )

            console.print(table)
        else:
            console.print("[yellow]No suggestions found for the given criteria.[/yellow]")

        # Export if requested
        if export and not suggestions_df.empty:
            from gtrends_core.utils.validators import validate_export_path

            export_dir = validate_export_path(export_path)
            export_file = export_dir / f"topic_suggestions_{category}_{region_display}.{format}"
            export_to_file(suggestions_df, export_file, format)

            console.print(f"[green]Results exported to {export_file}[/green]")

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
