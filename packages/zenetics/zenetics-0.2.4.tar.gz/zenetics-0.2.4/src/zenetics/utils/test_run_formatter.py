from rich.console import Console
from rich.table import Table
from rich import box
from typing import List

from zenetics.models.test_run import (
    EvaluationResultState,
    TestCaseResult,
    TestRun,
    TestSuiteResult,
)


class TestResultFormatter:
    def __init__(self, console: Console):
        self.console = console

    def display_results(self, test_run: TestRun, verbose: bool = False) -> None:
        """Display test results in the console."""
        for suite_result in test_run.test_suites:
            self._display_suite_results(suite_result, verbose)

    def _display_suite_results(
        self, suite_result: TestSuiteResult, verbose: bool
    ) -> None:
        """Display results for a single test suite."""
        # Calculate statistics
        total_evaluators = sum(len(tc.evaluations) for tc in suite_result.test_cases)
        passed_evaluators = sum(
            1
            for tc in suite_result.test_cases
            for eval_result in tc.evaluations
            if eval_result.result.state == EvaluationResultState.PASSED
        )
        failed_evaluators = total_evaluators - passed_evaluators
        success_rate = (
            (passed_evaluators / total_evaluators) * 100 if total_evaluators > 0 else 0
        )

        # Display summary header
        self.console.print(f"[bold]Test Suite: {suite_result.name}[/bold]")

        # Display statistics
        summary = (
            "[bold]Evaluation Summary:[/bold] "
            f"Total: [white]{total_evaluators}[/white], "
            f"Passed: [green]{passed_evaluators}[/green], "
            f"Failed: [red]{failed_evaluators}[/red], "
            f"Success Rate: "
            f"[{'green' if success_rate == 100 else 'red'}]{success_rate:.1f}%[/]"
        )
        self.console.print(summary)

        # Display duration and cost
        duration_in_seconds = suite_result.stats.duration / 1000
        total_tokens = (
            suite_result.token_usage.input_tokens
            + suite_result.token_usage.completion_tokens
        )
        formatted_total = format(total_tokens, ",").replace(",", ".")

        runtime_stats = (
            f"[bold]Duration:[/bold] [white]{duration_in_seconds:.2f}s[/white], "
            f"[bold]Tokens:[/bold] [white]{formatted_total}[/white]"
        )
        self.console.print(runtime_stats)

        # Create results table if there are failures or verbose mode is enabled
        has_failures = any(
            eval_result.result.state == EvaluationResultState.FAILED
            for tc in suite_result.test_cases
            for eval_result in tc.evaluations
        )

        if has_failures or verbose:
            self._display_detailed_results(suite_result.test_cases, verbose)

    def _display_detailed_results(
        self, test_cases: List[TestCaseResult], verbose: bool
    ) -> None:
        """Display detailed results table."""

        title = "Detailed Evaluation Results" if verbose else "Failed Evaluations"

        table = Table(
            title=f"\n{title}", show_header=True, header_style="bold", box=box.ROUNDED
        )

        # Add columns
        table.add_column("Test Case", style="")
        table.add_column("Evaluator", style="")
        table.add_column("Score", justify="left")
        table.add_column("Status", justify="center")
        table.add_column("Success Rate", justify="right")

        # Process results
        for test_case in test_cases:
            # Calculate test case success rate
            passed_evals = sum(
                1
                for e in test_case.evaluations
                if e.result.state == EvaluationResultState.PASSED
            )
            total_evals = len(test_case.evaluations)
            success_rate = (passed_evals / total_evals) * 100 if total_evals > 0 else 0

            # Filter evaluations based on verbose mode
            evaluations_to_show = test_case.evaluations
            if not verbose:
                evaluations_to_show = [
                    e
                    for e in test_case.evaluations
                    if e.result.state == EvaluationResultState.FAILED
                ]

            # Skip if no evaluations to show
            if not evaluations_to_show:
                continue

            # Add rows for each evaluation
            for idx, eval_result in enumerate(evaluations_to_show):
                test_case_name = test_case.name if idx == 0 else ""
                success_rate_str = f"{success_rate:.1f}%" if idx == 0 else ""

                status_style = (
                    "[green]PASSED[/green]"
                    if eval_result.result.state == EvaluationResultState.PASSED
                    else "[red]FAILED[/red]"
                    if eval_result.result.state == EvaluationResultState.FAILED
                    else "[yellow]SKIPPED[/yellow]"
                )

                threshold = eval_result.threshold

                table.add_row(
                    test_case_name,
                    eval_result.name,
                    f"[bold]Score: {eval_result.result.score:.3f}[/bold] "
                    f"(Threshold: {threshold})\nReason: {eval_result.result.reason}",
                    status_style,
                    success_rate_str,
                )

        # Display the table
        self.console.print(table)

        # Display legend if there are skipped evaluations
        has_skipped = any(
            eval_result.result.state == EvaluationResultState.SKIPPED
            for tc in test_cases
            for eval_result in tc.evaluations
        )
        if has_skipped:
            self.console.print("\n[bold]Legend:[/bold]")
            self.console.print(
                "[yellow]SKIPPED[/yellow]: Evaluator was not run"
                " due to previous failures"
            )
