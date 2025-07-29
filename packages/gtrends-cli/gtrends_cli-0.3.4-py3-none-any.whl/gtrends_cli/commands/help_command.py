"""Command module for the help commands."""

import click
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()


@click.command()
def help_timeframe_command():
    """Show help for the timeframe format used in Google Trends."""
    # Create a text with rich formatting
    text = Text()

    text.append("Google Trends Timeframe Format\n\n", style="bold cyan")

    text.append(
        "Timeframe specifies the time range for which data is retrieved.\n\n", style="yellow"
    )

    text.append("Format: ", style="bold")
    text.append("<date> <time-range>\n\n")

    text.append("Date options:\n", style="bold green")
    text.append("  • now - Current date and time\n")
    text.append("  • today - Current date (midnight)\n\n")

    text.append("Time range options:\n", style="bold green")
    text.append("  • <n>-H - Last n hours\n")
    text.append("  • <n>-d - Last n days\n")
    text.append("  • <n>-m - Last n months\n")
    text.append("  • <n>-y - Last n years\n\n")

    text.append("Examples:\n", style="bold magenta")
    text.append("  • now 1-H - Last hour\n")
    text.append("  • now 4-H - Last 4 hours\n")
    text.append("  • now 1-d - Last 24 hours\n")
    text.append("  • today 1-d - Last day (from midnight)\n")
    text.append("  • today 7-d - Last 7 days (from midnight)\n")
    text.append("  • today 1-m - Last month\n")
    text.append("  • today 3-m - Last 3 months\n")
    text.append("  • today 12-m - Last year\n")
    text.append("  • today 5-y - Last 5 years\n\n")

    text.append("Notes:\n", style="bold red")
    text.append("  • For hourly data, use 'now' instead of 'today'\n")
    text.append("  • For data over many years, consider using 'today 5-y' format\n")
    text.append("  • Some time ranges may have less granular data\n")

    # Create a panel to display the formatted text
    panel = Panel(
        text,
        title="Timeframe Format Help",
        subtitle="Google Trends CLI",
        border_style="blue",
        padding=(1, 2),
    )

    console.print(panel)
