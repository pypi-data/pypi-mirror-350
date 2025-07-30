import typer
from rich.table import Table
from rich import box

from zenetics.api.zenetics_api_client import ZeneticsAPIClient

from ..utils.environment import validate_environment
from ..models.test_suite import TestSuiteState

from rich.console import Console

console = Console()


def list_testsuites() -> None:
    """List all available test suites."""
    try:
        # Validate environment first
        env_config = validate_environment()

        zenetics_api_client = ZeneticsAPIClient(
            api_key=env_config.zenetics_key,
            api_url=env_config.zenetics_api_url,
            portal_url=env_config.zenetics_portal_url,
        )

        with console.status("[bold yellow]Fetching test suites..."):
            # Fetch test suites from the Zenetics API
            test_suites = zenetics_api_client.list_test_suites()

            # Create and configure the table
            table = Table(
                title="Available Test Suites",
                show_header=True,
                header_style="bold",
                box=box.ROUNDED,
            )

            # Add columns
            table.add_column("ID", style="white", justify="right")
            table.add_column("Name", style="white")
            table.add_column("Description")
            table.add_column("State", justify="center")

            # Add rows with state-specific styling
            for suite in test_suites:
                # Define state-specific style
                state_style = (
                    "[green]●[/green]"
                    if suite.state == TestSuiteState.ACTIVE
                    else "[yellow]●[/yellow]"
                )

                table.add_row(
                    str(suite.seq_id),
                    suite.name,
                    suite.description or "",
                    f"{state_style} {suite.state.value}",
                )

            # Display the table
            console.print("\n")
            console.print(table)

            # Display summary
            active_count = sum(
                1 for s in test_suites if s.state == TestSuiteState.ACTIVE
            )
            paused_count = sum(
                1 for s in test_suites if s.state == TestSuiteState.PAUSED
            )

            console.print("\nSummary:")
            console.print(f"  [green]●[/green] Active: {active_count}")
            console.print(f"  [yellow]●[/yellow] Paused: {paused_count}")
            console.print(f"  Total: {len(test_suites)}\n")

    except Exception as e:
        console.print(f"[red]Error listing test suites: {str(e)}[/red]")
        raise typer.Exit(1)
