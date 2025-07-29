"""CLI command for comparing multiple topics."""

from typing import Optional, Tuple

import click
from rich.console import Console

from gtrends_cli.formatters.console import format_interest_over_time
from gtrends_cli.formatters.export import export_data
from gtrends_core.config import DEFAULT_CATEGORY, get_trends_client
from gtrends_core.services.comparison_service import ComparisonService
from gtrends_core.utils.helpers import format_region_name
from gtrends_core.utils.validators import (
    parse_timeframe,
    validate_export_path,
    validate_region_code,
)

console = Console()


@click.command()
@click.argument("topics", nargs=-1, required=True)
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
    default=DEFAULT_CATEGORY,
    help=f"Category ID to filter results. Default: {DEFAULT_CATEGORY} (All)",
)
@click.option("--export", "-e", is_flag=True, help="Export results to file")
@click.option("--export-path", type=str, help="Directory to save exported data")
@click.option(
    "--format",
    "-f",
    type=click.Choice(["csv", "json", "xlsx"]),
    default="json",
    help="Export format",
)
@click.option("--visualize", "-v", is_flag=True, help="Generate visualization")
def compare_command(
    topics: Tuple[str, ...],
    region: Optional[str],
    timeframe: str,
    category: str,
    export: bool,
    export_path: Optional[str],
    visualize: bool,
    format: str = "json",
):
    """Compare search interest between multiple topics."""
    try:
        if len(topics) > 5:
            console.print(
                "[bold yellow]Warning:[/bold yellow] Google Trends limits comparisons to 5 topics. \
                Only the first 5 will be used."
            )
            topics = topics[:5]

        # Get the trends client
        client = get_trends_client()

        service = ComparisonService(client)

        region_code = validate_region_code(region) if region else None
        timeframe_parsed = parse_timeframe(timeframe)

        # Get comparison results
        comparison_result = service.get_interest_over_time(
            queries=list(topics), region=region_code, timeframe=timeframe_parsed, category=category
        )

        # Display results
        region_display = region_code if region_code else service.get_current_region()
        region_name = format_region_name(region_display)

        console.print(
            f"[bold]Interest over time for {', '.join(topics)} in {region_name} \
                over {timeframe_parsed}[/bold]\n"
        )

        format_interest_over_time(comparison_result)

        # Generate visualization if requested
        if visualize:
            try:
                # Prepare visualization export path if needed
                viz_path = None
                if export:
                    export_dir = validate_export_path(export_path)
                    topics_slug = "_".join([t.replace(" ", "-")[:10] for t in topics])
                    viz_path = export_dir / f"comparison_{topics_slug}_{region_display}.png"

                # Generate visualization
                service.visualize_comparison(comparison_result, export_path=viz_path)

                if not export:
                    console.print(
                        "[yellow]Tip:[/yellow] Use --export to save the visualization to a file."
                    )

            except ImportError:
                console.print(
                    "[yellow]Visualization require matplotlib. run: pip install matplotlib[/yellow]"
                )
            except Exception as e:
                console.print(f"[red]Error creating visualization: {str(e)}[/red]")

        # Export data if requested
        if export:
            export_dir = validate_export_path(export_path)
            topics_slug = "_".join([t.replace(" ", "-")[:10] for t in topics])
            export_file = export_dir / f"comparison_{topics_slug}_{region_display}.{format}"

            # Use export_data which handles complex model types better
            export_data(comparison_result, export_file, format)
            console.print(f"[green]Results exported to {export_file}[/green]")

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
