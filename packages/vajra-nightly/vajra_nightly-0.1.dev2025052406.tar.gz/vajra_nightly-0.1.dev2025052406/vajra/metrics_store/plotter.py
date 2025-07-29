import logging
from functools import reduce
from typing import TYPE_CHECKING, Dict, List

import pandas as pd
import plotly_express as px
import wandb
from rich.table import Table

from vajra._native.metrics_store import (
    ComparisonGroupType,
    EntityAssociationType,
    MetricType,
)
from vajra.config.utils import to_snake_case
from vajra.utils.logging_utils import log_table

if TYPE_CHECKING:
    from .datastores.base_cdf_datastore import BaseCDFDataStore

logger = logging.getLogger(__name__)


class Plotter:
    @staticmethod
    def print_stats_table(datastores: List["BaseCDFDataStore"]) -> None:
        if len(datastores) == 0:
            return

        table = Table(title="Metrics Stats Summary")
        table.add_column("Metric", style="cyan", no_wrap=True)
        table.add_column("Min", style="green")
        table.add_column("Max", style="red")
        table.add_column("Mean", style="blue")
        table.add_column("Median", style="magenta")
        table.add_column("P95", style="yellow")
        table.add_column("P99", style="dark_orange3")
        table.add_column("P99.9", style="purple")

        for datastore in datastores:
            metric_name = datastore.metric.name
            metric_unit = datastore.metric.unit
            metric_unit_name = metric_unit.name
            data_series = datastore.to_series()

            table.add_row(
                f"{metric_name} ({metric_unit_name})",
                f"{data_series.min():.3f}",
                f"{data_series.max():.3f}",
                f"{data_series.mean():.3f}",
                f"{data_series.median():.3f}",
                f"{data_series.quantile(0.95):.3f}",
                f"{data_series.quantile(0.99):.3f}",
                f"{data_series.quantile(0.999):.3f}",
            )

            if wandb.run:
                wandb_summary = {
                    f"{metric_name}_min": data_series.min(),
                    f"{metric_name}_max": data_series.max(),
                    f"{metric_name}_mean": data_series.mean(),
                    f"{metric_name}_median": data_series.median(),
                    f"{metric_name}_p95": data_series.quantile(0.95),
                    f"{metric_name}_p99": data_series.quantile(0.99),
                    f"{metric_name}_p99.9": data_series.quantile(0.999),
                }
                wandb.log(wandb_summary, step=0)

        log_table(table)

    @staticmethod
    def plot_cdf(
        data_series: pd.Series,
        metric_name: str,
        metric_unit: str,
        plot_dir: str,
        store_png: bool,
    ) -> None:
        if len(data_series) == 0:
            return

        # rename the series and create a df
        df = data_series.to_frame(metric_name)
        df["cdf"] = df[metric_name].rank(method="first", pct=True)
        # sort the df by cdf
        df = df.sort_values(by="cdf")

        metric_file_name = f"{to_snake_case(metric_name)}_cdf"
        df.to_csv(f"{plot_dir}/{metric_file_name}.csv", index=False)

        if store_png:
            fig = px.line(
                df, x=metric_name, y="cdf", markers=True, labels={"x": metric_unit}
            )
            fig.update_traces(marker=dict(color="red", size=2))
            fig.write_image(f"{plot_dir}/{metric_file_name}.png")

        if wandb.run:
            wandb_df = df.copy()
            # rename the metric_name column to y_axis_label
            wandb_df = wandb_df.rename(columns={metric_name: metric_unit})

            wandb.log(
                {
                    f"{metric_name}_cdf": wandb.plot.line(
                        wandb.Table(dataframe=wandb_df),
                        "cdf",
                        metric_unit,
                        title=metric_name,
                    )
                },
                step=0,
            )

    @staticmethod
    def plot_histogram(
        data_series: pd.Series,
        metric_name: str,
        metric_unit: str,
        plot_dir: str,
        store_png: bool,
    ) -> None:
        if len(data_series) == 0:
            return

        df: pd.DataFrame = data_series.to_frame(metric_name)
        # wandb histogram is highly inaccurate so we need to generate the histogram
        # ourselves and then use wandb bar chart
        histogram_df = df[metric_name].value_counts(bins=25, sort=False).sort_index()  # type: ignore
        histogram_df = histogram_df.reset_index()
        histogram_df.columns = [metric_unit, "Count"]
        histogram_df[metric_unit] = histogram_df[metric_unit].apply(lambda x: x.mid)
        histogram_df = histogram_df.sort_values(by=[metric_unit])
        # convert to percentage
        histogram_df["Percentage"] = histogram_df["Count"] * 100 / len(df)
        # drop bins with less than 0.1% of the total count
        histogram_df = histogram_df[histogram_df["Percentage"] > 0.1]

        metric_file_name = f"{to_snake_case(metric_name)}_histogram"
        histogram_df.to_csv(f"{plot_dir}/{metric_file_name}.csv", index=False)

        if store_png:
            fig = px.bar(
                histogram_df,
                x=metric_unit,
                y="Percentage",
                labels={"x": metric_unit, "y": "Percentage"},
            )
            fig.write_image(f"{plot_dir}/{metric_file_name}.png")

        if wandb.run:
            wandb.log(
                {
                    f"{metric_name}_histogram": wandb.plot.bar(
                        wandb.Table(dataframe=histogram_df),
                        metric_unit,
                        "Percentage",  # wandb plots are horizontal
                        title=metric_name,
                    )
                },
                step=0,
            )

    @staticmethod
    def plot_time_series(
        df: pd.DataFrame,
        metric_name: str,
        metric_unit: str,
        aggregate_values: bool,
        plot_dir: str,
        store_png: bool,
    ) -> None:

        if len(df) == 0:
            return

        assert metric_name in df.columns
        assert metric_unit in df.columns

        if aggregate_values:
            df[metric_name] = df[metric_name].cumsum()

        # sort the df by the metric_unit
        df = df.sort_values(by=metric_unit)

        metric_file_name = f"{to_snake_case(metric_name)}_time_series"
        # store the csv
        df.to_csv(f"{plot_dir}/{metric_file_name}.csv", index=False)

        if store_png:
            fig = px.line(
                df,
                x=metric_unit,
                y=metric_name,
                markers=True,
                labels={"x": metric_unit, "y": metric_name},
            )
            fig.update_traces(marker=dict(color="red", size=2))
            fig.write_image(f"{plot_dir}/{metric_file_name}.png")

        if wandb.run:
            wandb_df = df.copy()
            # rename the metric_name column to y_axis_label
            wandb_df = wandb_df.rename(columns={metric_name: metric_unit})

            wandb.log(
                {
                    f"{metric_name}_time_series": wandb.plot.line(
                        wandb.Table(dataframe=wandb_df),
                        metric_unit,
                        metric_name,
                        title=metric_name,
                    )
                },
                step=0,
            )

    @staticmethod
    def plot_comparison_bar_chart(
        data: Dict[str, float],
        metric_name: str,
        metric_unit: str,
        plot_dir: str,
        store_png: bool,
    ):
        if len(data) == 0:
            return

        # write the csv
        df = pd.DataFrame(data.items(), columns=[metric_name, metric_unit])  # type: ignore

        metric_file_name = f"{to_snake_case(metric_name)}_comparison"
        df.to_csv(f"{plot_dir}/{metric_file_name}.csv", index=False)

        if store_png:
            fig = px.bar(
                x=list(data.keys()),
                y=list(data.values()),
                labels={"x": metric_name, "y": metric_unit},
            )
            fig.write_image(f"{plot_dir}/{metric_file_name}.png")

        if wandb.run:
            wandb.log(
                {
                    metric_file_name: wandb.plot.bar(
                        wandb.Table(
                            dataframe=pd.DataFrame(
                                data=data.items(), columns=[metric_name, metric_unit]  # type: ignore
                            )
                        ),
                        metric_name,
                        metric_unit,
                        title=metric_file_name,
                    )
                },
                step=0,
            )

    @staticmethod
    def save_joined_data_summary(
        datastores: List["BaseCDFDataStore"],
        join_key: str,
        output_dir: str,
    ):
        dfs = [datastore.to_df() for datastore in datastores]
        assert [df[join_key].is_unique and pd.notnull(df[join_key]) for df in dfs]
        merged_df = reduce(
            lambda left, right: left.merge(right, on=join_key, how="inner"),
            dfs,
        )

        metric_file_name = f"{to_snake_case(join_key)}_summary"
        merged_df.to_csv(f"{output_dir}/{metric_file_name}.csv", index=False)

    @staticmethod
    def store_associated_metrics(
        datastores: Dict[MetricType, "BaseCDFDataStore"], output_dir: str
    ) -> None:
        grouped_metrics: Dict[EntityAssociationType, List["BaseCDFDataStore"]] = {}

        for datastore in datastores.values():
            association_type = datastore.metric.entity_association_group
            if (
                not association_type
                or not datastore.metric.requires_label
                or len(datastore) == 0
            ):
                continue

            if association_type not in grouped_metrics:
                grouped_metrics[association_type] = []

            grouped_metrics[association_type].append(datastore)

        for association_type, grouped_datastores in grouped_metrics.items():
            assert all(
                [
                    d.metric.label_type
                    and d.metric.label_type.name == association_type.name
                    for d in grouped_datastores
                ]
            )

            Plotter.save_joined_data_summary(
                grouped_datastores,
                association_type.name,
                output_dir,
            )

    @staticmethod
    def store_comparison_metrics(
        datastores: Dict[MetricType, "BaseCDFDataStore"], plot_dir: str, store_png: bool
    ) -> None:
        grouped_metrics: Dict[ComparisonGroupType, List["BaseCDFDataStore"]] = {}

        for datastore in datastores.values():
            comparison_type = datastore.metric.comparison_group
            if not comparison_type:
                continue

            if comparison_type not in grouped_metrics:
                grouped_metrics[comparison_type] = []

            grouped_metrics[comparison_type].append(datastore)

        for comparison_type, grouped_datastores in grouped_metrics.items():
            units_set = {datastore.metric.unit for datastore in grouped_datastores}
            assert len(units_set) == 1, f"Expected one unit, got {units_set}"
            unit = units_set.pop()

            summation_data = {
                metric.metric.name: metric.sum() for metric in grouped_datastores
            }

            Plotter.plot_comparison_bar_chart(
                summation_data,
                comparison_type.name,
                unit.name,
                plot_dir,
                store_png,
            )
