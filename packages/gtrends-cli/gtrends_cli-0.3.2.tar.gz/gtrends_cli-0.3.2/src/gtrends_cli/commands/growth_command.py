"""Command module for the 'topic-growth' command."""

from typing import Optional, Tuple

import click
from rich.console import Console
from rich.table import Table

from gtrends_cli.formatters.export import export_to_file
from gtrends_core.services.growth_service import GrowthService

console = Console()


@click.command()
@click.argument("topics", nargs=-1, required=True)
@click.option(
    "--period",
    "-p",
    type=click.Choice(["4h", "24h", "48h", "7d"]),
    default="24h",
    help="Time period to analyze (4h, 24h, 48h, 7d)",
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
@click.option("--visualize", "-v", is_flag=True, help="Generate visualization")
def topic_growth_command(
    topics: Tuple[str],
    period: str,
    export: bool,
    export_path: Optional[str],
    visualize: bool,
    format: str = "json",
):
    """Analyze growth trends for topics over recent time periods."""
    try:
        from gtrends_core.config import get_trends_client

        # Get trends client
        client = get_trends_client()

        # Create service
        service = GrowthService(client)

        # Convert tuple to list
        topics_list = list(topics)

        # Get growth data
        growth_df = service.get_topic_growth_data(
            topics=topics_list,
            time_period=period,
        )

        # Display results
        console.print(f"[bold]Growth analysis for topics over the past {period}[/bold]\n")

        # Format and display growth data
        if not growth_df.empty:
            table = Table(
                title=f"Topic Growth Trends (Past {period})",
                show_header=True,
                header_style="bold magenta",
            )

            table.add_column("Topic", style="cyan")
            table.add_column("Start Value", style="blue")
            table.add_column("End Value", style="blue")
            table.add_column("Growth %", style="green")
            table.add_column("Trend", style="yellow")

            for _, row in growth_df.iterrows():
                # Format growth percentage with sign and color
                growth_pct = row["growth_pct"]
                growth_str = f"{growth_pct:+.1f}%"
                growth_color = (
                    "[green]" if growth_pct > 0 else "[red]" if growth_pct < 0 else "[white]"
                )

                table.add_row(
                    row["topic"],
                    f"{row['start_value']:.1f}",
                    f"{row['end_value']:.1f}",
                    f"{growth_color}{growth_str}[/]",
                    row["trend"],
                )

            console.print(table)
        else:
            console.print("[yellow]No growth data found for the specified topics.[/yellow]")

        # Generate visualization if requested
        if visualize and not growth_df.empty:
            try:
                import matplotlib.pyplot as plt

                # Create bar chart
                plt.figure(figsize=(10, 6))

                # Get data for plotting
                topics = growth_df["topic"].tolist()
                growth_values = growth_df["growth_pct"].tolist()

                # Create colors based on growth values
                colors = ["green" if x > 0 else "red" for x in growth_values]

                # Create the bar chart
                bars = plt.bar(topics, growth_values, color=colors)

                # Add details
                plt.title(f"Topic Growth Analysis (Past {period})")
                plt.xlabel("Topics")
                plt.ylabel("Growth Percentage (%)")
                plt.axhline(y=0, color="black", linestyle="-", alpha=0.3)
                plt.grid(axis="y", linestyle="--", alpha=0.3)

                # Add value labels
                for bar in bars:
                    height = bar.get_height()
                    label_text = f"{height:+.1f}%"
                    plt.text(
                        bar.get_x() + bar.get_width() / 2.0,
                        height + (5 if height > 0 else -15),
                        label_text,
                        ha="center",
                        va="bottom" if height > 0 else "top",
                        fontweight="bold",
                    )

                # Adjust layout
                plt.tight_layout()

                # Save or show
                if export:
                    from gtrends_core.utils.validators import validate_export_path

                    export_dir = validate_export_path(export_path)
                    topics_str = "_".join(topics_list)
                    vis_file = export_dir / f"topic_growth_{topics_str}_{period}.png"
                    plt.savefig(vis_file)
                    console.print(f"[green]Visualization saved to {vis_file}[/green]")
                else:
                    plt.show()

            except ImportError:
                console.print(
                    "[yellow]Visualization require matplotlib. run: pip install matplotlib[/yellow]"
                )

        # Export data if requested
        if export and not growth_df.empty:
            from gtrends_core.utils.validators import validate_export_path

            export_dir = validate_export_path(export_path)
            topics_str = "_".join(topics_list)
            export_file = export_dir / f"topic_growth_{topics_str}_{period}.{format}"
            export_to_file(growth_df, export_file, format)

            console.print(f"[green]Results exported to {export_file}[/green]")

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
