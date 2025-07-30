import glob
import json
import os
from datetime import datetime
from pathlib import Path
from test.utils.api_client import GitHubAPIClient
from test.utils.config import GitHubCIConfig
from test.utils.data import (
    PerformanceComparisonMetadata,
    PerformanceData,
    PerformanceMetadata,
    PerformanceMetricComparison,
    calculate_quantiles,
)
from test.utils.files import (
    cleanup_output_dir,
    cleanup_zip_file,
    download_zip_file,
    extract_json_from_zip,
    find_performance_artifact,
    load_json_file,
    save_json_file,
)
from test.utils.logging import (
    log_and_print_error,
    log_and_print_info,
    log_and_print_warning,
)
from typing import Any, Dict, List, Optional, Tuple

import pandas as pd
import pytest
import ray
import yaml
from rich.console import Console
from rich.table import Table

from vajra.benchmark.benchmark_runner import BenchmarkRunner
from vajra.benchmark.config import (
    BaseRequestIntervalGeneratorConfig,
    BenchmarkConfig,
    SyntheticRequestGeneratorConfig,
    TraceRequestLengthGeneratorConfig,
)
from vajra.config import (
    FixedChunkReplicaSchedulerConfig,
    InferenceEngineConfig,
    LlmReplicaControllerConfig,
    LlmReplicasetControllerConfig,
    MetricsConfig,
    ModelConfig,
    ParallelConfig,
)
from vajra.config.flat_dataclass import get_config_class_by_type_name
from vajra.logger import init_logger

console: Console = Console(
    force_terminal=True
)  # force_terminal required for GitHub Actions
logger = init_logger(__name__)


@pytest.fixture
def performance_context():
    config = GitHubCIConfig()
    baseline, run_id = fetch_baseline_metrics(config)
    return {"config": config, "baseline": baseline, "most_recent_run_id": run_id}


def load_test_cases() -> List[Tuple[str, Dict[str, Any]]]:
    config_path = Path(__file__).parent / "test_spec.yml"
    with open(config_path) as f:
        config = yaml.safe_load(f)

    test_cases = []
    for name, params in config["performance_tests"].items():
        test_cases.append(
            pytest.param(
                params["model"],
                params["max_model_len"],
                params["pp_size"],
                params["tp_size"],
                params["enable_spp"],
                params["enable_ep"],
                params["dataset"],
                params["request_pattern"],
                params["qps"],
                id=name,
            )
        )
    return test_cases


def fetch_baseline_metrics(
    config: GitHubCIConfig,
) -> tuple[Optional[Dict], Optional[int]]:
    """
    Fetches baseline performance metrics from the most recent successful workflow run.

    Args:
        config: CI configuration class.

    Returns:
        Tuple of (baseline_metrics, most_recent_run_id). Both are None if fetching fails.
    """
    baseline_metrics = None
    most_recent_run_id = None
    api_client = GitHubAPIClient(
        config.github_token, config.repo_owner, config.repo_name
    )

    try:
        workflow_data = api_client.get_workflow_runs(
            config.workflow_filename, config.baseline_branch
        )
        if not workflow_data["total_count"]:
            log_and_print_warning(
                "No workflow runs found for baseline branch. Skipping performance comparison."
            )
            return None, None

        for workflow in workflow_data["workflow_runs"]:
            if workflow["name"] == config.workflow_name:
                most_recent_run_id = workflow["id"]
                break

        if not most_recent_run_id:
            log_and_print_warning(
                f"No successful workflow runs with name '{config.workflow_name}' found for baseline."
            )
            return None, None

        log_and_print_info(f"Baseline workflow run ID: {most_recent_run_id}")
        artifacts_data = api_client.get_artifacts_for_run(most_recent_run_id)
        found_artifact = find_performance_artifact(
            artifacts_data, most_recent_run_id, config.performance_artifact_prefix
        )

        if found_artifact:
            artifact_zip_path = download_zip_file(
                api_client,
                found_artifact["id"],
                config.output_dir,
                found_artifact["name"],
            )
            prev_json_files = extract_json_from_zip(
                artifact_zip_path, config.output_dir
            )
            cleanup_zip_file(artifact_zip_path)

            if prev_json_files:
                prev_json_path = prev_json_files[0]
                baseline_metrics = load_json_file(prev_json_path)
                log_and_print_info("Baseline metrics loaded.")
            else:
                log_and_print_warning("No JSON file found in baseline artifact.")
        else:
            log_and_print_info("No baseline performance artifact found.")
    except Exception as e:
        console.print_exception(show_locals=True)
        log_and_print_error(f"Error fetching baseline metrics: {e}")
        baseline_metrics = None
        most_recent_run_id = None

    return baseline_metrics, most_recent_run_id


def run_perf_test_benchmark(
    model: str,
    max_model_len: int,
    pp_size: int,
    tp_size: int,
    enable_spp: bool,
    enable_ep: bool,
    dataset: str,
    request_pattern: str,
    benchmark_output_dir: str,
    test_output_dir: str,
    qps: int,
    config: GitHubCIConfig,
) -> None:
    """
    Configures and runs a single performance test.

    Args:
        model: The name of the model.
        max_model_len: The maximum model length.
        pp_size: The pipeline parallel size.
        tp_size: The tensor parallel size.
        enable_spp: Whether to enable sequence pipeline parallelism or not.
        enable_ep: Whether to enable expert parallelism (when applicable) or not.
        dataset: The dataset to use.
        request_pattern: The request pattern to use.
        benchmark_output_dir: Directory for benchmark output.
        test_output_dir: Directory for test output.
        qps: Queries per second.
        config: CI configuration class
    """

    model_config = ModelConfig(model=model, max_model_len=max_model_len)
    parallel_config = ParallelConfig(
        pipeline_parallel_size=pp_size,
        tensor_parallel_size=tp_size,
        enable_sequence_pipeline_parallel=enable_spp,
        enable_expert_parallel=enable_ep,
    )

    request_length_generator_config = TraceRequestLengthGeneratorConfig(
        trace_file=f"data/processed_traces/{dataset}.csv"
    )

    request_interval_generator_config = get_config_class_by_type_name(
        BaseRequestIntervalGeneratorConfig,
        request_pattern,
    )(**{"qps": qps})

    request_generator_config = SyntheticRequestGeneratorConfig(
        length_generator_config=request_length_generator_config,
        interval_generator_config=request_interval_generator_config,
    )

    scheduler_config = FixedChunkReplicaSchedulerConfig(
        max_batch_size=128, chunk_size=512
    )

    metrics_config = MetricsConfig(
        write_metrics=True,
        enable_chrome_trace=True,
        output_dir=f"{benchmark_output_dir}/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S-%f')}",
    )

    llm_replica_controller_config = LlmReplicaControllerConfig(
        model_config=model_config,
        parallel_config=parallel_config,
        scheduler_config=scheduler_config,
    )
    controller_config = LlmReplicasetControllerConfig(
        replica_controller_config=llm_replica_controller_config,
    )
    inference_engine_config = InferenceEngineConfig(
        controller_config=controller_config,
        metrics_config=metrics_config,
    )

    benchmark_config = BenchmarkConfig(
        log_level="error",
        inference_engine_config=inference_engine_config,
        request_generator_config=request_generator_config,
    )

    benchmark_runner = BenchmarkRunner(benchmark_config)
    benchmark_runner.run()

    key = f"{model.replace('/', '-')}_pp{pp_size}_tp{tp_size}_spp{enable_spp}_{dataset}_{request_pattern}_{qps}qps"
    if enable_ep:
        key += f"_ep{enable_ep}"

    perf_json_path = os.path.join(
        test_output_dir, f"perf_results_{os.getenv('GITHUB_RUN_ID', 'dev')}.json"
    )

    perf_data = _build_perf_data(benchmark_output_dir)
    _update_json_file(perf_json_path, key, perf_data, config)
    cleanup_output_dir(benchmark_output_dir)
    ray.shutdown()


def compare_and_report(
    baseline_metrics: Optional[Dict],
    new_metrics_path: str,
    config: GitHubCIConfig,
    most_recent_run_id: Optional[int],
) -> None:
    """
    Compares new metrics with baseline metrics and fails the test if a regression is detected.

    Args:
        baseline_metrics: Metrics from the baseline run.
        new_metrics_path: Path to the JSON file with new metrics.
        config: CI configuration class.
        most_recent_run_id: ID of the baseline workflow run.
    """
    try:
        new_metrics = load_json_file(new_metrics_path)
        log_and_print_info("Loaded new metrics for comparison.")

        if baseline_metrics:
            comparison_results_data = compare_metrics(
                baseline_metrics, new_metrics, config.regression_threshold_pct
            )
            perf_regression = report_performance_comparison(
                comparison_results_data, config.regression_threshold_pct, config
            )

            comparison_results = {
                model_name: {
                    metric_name: metrics.__dict__
                    for metric_name, metrics in model_comparison.items()
                }
                for model_name, model_comparison in comparison_results_data.items()
            }
            metadata = create_comparison_metadata(config, most_recent_run_id)
            comparison_output = {"results": comparison_results, "metadata": metadata}
            save_comparison_results(
                comparison_output=comparison_output,
                output_dir=config.output_dir,
                run_id=config.run_id,
                filename_prefix=config.comparison_result_prefix,
            )

            if perf_regression:
                if not config.overwrite_baseline:
                    pytest.fail(
                        "Performance regression detected in one or more metrics. Check output for details."
                    )
                else:
                    log_and_print_warning(
                        "Performance regression detected, but overwriting baseline."
                    )
        else:
            if not config.overwrite_baseline:
                log_and_print_error("No baseline metrics available for comparison.")
                pytest.fail(
                    f"Could not find baseline metrics for workflow '{config.workflow_name}' in branch '{config.baseline_branch}'."
                )
            else:
                log_and_print_info(
                    "No baseline metrics found, but saving current run as a new baseline."
                )
    except Exception as e:
        console.print_exception(show_locals=True)
        log_and_print_error(f"Error during performance comparison: {e}")
        pytest.fail("Error during performance comparison.")


@pytest.mark.gpu
@pytest.mark.performance
@pytest.mark.parametrize(
    "model, max_model_len, pp_size, tp_size, enable_spp, enable_ep, dataset, request_pattern, qps",
    load_test_cases(),
)
def test_perf_benchmark(
    performance_context: Dict[str, Any],
    model: str,
    max_model_len: int,
    pp_size: int,
    tp_size: int,
    enable_spp: bool,
    enable_ep: bool,
    dataset: str,
    request_pattern: str,
    qps: int,
) -> None:
    """
    Runs parameterized performance benchmarks, saves results, and checks for regressions.
    Fails if either the benchmark run fails or a regression is detected.
    """
    config = performance_context["config"]
    baseline_metrics = performance_context["baseline"]
    most_recent_run_id = performance_context["most_recent_run_id"]
    benchmark_output_dir = os.path.join(os.getcwd(), "benchmark_output")
    test_output_dir = config.output_dir

    try:
        run_perf_test_benchmark(
            model,
            max_model_len,
            pp_size,
            tp_size,
            enable_spp,
            enable_ep,
            dataset,
            request_pattern,
            benchmark_output_dir,
            test_output_dir,
            qps,
            config,
        )
    except Exception as e:
        console.print_exception(show_locals=True)
        log_and_print_error(f"Performance benchmark run error: {e}")
        pytest.fail(
            f"Performance benchmark run failed for parameters: model={model}, max_model_len={max_model_len}, pp_size={pp_size}, tp_size={tp_size}, dataset={dataset}, request_pattern={request_pattern}"
        )

    # regression check
    new_metrics_path = os.path.join(
        test_output_dir, f"perf_results_{config.run_id}.json"
    )
    compare_and_report(baseline_metrics, new_metrics_path, config, most_recent_run_id)


def _build_perf_data(benchmark_output_dir: str) -> PerformanceData:
    """
    Builds performance data from benchmark output and updates a JSON file.

    Args:
        benchmark_output_dir: The directory containing benchmark output.
    """

    metrics = {
        "ttft": "prefill_e2e_time",
        "tbt": "decode_token_execution_plus_preemption_time",
    }

    perf_data_dict = {}
    try:
        # assumption: 1 replica and 1 benchmark output
        csv_main_path = glob.glob(f"{benchmark_output_dir}/*/plots")[0]
        for prefix, metric_name in metrics.items():
            csv_path = f"{csv_main_path}/{metric_name}_cdf.csv"
            df = pd.read_csv(csv_path)
            perf_data_dict.update(calculate_quantiles(df, metric_name, prefix))
    except (FileNotFoundError, IndexError) as e:
        console.print_exception(show_locals=True)
        raise RuntimeError(f"Error processing benchmark output: {e}") from e

    return PerformanceData(**perf_data_dict)


def compare_metrics(
    prev_metrics: Dict[str, Dict[str, float]],
    new_metrics: Dict[str, Dict[str, float]],
    threshold_pct: int,
) -> Dict[str, Dict[str, PerformanceMetricComparison]]:
    """
    Compares two sets of performance metrics and identifies regressions.
    """
    comparison_results = {}
    for model, new_data in new_metrics.items():
        if model == "metadata":
            continue
        prev_data = PerformanceData(**prev_metrics.get(model, {}))
        new_data = PerformanceData(**new_data)
        comparison = {}
        for metric in new_data.get_metric_names():
            prev_value = getattr(prev_data, metric)
            new_value = getattr(new_data, metric)
            if prev_value is not None:
                diff_ms = new_value - prev_value
                regression_flag = diff_ms > (threshold_pct / 100) * prev_value
                comparison[metric] = PerformanceMetricComparison(
                    regression=regression_flag,
                    diff_ms=diff_ms,
                    diff_pct=100 * (diff_ms / prev_value),
                    prev_value=prev_value,
                    new_value=new_value,
                )
            else:
                comparison[metric] = PerformanceMetricComparison(
                    regression=None,
                    diff_ms=None,
                    diff_pct=None,
                    prev_value=None,
                    new_value=new_value,
                )
        comparison_results[model] = comparison
    return comparison_results


def save_comparison_results(
    comparison_output: Dict[str, Any],
    output_dir: str,
    run_id: str | int,
    filename_prefix: str,
) -> None:
    """
    Saves the comparison results to a JSON file using utility function.
    """
    save_json_file(comparison_output, output_dir, f"{filename_prefix}_{run_id}.json")


def create_comparison_metadata(
    config: GitHubCIConfig, baseline_run_id: int | None
) -> Dict[str, Any]:
    """
    Creates metadata for the comparison report.
    """
    metadata = PerformanceComparisonMetadata(
        regression_threshold_pct=config.regression_threshold_pct,
        date=datetime.now().isoformat(),
        workflow_run_id=config.run_id,
        baseline_run_id=baseline_run_id,
        commit_sha=config.github_sha,
    )
    return metadata.__dict__


def _update_json_file(
    json_path: str, key: str, new_data: PerformanceData, config: GitHubCIConfig
) -> None:
    """Updates or creates a JSON file with new performance data."""

    json_dir = os.path.dirname(json_path)
    os.makedirs(json_dir, exist_ok=True)

    try:
        with open(json_path, "r") as f:
            existing_data: Dict[str, Any] = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        existing_data = {}

    existing_data[key] = new_data.to_dict()

    if (
        "metadata" not in existing_data
    ):  # minimal metadata just for run context if needed
        existing_data["metadata"] = PerformanceMetadata(
            date=datetime.now().isoformat(),
            workflow_run_id=config.run_id,
            commit_sha=config.github_sha,
        ).__dict__

    with open(json_path, "w") as f:
        json.dump(existing_data, f, indent=2, separators=(",", ": "))


def report_performance_comparison(
    comparison_results_data: Dict, regression_threshold_pct: int, config: GitHubCIConfig
) -> bool:
    """Displays performance comparison results in a formatted table.

    returns:
        bool: True if any regressions were detected, False otherwise.
    """

    console.rule("[bold magenta]Performance regression summary[/bold magenta]")

    perf_regression = False
    if comparison_results_data:
        for model_name, model_comparison in comparison_results_data.items():
            model_regressed = False
            table = Table(title=f"[bold blue]{model_name}[/bold blue]")
            table.add_column("Metric", style="cyan")
            table.add_column("Previous value", style="magenta")
            table.add_column("New value", style="green")
            table.add_column("Diff (ms)", style="yellow")
            table.add_column("Diff (%)", style="red")
            table.add_column("Regression", style="bold")

            for metric_name, metric_comparison in model_comparison.items():
                prev_str = (
                    f"{metric_comparison.prev_value:.6f}"
                    if metric_comparison.prev_value is not None
                    else "N/A"
                )
                new_str = (
                    f"{metric_comparison.new_value:.6f}"
                    if metric_comparison.new_value is not None
                    else "N/A"
                )
                diff_ms_str = (
                    f"{metric_comparison.diff_ms:.6f}"
                    if metric_comparison.diff_ms is not None
                    else "N/A"
                )

                if metric_comparison.diff_pct is not None:
                    diff_pct_style = (
                        "[green]"
                        if metric_comparison.diff_pct <= regression_threshold_pct
                        else "[red]"
                    )
                    diff_pct_str = f"{diff_pct_style}{metric_comparison.diff_pct:.2f}%{diff_pct_style}"
                else:
                    diff_pct_str = "N/A"

                if metric_comparison.regression is not None:
                    regression_status = (
                        "[bold red]YES[/bold red]"
                        if metric_comparison.regression
                        else "[green]NO[/green]"
                    )
                    regression_flag = metric_comparison.regression
                else:
                    regression_status = "N/A"
                    regression_flag = False  # only for logic, console shows N/A

                table.add_row(
                    metric_name,
                    prev_str,
                    new_str,
                    diff_ms_str,
                    diff_pct_str,
                    regression_status,
                )
                if regression_flag:
                    perf_regression = True

            console.print(table)

        if perf_regression:
            console.print("[bold red]Performance regression detected![/bold red]")
        elif not config.overwrite_baseline:
            console.print("[green]No performance regression detected.[/green]")
        else:
            console.print("[green]Overwriting baseline with new values.[/green]")
    return perf_regression
