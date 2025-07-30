import typer
from rich.console import Console
from typing import NoReturn

console = Console()


def handle_error(error: Exception) -> NoReturn:
    """Handle errors with proper formatting and exit codes."""
    if isinstance(error, typer.Exit):
        raise error

    console.print(f"[red]Error: {str(error)}[/red]")
    if isinstance(error, (ConnectionError, TimeoutError)):
        console.print("\nPlease check your internet connection and try again.")
    elif isinstance(error, ValueError):
        console.print("\nPlease check your input values and try again.")

    raise typer.Exit(1)
