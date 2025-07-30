from dataclasses import dataclass, fields
from typing import Dict, Optional

import pandas as pd


def calculate_quantiles(
    df: pd.DataFrame, column: str, prefix: str
) -> Dict[str, float | pd.Series]:
    """Calculates the p50 and p90 quantiles for a given column in a DataFrame."""
    return {
        f"{prefix}_p50": df[column].quantile(0.5),
        f"{prefix}_p90": df[column].quantile(0.9),
    }


@dataclass(frozen=True)
class PerformanceData:
    """Performance data available."""

    ttft_p50: Optional[float] = None
    ttft_p90: Optional[float] = None
    tbt_p50: Optional[float] = None
    tbt_p90: Optional[float] = None

    perf_schema_version: float = 0.0

    @classmethod
    def get_metric_names(cls):
        """Returns the field names of PerformanceData for iteration."""
        return [
            field.name for field in fields(cls) if field.name != "perf_schema_version"
        ]

    def to_dict(self):
        return {
            metric_name: getattr(self, metric_name)
            for metric_name in self.get_metric_names()
        }


@dataclass(frozen=True)
class PerformanceMetricComparison:
    """
    Represents the comparison result for a single metric.
    """

    regression: Optional[bool]
    diff_ms: Optional[float]
    diff_pct: Optional[float]
    prev_value: Optional[float]
    new_value: Optional[float]


@dataclass(frozen=True)
class PerformanceComparisonMetadata:
    """Metadata for performance comparison reports."""

    regression_threshold_pct: Optional[float] = None
    date: Optional[str] = None  # ISO format
    workflow_run_id: Optional[int | str] = None
    baseline_run_id: Optional[int | str] = None
    commit_sha: Optional[str] = None
    perf_schema_version: float = PerformanceData.perf_schema_version


@dataclass(frozen=True)
class PerformanceMetadata:
    """Metadata for performance testing results."""

    date: Optional[str] = None  # ISO format
    workflow_run_id: Optional[int | str] = None
    commit_sha: Optional[str] = None

    perf_schema_version: float = PerformanceData.perf_schema_version
