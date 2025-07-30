# src/zenetics/cli/check.py
import typer
from rich.console import Console

from zenetics.api.zenetics_api_client import ZeneticsAPIClient
from zenetics.cli.common import handle_error
from zenetics.utils.environment import validate_environment

console = Console()


def check_connections(verbose: bool = False) -> None:
    """Check connections to Zenetics API."""
    try:
        # Validate environment first
        env_config = validate_environment()
        if verbose:
            print(env_config)

        with console.status("[bold yellow]Running connection checks...") as status:
            # Check Zenetics API connection
            status.update("[bold yellow]Testing Zenetics API connection...")
            zenetics_api_client = ZeneticsAPIClient(
                api_key=env_config.zenetics_key,
                api_url=env_config.zenetics_api_url,
                portal_url=env_config.zenetics_portal_url,
            )
            try:
                # Test API connection
                zenetics_api_client.check_connection()
                console.print("[green]✓[/green] Zenetics API connection successful")
            except Exception as e:
                console.print("[red]✗[/red] Zenetics API connection failed")
                console.print(f"  Error: {str(e)}")
                raise typer.Exit(1)

        console.print("\n[green]All connections are working correctly![/green]")

    except Exception as e:
        handle_error(e)
