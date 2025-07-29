from typing import List, Type

import wandb

from vajra._native.metrics_store import (
    EngineMetricsStore as EngineMetricsStoreC,  # Add import for the native class
)
from vajra._native.metrics_store import (
    MetricType,
    get_completion_time_series_metrics_types,
)
from vajra.config import MetricsConfig
from vajra.datatypes import SchedulerOutput, Sequence
from vajra.logger import init_logger

from .base_metrics_store import BaseMetricsStore, check_enabled, if_write_metrics
from .plotter import Plotter

logger = init_logger(__name__)


class EngineMetricsStore(BaseMetricsStore):
    def __init__(
        self,
        config: MetricsConfig,
    ):
        super().__init__(config)
        self._init_wandb()

    def _get_native_handle_impl(self) -> Type[EngineMetricsStoreC]:
        return EngineMetricsStoreC

    @property
    def native_handle(self) -> EngineMetricsStoreC:
        return self._native_handle

    def is_operation_enabled(
        self,
        metric_type: MetricType,
        **kwargs,
    ) -> bool:
        return self.native_handle.is_operation_enabled(metric_type)

    def _init_wandb(self):
        if (
            not self.config.write_metrics
            or not self.config.wandb_project
            or not self.config.wandb_group
        ):
            return

        logger.info(
            f"Initializing wandb with project: {self.config.wandb_project}, group: {self.config.wandb_group}, run_name: {self.config.wandb_run_name}"
            f", sweep_id: {self.config.wandb_sweep_id}, run_id: {self.config.wandb_run_id}"
        )
        if self.config.wandb_sweep_id or self.config.wandb_run_id:
            logger.warning("wandb_sweep_id and wandb_run_id are not supported yet.")

        wandb.init(
            project=self.config.wandb_project,
            group=self.config.wandb_group,
            name=self.config.wandb_run_name,
        )

    @check_enabled
    @if_write_metrics
    def on_request_arrival(self, seq_id: str, arrival_time: float) -> None:
        self.native_handle.on_request_arrival(seq_id, arrival_time)

    @if_write_metrics
    def _on_request_end(self, seq: Sequence) -> None:
        self.native_handle.on_request_end(seq)

    def _get_native_handle_extra_args(self) -> List:
        return []

    @check_enabled
    @if_write_metrics
    def on_schedule(
        self,
        replica_id: int,
        scheduler_output: SchedulerOutput,
        start_time: float,
        end_time: float,
    ) -> None:
        self.native_handle.on_schedule(
            replica_id, scheduler_output, start_time, end_time
        )

    @check_enabled
    @if_write_metrics
    def on_batch_end(
        self,
        seqs: List[Sequence],
        scheduler_output: SchedulerOutput,
        batch_start_time: float,
        batch_end_time: float,
    ) -> None:
        self.native_handle.on_batch_end(
            seqs, scheduler_output, batch_start_time, batch_end_time
        )

    @check_enabled
    @if_write_metrics
    def plot(self) -> None:
        # Keep plotting functionality in Python
        # Get the start time from the REQUEST_ARRIVED time series metric
        start_time = self.time_series_datastores[MetricType.REQUEST_ARRIVED].start_time
        if start_time is None:
            logger.warning("No metrics to plot")
            return

        # Set time offset for all time series datastores
        for metric_type in get_completion_time_series_metrics_types():
            if metric_type in self.time_series_datastores:
                self.time_series_datastores[metric_type].set_time_offset(start_time)

        # print stats table
        Plotter.print_stats_table(list(self.cdf_datastores.values()))

        # Plot time series metrics
        for datastore in self.time_series_datastores.values():
            datastore.plot()

        # Plot CDF metrics
        for datastore in self.cdf_datastores.values():
            datastore.plot()

        # Store associated and comparison metrics
        Plotter.store_associated_metrics(self.cdf_datastores, self.config.output_dir)
        Plotter.store_comparison_metrics(
            self.cdf_datastores, self.plots_dir, self.config.store_png
        )

        self.chrome_tracer.store()

    @check_enabled
    @if_write_metrics
    def merge(self, other: BaseMetricsStore) -> None:
        # Merge time series datastores
        for metric_type, datastore in self.time_series_datastores.items():
            if metric_type in other.time_series_datastores:
                datastore.merge(other.time_series_datastores[metric_type])

        # Merge CDF datastores
        for metric_type, datastore in self.cdf_datastores.items():
            if metric_type in other.cdf_datastores:
                datastore.merge(other.cdf_datastores[metric_type])

        self.chrome_tracer.merge(other.chrome_tracer)
