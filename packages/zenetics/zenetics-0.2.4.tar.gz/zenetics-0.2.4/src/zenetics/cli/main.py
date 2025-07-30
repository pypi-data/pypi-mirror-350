# src/zenetics/cli/main.py
from pathlib import Path
import sys
import typer
from rich.console import Console

from zenetics.cli.run import run_tests_server

from .help import show_help
from .check import check_connections
from .testsuites import list_testsuites
from .common import handle_error

# Initialize Typer app and console
app = typer.Typer(
    name="zenetics", help="CLI for running Zenetics test suites", add_completion=False
)

console = Console()


@app.command()
def help() -> None:
    """Show detailed help information about all commands."""
    show_help()


@app.command()
def check(
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose output")
) -> None:
    """Check connections to Zenetics API."""
    check_connections(verbose=verbose)


@app.command()
def testsuites() -> None:
    """List all available test suites."""
    list_testsuites()


@app.command()
def run(
    test_suite_id: str = typer.Argument(..., help="ID of the test suite to run"),
    source_file: Path = typer.Argument(
        ...,
        help="Python file containing the generate function",
        exists=True,
        dir_okay=False,
        readable=True,
    ),
    output_dir: str = typer.Option(
        "test_results", "--output-dir", "-o", help="Directory for storing test results"
    ),
    local_only: bool = typer.Option(
        False,
        "--local-only",
        help="Run the test suite locally without connecting to Zenetics API",
    ),
    max_parallel: int = typer.Option(
        5,
        "--max-parallel",
        "-p",
        help="Maximum number of parallel evaluations (1-10)",
        min=1,
        max=10,
    ),
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="Enable verbose output"
    ),
) -> None:
    """Run a test suite with the specified generate function."""
    run_tests_server(
        test_suite_id=test_suite_id,
        source_file=source_file,
        output_dir=output_dir,
        local_only=local_only,
        verbose=verbose,
        parallel=max_parallel,
    )


@app.command()
def version() -> None:
    """Show the version of the Zenetics CLI."""
    from importlib.metadata import version as get_version

    try:
        version = get_version("zenetics")
        console.print(f"Zenetics CLI version: {version}")
    except Exception:
        console.print("Version information not available")


def main() -> None:
    """Entry point for the CLI."""
    try:
        app()
    except KeyboardInterrupt:
        console.print("\n[yellow]Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        handle_error(e)


if __name__ == "__main__":
    main()
