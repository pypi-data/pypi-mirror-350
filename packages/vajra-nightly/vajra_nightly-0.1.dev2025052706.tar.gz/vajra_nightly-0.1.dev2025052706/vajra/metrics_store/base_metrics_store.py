import os
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Type

from vajra._native.metrics_store import BaseMetricsStore as BaseMetricsStoreC
from vajra._native.metrics_store import (
    ChromeTracer,
    Metric,
    MetricType,
    PlotType,
    get_all_metrics,
)
from vajra.config import MetricsConfig
from vajra.logger import init_logger

from .datastores.base_cdf_datastore import BaseCDFDataStore
from .datastores.datastore_factory import DataStoreFactory
from .datastores.time_series_datastore import TimeSeriesDataStore

logger = init_logger(__name__)


def if_write_metrics(func):

    def wrapper(self, *args, **kwargs):
        if self.config.write_metrics:
            return func(self, *args, **kwargs)

    return wrapper


def check_enabled(func):

    def wrapper(self, *args, **kwargs):
        if self.disabled:
            return
        return func(self, *args, **kwargs)

    return wrapper


class BaseMetricsStore(ABC):
    _instance: Optional["BaseMetricsStore"] = None

    def __init__(
        self,
        config: MetricsConfig,
    ):
        self.config = config
        self.plots_dir = f"{self.config.output_dir}/plots/"
        os.makedirs(self.plots_dir, exist_ok=True)

        self.disabled = False
        self.metrics: Dict[MetricType, Metric] = get_all_metrics(
            self.config.write_metrics,
            self.config.keep_individual_batch_metrics,
            self.config.enable_gpu_op_level_metrics,
            self.config.enable_cpu_op_level_metrics,
        )
        self.cdf_metrics = [
            metric
            for metric in self.metrics
            if metric.plot_type == PlotType.CDF
            or metric.plot_type == PlotType.HISTOGRAM
        ]
        self.time_series_metrics = [
            metric
            for metric in self.metrics
            if metric.plot_type == PlotType.TIME_SERIES
        ]

        self.chrome_tracer = ChromeTracer(self.config.output_dir)
        self.cdf_datastores: Dict[MetricType, BaseCDFDataStore] = {  # type: ignore
            metric.type: DataStoreFactory.get_cdf_datastore(
                metric, self.plots_dir, self.config.store_png
            )
            for metric in self.cdf_metrics
        }
        self.time_series_datastores: Dict[MetricType, TimeSeriesDataStore] = {  # type: ignore
            metric.type: DataStoreFactory.get_time_series_datastore(
                metric, self.plots_dir, self.config.store_png
            )
            for metric in self.time_series_metrics
        }
        self._native_handle = self._create_native_handle()

    @abstractmethod
    def _get_native_handle_impl(self) -> Type[BaseMetricsStoreC]:
        pass

    def _create_native_handle(self) -> BaseMetricsStoreC:
        return self._get_native_handle_impl()(
            self.config.native_handle,
            {
                metric: datastore.native_handle
                for metric, datastore in self.cdf_datastores.items()
            },
            {
                metric: datastore.native_handle
                for metric, datastore in self.time_series_datastores.items()
            },
            self.chrome_tracer,
            *self._get_native_handle_extra_args(),
        )

    @abstractmethod
    def _get_native_handle_extra_args(self) -> List:
        pass

    @property
    @abstractmethod
    def native_handle(self) -> BaseMetricsStoreC:
        pass

    @check_enabled
    def reset(self):

        # Reset the cdf datastores
        for datastore in self.cdf_datastores.values():
            datastore.reset()

        # Reset the time series datastores
        for datastore in self.time_series_datastores.values():
            datastore.reset()

        # Reset the chrome tracer
        self.chrome_tracer.reset()

        # Reset the native handle
        self.native_handle.reset()

    @check_enabled
    @if_write_metrics
    def push_cpu_operation_metric(
        self,
        metric_type: MetricType,
        time: float,
    ):
        self.native_handle.push_cpu_operation_metric(metric_type, time)

    @abstractmethod
    def is_operation_enabled(
        self,
        metric_type: MetricType,
        **kwargs,
    ) -> bool:
        """
        Check if the operation is enabled for the given metric type.
        """
        raise NotImplementedError
