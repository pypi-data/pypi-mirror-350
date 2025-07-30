from rich.console import Console

console = Console()


def show_help() -> None:
    """Show detailed help information about all commands."""
    console.print("\n[bold]Zenetics Test Runner CLI[/bold]")
    console.print(
        "A command-line tool for running and managing Zenetics test suites.\n"
    )

    # Environment Setup
    console.print("[bold yellow]Environment Setup[/bold yellow]")
    console.print("Required environment variables:")
    console.print("  [cyan]ZENETICS_API_KEY[/cyan] - Your Zenetics API key")
    console.print("\nYou can set these using:")
    console.print("  export ZENETICS_API_KEY=your_key")
    console.print("  # Or create a .env file with these variables\n")

    # Commands
    console.print("[bold yellow]Available Commands[/bold yellow]")

    # run command
    console.print("\n[bold cyan]run[/bold cyan] <test-suite-id>")
    console.print("  Run a test suite with the specified ID")
    console.print("  Options:")
    console.print("    [green]-o, --output[/green]  Path to save results JSON file")
    console.print("    [green]-v, --verbose[/green] Enable verbose output")
    console.print(
        "    [green]-f, --force[/green]   Force overwrite existing output file"
    )
    console.print(
        "  Example: [italic]zenetics run test-123 -o results.json -v[/italic]"
    )

    # check command
    console.print("\n[bold cyan]check[/bold cyan]")
    console.print("  Verify connections to Zenetics API")
    console.print("  Example: [italic]zenetics check[/italic]")

    # version command
    console.print("\n[bold cyan]testsuites[/bold cyan]")
    console.print("  List all available test suites")
    console.print("  Example: [italic]zenetics testsuites[/italic]")

    # version command
    console.print("\n[bold cyan]version[/bold cyan]")
    console.print("  Show the CLI version")
    console.print("  Example: [italic]zenetics version[/italic]")

    # help command
    console.print("\n[bold cyan]help[/bold cyan]")
    console.print("  Show this help message")
    console.print("  Example: [italic]zenetics help[/italic]")

    # Additional Information
    console.print("\n[bold yellow]Additional Information[/bold yellow]")
    console.print("• All commands will return non-zero exit codes on failure")
    console.print("• Results are saved in JSON format for further processing")
    console.print("• Use verbose mode (-v) for detailed execution information")
    console.print("• Check command is recommended before running tests\n")

    # Further Help
    console.print("[bold yellow]Further Resources[/bold yellow]")
    console.print("• Documentation: https://docs.zenetics.io")
    console.print("• Issues: https://github.com/zenetics/zenetics-sdk/issues")
    console.print("• Support: contact@zenetics.io\n")
