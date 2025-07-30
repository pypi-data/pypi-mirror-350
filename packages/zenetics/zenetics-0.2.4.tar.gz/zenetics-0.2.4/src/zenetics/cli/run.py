import datetime
import importlib.util
import asyncio
from pathlib import Path
from typing import Callable
import typer
from rich.console import Console

from zenetics.testrunners.test_runner_server import TestSuiteRunnerServer
from zenetics.utils.test_run_formatter import TestResultFormatter

from .common import handle_error
from ..utils.environment import validate_environment

console = Console()
formatter = TestResultFormatter(console)


def load_generate_function(file_path: Path) -> Callable:
    """Load the generate function from a Python file."""
    try:
        spec = importlib.util.spec_from_file_location(file_path.stem, file_path)
        if spec is None or spec.loader is None:
            raise ImportError(f"Could not load module from {file_path}")

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        if not hasattr(module, "generate"):
            raise ValueError(f"Missing 'generate' function in {file_path}")

        return module.generate

    except Exception as e:
        raise ValueError(f"Error loading generate function from {file_path}: {str(e)}")


def run_tests_server(
    test_suite_id: str,
    source_file: Path,
    output_dir: str,
    local_only: bool,
    verbose: bool,
    parallel: int = 2,
    use_async: bool = False,
) -> None:
    """
    Run tests using the specified test suite and generate function.

    Args:
        test_suite_id: ID of the test suite to run
        source_file: Path to the Python file containing the generate function
        output_dir: Directory to save output files
        local_only: If True, don't upload results to Zenetics
        verbose: Enable verbose output
        parallel: Maximum number of parallel evaluations
        use_async: Use asynchronous execution for potentially better performance
    """
    try:
        # Validate environment first
        env_config = validate_environment()

        # Create output directory
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        if verbose:
            console.print(
                f"\nLoading generate function from [cyan]{source_file}[/cyan]"
            )

        try:
            # Load the generate function
            generate_fn = load_generate_function(source_file)

            # Create result file name
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            result_file = (
                output_path
                / f"{timestamp}_{source_file.stem}_{test_suite_id}_results.json"
            )

            # Initialize test runner
            runner = TestSuiteRunnerServer(
                test_suite_id=test_suite_id,
                zenetics_api_key=env_config.zenetics_key,
                zenetics_api_url=env_config.zenetics_api_url,
                zenetics_portal_url=env_config.zenetics_portal_url,
                console=console,
                max_parallel=parallel,
            )

            if verbose:
                console.print(f"Running test suite id: {test_suite_id}")
                console.print(f"Maximum parallel evaluations: {parallel}")
                console.print(
                    f"Execution mode: {'Asynchronous' if use_async else 'Synchronous'}"
                )

            # Run the tests
            if use_async:
                # Run asynchronously
                results, test_run_url = asyncio.run(
                    runner.run_async(
                        generate_fn=generate_fn,
                        output_file=result_file,
                        max_parallel=parallel,
                        save_to_zenetics=not local_only,
                    )
                )
            else:
                # Run synchronously
                results, test_run_url = runner.run(
                    generate_fn=generate_fn,
                    output_file=result_file,
                    max_parallel=parallel,
                    save_to_zenetics=not local_only,
                )

            # Print results
            console.print("\n")
            formatter.display_results(results, verbose)
            console.print(f"\nResults saved in: {result_file}")

            if not local_only and test_run_url:
                # Results already saved to Zenetics in the run method
                # if save_to_zenetics=True
                console.print(
                    f"View results in Zenetics: [link={test_run_url}]"
                    f"{test_run_url}[/link]"
                )
                console.print("\n")
            else:
                console.print("No test run saved in Zenetics (local run only)")

        except Exception as e:
            console.print(f"[bold red]Error running tests: {str(e)}[/bold red]")
            if verbose:
                import traceback

                console.print(traceback.format_exc())
            raise typer.Exit(1)

    except Exception as e:
        handle_error(e)


# Add this function to create the Typer command
def register_commands(app: typer.Typer) -> None:
    """Register test commands with the Typer app."""

    @app.command("run")
    def run_tests(
        test_suite_id: str = typer.Argument(..., help="ID of the test suite to run"),
        source_file: Path = typer.Argument(
            ..., help="Path to Python file with 'generate' function"
        ),
        output_dir: str = typer.Option("./results", help="Directory to save results"),
        local_only: bool = typer.Option(False, help="Don't upload results to Zenetics"),
        verbose: bool = typer.Option(False, help="Enable verbose output"),
        parallel: int = typer.Option(5, help="Maximum number of parallel evaluations"),
        async_mode: bool = typer.Option(
            False, "--async", help="Use asynchronous execution"
        ),
    ):
        """Run tests for the specified test suite using the generate function."""
        run_tests_server(
            test_suite_id=test_suite_id,
            source_file=source_file,
            output_dir=output_dir,
            local_only=local_only,
            verbose=verbose,
            parallel=parallel,
            use_async=async_mode,
        )
