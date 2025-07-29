"""Command module for the 'categories' command."""

from typing import Optional

import click
from rich.console import Console
from rich.table import Table

console = Console()


@click.command()
@click.option("--find", "-f", help="Search term to filter categories")
def categories_command(find: Optional[str]):
    """List available Google Trends categories."""
    try:
        from gtrends_core.config import get_trends_client

        # Get trends client
        client = get_trends_client()

        # Get categories
        categories = client.get_categories()

        # Filter if search term provided
        if find:
            find_lower = find.lower()
            categories = {
                k: v
                for k, v in categories.items()
                if find_lower in k.lower() or find_lower in v.lower()
            }

        console.print("[bold]Google Trends Categories[/bold]\n")

        if categories:
            table = Table(
                title="Available Categories", show_header=True, header_style="bold magenta"
            )

            table.add_column("ID", style="cyan")
            table.add_column("Name", style="green")

            # Sort by category ID
            for category_id, category_name in sorted(categories.items(), key=lambda x: int(x[0])):
                table.add_row(category_id, category_name)

            console.print(table)
        else:
            if find:
                console.print(f"[yellow]No categories found matching '{find}'.[/yellow]")
            else:
                console.print("[yellow]No categories available.[/yellow]")

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
