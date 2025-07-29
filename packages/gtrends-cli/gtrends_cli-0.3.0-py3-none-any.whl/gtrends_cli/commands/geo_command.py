"""Command module for the geographical commands."""

from typing import Optional

import click
from rich.console import Console
from rich.table import Table

from gtrends_cli.formatters.export import export_to_file
from gtrends_core.services.geo_service import GeoService
from gtrends_core.utils.helpers import format_region_name
from gtrends_core.utils.validators import parse_timeframe, validate_region_code

console = Console()


@click.command()
@click.argument("query", type=str)
@click.option(
    "--region", "-r", help="Region code (e.g., US, GB, AE). Auto-detects if not specified."
)
@click.option(
    "--resolution",
    type=click.Choice(["COUNTRY", "REGION", "CITY", "DMA"]),
    default="COUNTRY",
    help="Geographic resolution level",
)
@click.option(
    "--timeframe", "-t", default="today 12-m", help="Timeframe for data (e.g., 'today 12-m')"
)
@click.option(
    "--category",
    type=str,
    default="0",
    help="Category ID to filter results. Default: 0 (All)",
)
@click.option("--count", "-n", type=int, default=20, help="Number of regions to display")
@click.option("--export", "-e", is_flag=True, help="Export results to file")
@click.option("--export-path", type=str, help="Directory to save exported data")
@click.option(
    "--format",
    "-f",
    type=click.Choice(["csv", "json", "xlsx"]),
    default="csv",
    help="Export format",
)
def geo_interest_command(
    query: str,
    region: Optional[str],
    resolution: str,
    timeframe: str,
    category: str,
    count: int,
    export: bool,
    export_path: Optional[str],
    format: str,
):
    """Show geographical interest for a search term."""
    try:
        from gtrends_core.config import get_trends_client

        # Get trends client
        client = get_trends_client()

        # Create service
        service = GeoService(client)

        # Validate parameters
        region_code = validate_region_code(region) if region else None
        timeframe_parsed = parse_timeframe(timeframe)

        # Get geo interest data
        geo_data = service.get_interest_by_region(
            query=query,
            region=region_code,
            resolution=resolution,
            timeframe=timeframe_parsed,
            category=category,
            count=count,
        )

        # Display results
        region_display = region_code if region_code else "Global"
        region_name = format_region_name(region_display) if region_code else "Global"

        console.print(
            f"[bold]Geographical interest for '{query}' in {region_name} "
            f"({resolution}) over {timeframe_parsed}[/bold]\n"
        )

        # Format and display geo data
        if not geo_data.empty:
            table = Table(
                title=f"Geographic Interest - {query}",
                show_header=True,
                header_style="bold magenta",
            )

            table.add_column("Region", style="cyan")
            table.add_column("Code", style="blue")
            table.add_column("Interest", style="green")
            table.add_column("Level", style="yellow")

            for _, row in geo_data.iterrows():
                # Get interest value with appropriate color
                interest_value = int(row["value"]) if "value" in row else 0
                interest_level = row["interest_level"] if "interest_level" in row else "Unknown"

                # Determine color based on interest level
                level_color = "[green]"
                if interest_level.startswith("Very High"):
                    level_color = "[bright_green]"
                elif interest_level.startswith("High"):
                    level_color = "[green]"
                elif interest_level.startswith("Moderate"):
                    level_color = "[yellow]"
                elif interest_level.startswith("Low"):
                    level_color = "[dim]"
                elif interest_level.startswith("Very Low"):
                    level_color = "[dim red]"

                table.add_row(
                    row["geoName"] if "geoName" in row else "Unknown",
                    row["geoCode"] if "geoCode" in row else "Unknown",
                    str(interest_value),
                    f"{level_color}{interest_level}[/]",
                )

            console.print(table)
        else:
            console.print("[yellow]No geographical data found for the given criteria.[/yellow]")

        # Export if requested
        if export and not geo_data.empty:
            from gtrends_core.utils.validators import validate_export_path

            export_dir = validate_export_path(export_path)
            region_suffix = f"_{region_code}" if region_code else ""
            export_file = export_dir / f"geo_interest_{query}{region_suffix}_{resolution}.{format}"
            export_to_file(geo_data, export_file, format)

            console.print(f"[green]Results exported to {export_file}[/green]")

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")


@click.command()
@click.argument("search_term", required=True)
def geo_command(search_term: str):
    """Search for country/region codes matching the search term."""
    try:
        from gtrends_core.config import get_trends_client

        # Get trends client
        client = get_trends_client()

        # Create service
        service = GeoService(client)

        # Search for region codes
        geo_codes = service.get_geo_codes_by_search(search_term)

        # Display results
        console.print(f"[bold]Region codes matching '{search_term}'[/bold]\n")

        if not geo_codes.empty:
            table = Table(
                title="Matching Region Codes", show_header=True, header_style="bold magenta"
            )

            table.add_column("Region", style="cyan")
            table.add_column("Code", style="green")

            for _, row in geo_codes.iterrows():
                table.add_row(
                    row["name"],
                    row["code"],
                )

            console.print(table)
        else:
            console.print(f"[yellow]No region codes found matching '{search_term}'.[/yellow]")

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
