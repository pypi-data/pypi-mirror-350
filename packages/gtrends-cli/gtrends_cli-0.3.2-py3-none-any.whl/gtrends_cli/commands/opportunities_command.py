"""Command module for the 'writing-opportunities' command."""

from typing import Optional, Tuple

import click
from rich.console import Console
from rich.table import Table

from gtrends_cli.formatters.export import export_to_file
from gtrends_core.services.opportunity_service import OpportunityService
from gtrends_core.utils.helpers import format_region_name
from gtrends_core.utils.validators import parse_timeframe, validate_region_code

console = Console()


@click.command()
@click.option(
    "--region", "-r", help="Region code (e.g., US, GB, AE). Auto-detects if not specified."
)
@click.option(
    "--timeframe",
    "-t",
    default="today 1-m",
    help="Timeframe for data (e.g., 'today 1-m', 'now 7-d')",
)
@click.option("--count", "-n", type=int, default=5, help="Number of opportunities to find")
@click.option("--export", "-e", is_flag=True, help="Export results to file")
@click.option("--export-path", type=str, help="Directory to save exported data")
@click.option(
    "--format",
    "-f",
    type=click.Choice(["csv", "json", "xlsx"]),
    default="csv",
    help="Export format",
)
@click.argument("seed_topics", nargs=-1)
def writing_opportunities_command(
    region: Optional[str],
    timeframe: str,
    count: int,
    export: bool,
    export_path: Optional[str],
    format: str,
    seed_topics: Tuple[str],
):
    """Find content writing opportunities based on trending topics and seeds."""
    try:
        from gtrends_core.config import get_trends_client

        # Get trends client
        client = get_trends_client()

        # Create service
        service = OpportunityService(client)

        # Validate parameters
        region_code = validate_region_code(region) if region else None
        timeframe_parsed = parse_timeframe(timeframe)

        # Convert tuple to list
        seed_topics_list = list(seed_topics) if seed_topics else None

        # Get writing opportunities
        opportunities_df = service.get_writing_opportunities(
            seed_topics=seed_topics_list,
            region=region_code,
            timeframe=timeframe_parsed,
            count=count,
        )

        # Display results
        region_display = region_code if region_code else client.get_current_region()
        region_name = format_region_name(region_display)

        console.print(
            f"[bold]Writing opportunities in {region_name} over {timeframe_parsed}[/bold]\n"
        )

        # Format and display opportunities
        if not opportunities_df.empty:
            table = Table(
                title=f"Content Writing Opportunities ({region_name})",
                show_header=True,
                header_style="bold magenta",
                width=100,
            )

            table.add_column("Topic", style="cyan", width=20)
            table.add_column("Opportunity Score", style="green", width=10)
            table.add_column("Growth", style="yellow", width=10)
            table.add_column("Related To", style="blue", width=15)
            table.add_column("Article Idea", style="white", width=45)

            for _, row in opportunities_df.iterrows():
                table.add_row(
                    row["topic"],
                    str(int(row["opportunity_score"])),
                    str(int(row["growth_score"])),
                    row["related_to"],
                    row["article_idea"],
                )

            console.print(table)
        else:
            console.print("[yellow]No writing opportunities found for the given criteria.[/yellow]")

        # Export if requested
        if export and not opportunities_df.empty:
            from gtrends_core.utils.validators import validate_export_path

            export_dir = validate_export_path(export_path)
            seeds_str = "_".join(seed_topics_list) if seed_topics_list else "general"
            export_file = (
                export_dir / f"writing_opportunities_{seeds_str}_{region_display}.{format}"
            )
            export_to_file(opportunities_df, export_file, format)

            console.print(f"[green]Results exported to {export_file}[/green]")

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
