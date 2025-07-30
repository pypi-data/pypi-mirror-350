from abc import abstractmethod

import pandas as pd

from vajra._native.metrics_store import Metric, PlotType
from vajra._native.metrics_store.datastores import BaseCdfDataStore as BaseCdfDataStoreC

from ..datastores.abstract_datastore import AbstractDataStore
from ..plotter import Plotter


class BaseCDFDataStore(AbstractDataStore):
    def __init__(
        self,
        metric: Metric,
        plot_dir: str,
        store_png: bool = False,
    ) -> None:
        super().__init__(metric, plot_dir, store_png)
        assert (
            metric.plot_type == PlotType.CDF or metric.plot_type == PlotType.HISTOGRAM
        )

        self.value_multiplier: float = 1.0

    @property
    @abstractmethod
    def native_handle(self) -> BaseCdfDataStoreC:
        pass

    def set_value_multiplier(self, value_multiplier: float) -> None:
        self.value_multiplier = value_multiplier
        self.native_handle.set_value_multiplier(value_multiplier)

    @abstractmethod
    def to_series(self) -> pd.Series:
        pass

    @abstractmethod
    def reset(self) -> None:
        pass

    @abstractmethod
    def put(self, label: str, value: float) -> None:
        pass

    def plot(self) -> None:
        data_series = self.to_series()

        if self.metric.plot_type == PlotType.CDF:
            Plotter.plot_cdf(
                data_series,
                metric_name=self.metric.name,
                metric_unit=self.metric.unit.name,
                plot_dir=self.plot_dir,
                store_png=self.store_png,
            )
        else:
            Plotter.plot_histogram(
                data_series,
                metric_name=self.metric.name,
                metric_unit=self.metric.unit.name,
                plot_dir=self.plot_dir,
                store_png=self.store_png,
            )
