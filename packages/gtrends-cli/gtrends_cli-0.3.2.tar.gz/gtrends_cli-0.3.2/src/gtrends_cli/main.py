"""Main entry point for the Google Trends CLI."""

import sys

import click
from rich.console import Console

from gtrends_cli.commands.categories_command import categories_command
from gtrends_cli.commands.compare_command import compare_command
from gtrends_cli.commands.geo_command import geo_command, geo_interest_command
from gtrends_cli.commands.growth_command import topic_growth_command
from gtrends_cli.commands.help_command import help_timeframe_command
from gtrends_cli.commands.opportunities_command import writing_opportunities_command
from gtrends_cli.commands.related_command import related_command
from gtrends_cli.commands.suggestions_command import suggest_topics_command
from gtrends_cli.commands.trending_command import trending_command
from gtrends_core import __version__

console = Console()


@click.group()
@click.version_option(version=__version__)
def cli():
    """Google Trends CLI - Fetch trending topics & analyze search interests for content creators."""


# Register commands
cli.add_command(trending_command, "trending")
cli.add_command(related_command, "related")
cli.add_command(compare_command, "compare")
cli.add_command(suggest_topics_command, "suggest-topics")
cli.add_command(writing_opportunities_command, "writing-opportunities")
cli.add_command(topic_growth_command, "topic-growth")
cli.add_command(geo_interest_command, "geo-interest")
cli.add_command(geo_command, "geo")
cli.add_command(categories_command, "categories")
cli.add_command(help_timeframe_command, "help-timeframe")


def main():
    """Entry point for the CLI."""
    try:
        cli()
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
