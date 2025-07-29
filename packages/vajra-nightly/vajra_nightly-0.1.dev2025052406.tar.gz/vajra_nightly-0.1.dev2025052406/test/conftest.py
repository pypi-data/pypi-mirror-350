import os
import re
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

import pytest
import torch
from pytest import Config, Item, TestReport
from rich.console import Console
from rich.panel import Panel
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich.theme import Theme

# Regex to extract parameters from a test nodeid
PARAM_PATTERN = re.compile(r"\[(.*?)\]$")


@pytest.fixture
def gpu_test_sync_cuda():
    torch.cuda.synchronize()
    yield
    torch.cuda.synchronize()


@dataclass
class TestRunStats:
    """Tracks statistics for test execution."""

    start_time: float = 0.0
    total_duration: float = 0.0
    tests_executed: int = 0
    tests_passed: int = 0
    tests_failed: int = 0
    tests_skipped: int = 0
    tests_deselected: int = 0  # New field to track deselected tests
    slowest_tests: List[Tuple[str, float]] = field(default_factory=list)

    def __post_init__(self):
        self.slowest_tests = []
        self.start_time = time.time()

    def update_duration(self):
        self.total_duration = time.time() - self.start_time

    def record_test_duration(self, test_name: str, duration: float):
        self.slowest_tests.append((test_name, duration))
        self.slowest_tests.sort(key=lambda x: x[1], reverse=True)
        if len(self.slowest_tests) > 10:  # Keep only the 10 slowest tests
            self.slowest_tests.pop()


# Function to detect if we're running in a CI environment
def is_running_in_ci() -> bool:
    """Detect if the code is running in a CI environment."""
    # Check for common CI environment variables
    ci_env_vars = [
        "CI",
        "CONTINUOUS_INTEGRATION",
        "GITHUB_ACTIONS",
        "GITLAB_CI",
        "JENKINS_URL",
        "TRAVIS",
        "CIRCLECI",
        "VAJRA_IS_CI_CONTEXT",
        "APPVEYOR",
        "TF_BUILD",  # Azure Pipelines
    ]

    return any(os.environ.get(var) for var in ci_env_vars)


custom_theme = Theme(
    {
        "success": "green",
        "failure": "red",
        "skip": "yellow",
        "warning": "yellow",
        "info": "cyan",
        "debug": "blue",
        "title": "magenta bold",
        "unit": "cyan",
        "integration": "blue",
        "performance": "magenta",
        "correctness": "green",
    }
)

console = Console(theme=custom_theme, force_terminal=True)
stats = TestRunStats()
_pytest_config: Optional[Config] = None
_current_progress = None
_test_progress_task = None
_show_params: bool = True
_show_error_details: bool = True
_use_progress_bar: bool = not is_running_in_ci()
_collected_items_count: int = 0  # Track total collected items before deselection
_first_test_seen: bool = False  # Flag to detect the first test execution


def pytest_configure(config: Config) -> None:
    """Pytest hook to capture config object and initialize progress bar."""
    global _pytest_config, _current_progress, _test_progress_task, _use_progress_bar
    _pytest_config = config

    if config.option.verbose > 0:
        global _show_params, _show_error_details
        _show_params = True
        _show_error_details = True

    # Check for command-line option to override progress bar behavior
    if hasattr(config.option, "no_progress_bar") and config.option.no_progress_bar:
        _use_progress_bar = False

    # Initialize progress bar if not in CI environment
    if _use_progress_bar:
        _current_progress = Progress(
            SpinnerColumn(),
            TextColumn("[bold blue]{task.description}"),
            BarColumn(),
            TextColumn("[bold]{task.completed}/{task.total}"),
            TextColumn("[green]{task.fields[passed]} passed"),
            TextColumn("[red]{task.fields[failed]} failed"),
            TextColumn("[yellow]{task.fields[skipped]} skipped"),
            TextColumn("[cyan]{task.elapsed:.2f}s"),
            console=console,
            expand=True,
        )
        _current_progress.start()


def pytest_addoption(parser):
    """Add custom command line options."""
    parser.addoption(
        "--no-progress-bar",
        action="store_true",
        default=False,
        help="Disable progress bar regardless of environment",
    )


def pytest_collection_modifyitems(config: Config, items: List[Item]) -> None:
    """Pytest hook to initialize progress bar with collected test count."""
    global _test_progress_task, _current_progress, _collected_items_count

    # Store the original count of collected items
    _collected_items_count = len(items)

    if _current_progress and _use_progress_bar:
        _test_progress_task = _current_progress.add_task(
            "Running tests", total=_collected_items_count, passed=0, failed=0, skipped=0
        )

    for item in items:
        if "gpu" in item.keywords:
            if "gpu_test_sync_cuda" not in item.fixturenames:  # type: ignore[attr-defined]
                item.fixturenames.append("gpu_test_sync_cuda")  # type: ignore[attr-defined]


def pytest_deselected(items):
    """Pytest hook for tracking deselected items."""
    global stats
    stats.tests_deselected += len(items)


def extract_parameters(nodeid: str) -> str:
    """Extract parameter info from test nodeid."""
    match = PARAM_PATTERN.search(nodeid)
    if match:
        return match.group(1)
    return ""


def test_category_style(nodeid: str) -> str:
    """Determine style based on test category."""
    if "unit" in nodeid:
        return "unit"
    elif "integration" in nodeid:
        return "integration"
    elif "performance" in nodeid:
        return "performance"
    elif "correctness" in nodeid:
        return "correctness"
    else:
        return ""


def get_formatted_test_name(report: TestReport) -> str:
    """Format test nodeid with parameters if available."""
    if not _show_params:
        return report.nodeid

    params = extract_parameters(report.nodeid)
    category = test_category_style(report.nodeid)

    if params:
        return f"[{category}]{report.nodeid.split('[')[0]}[/{category}] [bold]({params})[/bold]"
    else:
        return f"[{category}]{report.nodeid}[/{category}]"


def update_progress(outcome: str) -> None:
    """Update the progress bar counters."""
    global _current_progress, _test_progress_task, _first_test_seen, stats

    if not _use_progress_bar or not _current_progress or _test_progress_task is None:
        return

    # On first test, adjust progress bar total to account for deselected tests
    if not _first_test_seen:
        _first_test_seen = True
        if stats.tests_deselected > 0:
            new_total = _collected_items_count - stats.tests_deselected
            _current_progress.update(_test_progress_task, total=new_total)

    # Update outcome counters based on the outcome
    if outcome == "passed":
        current_passed = _current_progress.tasks[_test_progress_task].fields["passed"]
        _current_progress.update(
            _test_progress_task, advance=1, passed=current_passed + 1
        )
    elif outcome == "failed":
        current_failed = _current_progress.tasks[_test_progress_task].fields["failed"]
        _current_progress.update(
            _test_progress_task, advance=1, failed=current_failed + 1
        )
    elif outcome == "skipped":
        current_skipped = _current_progress.tasks[_test_progress_task].fields["skipped"]
        _current_progress.update(
            _test_progress_task, advance=1, skipped=current_skipped + 1
        )


def pytest_runtest_logreport(report: TestReport) -> None:
    """
    Hook to process test reports and update progress bar and statistics.

    Args:
        report (TestReport): The pytest test report containing phase and outcome info.
    """
    if not _pytest_config:
        raise RuntimeError("pytest_configure was not called")

    # Handle test outcomes during the "setup" phase
    if report.when == "setup":
        if report.outcome == "skipped":
            # Test skipped during setup (e.g., via skipif or fixture)
            stats.tests_skipped += 1
            stats.tests_executed += 1
            update_progress("skipped")
            skip_reason = (
                report.longrepr[2]
                if hasattr(report, "longrepr") and isinstance(report.longrepr, tuple)
                else ""
            )
            console.print(
                f"[skip]s {get_formatted_test_name(report)} {skip_reason}[/skip]"
            )
        elif report.outcome == "failed":
            # Test failed during setup (e.g., fixture failure)
            stats.tests_failed += 1
            stats.tests_executed += 1
            update_progress("failed")
            console.print(
                f"[failure]✘ {get_formatted_test_name(report)} (setup failed)[/failure]"
            )
            if _show_error_details and hasattr(report, "longrepr") and report.longrepr:
                console.print(
                    Panel(str(report.longrepr), title="Setup Error", border_style="red")
                )

    # Handle test outcomes during the "call" phase
    elif report.when == "call":
        stats.tests_executed += 1
        if report.outcome == "passed":
            # Test passed successfully
            stats.tests_passed += 1
            update_progress("passed")
            console.print(f"[success]✔ {get_formatted_test_name(report)}[/success]")
        elif report.outcome == "failed":
            # Test failed during execution
            stats.tests_failed += 1
            update_progress("failed")
            console.print(f"[failure]✘ {get_formatted_test_name(report)}[/failure]")
            if _show_error_details and hasattr(report, "longrepr") and report.longrepr:
                console.print(
                    Panel(
                        str(report.longrepr), title="Error Details", border_style="red"
                    )
                )
        elif report.outcome == "skipped":
            # Test skipped during call (e.g., via pytest.skip())
            stats.tests_skipped += 1
            update_progress("skipped")
            skip_reason = (
                report.longrepr[2]
                if hasattr(report, "longrepr") and isinstance(report.longrepr, tuple)
                else ""
            )
            console.print(
                f"[skip]s {get_formatted_test_name(report)} {skip_reason}[/skip]"
            )

    # Record test duration for statistics (only in "call" phase)
    if report.when == "call" and hasattr(report, "duration"):
        stats.record_test_duration(get_formatted_test_name(report), report.duration)


def pytest_report_teststatus(
    report: TestReport,
) -> Tuple[str, str, Tuple[str, Dict[str, bool]]]:
    """Pytest hook to customize test status characters."""
    if report.when == "call":
        if report.outcome == "passed":
            return "pass", "✔", ("success", {"bold": True})
        elif report.outcome == "failed":
            return "fail", "✘", ("failure", {"bold": True})
        elif report.outcome == "skipped":
            return "skipped", "s", ("skip", {"bold": True})
    return "", "", ("", {})  # default return for other phases


def print_failed_test_details(failed_reports: List[TestReport]) -> None:
    """Print detailed information for failed tests."""
    console.print("\n[failure]Failed Tests Details:[/failure]")

    for i, report in enumerate(failed_reports, 1):
        console.print(f"\n[failure]{i}. {get_formatted_test_name(report)}[/failure]")

        if hasattr(report, "duration"):
            console.print(f"   Duration: {report.duration:.2f}s")

        if hasattr(report, "longrepr") and report.longrepr:
            if isinstance(report.longrepr, str):
                console.print(
                    Panel(report.longrepr, title="Error Details", border_style="red")
                )
            else:
                console.print(
                    Panel(
                        str(report.longrepr),
                        title="Error Details",
                        border_style="red",
                    )
                )


def pytest_terminal_summary(terminalreporter) -> None:
    """Pytest hook to add customized terminal summary report."""
    global _current_progress

    # Stop the progress bar
    if _use_progress_bar and _current_progress:
        _current_progress.stop()

    markexpr = terminalreporter.config.option.markexpr
    stats.update_duration()

    console.rule(f"[title]Report for mark '{markexpr}' start[/title]")

    passed_reports: List[TestReport] = terminalreporter.stats.get("passed", [])
    failed_reports: List[TestReport] = terminalreporter.stats.get("failed", [])
    skipped_reports: List[TestReport] = terminalreporter.stats.get("skipped", [])

    # Create summary table
    table = Table(title="Test Summary")
    table.add_column("Metric", style="bold")
    table.add_column("Value")

    table.add_row("Total tests", str(stats.tests_executed))
    table.add_row("Passed", f"[success]{stats.tests_passed}[/success]")
    table.add_row("Failed", f"[failure]{stats.tests_failed}[/failure]")
    table.add_row("Skipped", f"[skip]{stats.tests_skipped}[/skip]")
    table.add_row(
        "Deselected", f"{stats.tests_deselected}"
    )  # Add deselected tests to summary
    table.add_row("Total duration", f"{stats.total_duration:.2f}s")

    console.print(table)

    # Show slowest tests
    if stats.slowest_tests:
        slow_table = Table(title="Slowest Tests")
        slow_table.add_column("Test", style="bold")
        slow_table.add_column("Duration (s)")

        for test, duration in stats.slowest_tests[:5]:  # Show top 5 slowest
            slow_table.add_row(test, f"{duration:.2f}")

        console.print(slow_table)

    # detailed list of test results
    if len(failed_reports) > 0:
        print_failed_test_details(failed_reports)

    # List of failed tests (short version)
    if len(failed_reports) > 0:
        console.print("\n[failure]Failed Tests:[/failure]")
        for report in failed_reports:
            console.print(f"  [failure]✘ {get_formatted_test_name(report)}[/failure]")

    if len(passed_reports) > 0:
        console.print("\n[success]Passed Tests:[/success]")
        for report in passed_reports:
            console.print(f"  [success]✔ {get_formatted_test_name(report)}[/success]")

    if len(skipped_reports) > 0:
        console.print("\n[skip]Skipped Tests:[/skip]")
        for report in skipped_reports:
            skip_reason = (
                report.longrepr[2]
                if hasattr(report, "longrepr") and isinstance(report.longrepr, tuple)
                else ""
            )
            console.print(
                f"  [skip]s {get_formatted_test_name(report)} {skip_reason}[/skip]"
            )

    if markexpr:
        console.rule(f"[title]Report for mark '{markexpr}' end[/title]")
    else:
        console.rule("[title]Regression report end[/title]")
