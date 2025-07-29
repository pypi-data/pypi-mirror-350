from typing import Optional

import pandas as pd

from vajra._native.metrics_store import Metric, PlotType
from vajra._native.metrics_store.datastores import (
    TimeSeriesDataStore as TimeSeriesDataStoreC,
)

from ..datastores.abstract_datastore import AbstractDataStore
from ..plotter import Plotter


class TimeSeriesDataStore(AbstractDataStore):
    def __init__(
        self,
        metric: Metric,
        plot_dir: str,
        store_png: bool = False,
    ) -> None:
        super().__init__(metric, plot_dir, store_png)
        assert metric.plot_type == PlotType.TIME_SERIES
        assert not metric.requires_label

        # Use native handle for time series data storage
        self.native_handle = TimeSeriesDataStoreC()
        self.time_offset: float = 0.0

    def set_time_offset(self, time_offset: float) -> None:
        self.time_offset = time_offset

    def merge(self, other: AbstractDataStore) -> None:
        assert isinstance(other, TimeSeriesDataStore)
        assert self == other

        if len(other) == 0:
            return

        self.native_handle.merge(other.native_handle)

    @property
    def start_time(self) -> Optional[float]:
        return self.native_handle.get_start_time()

    def __len__(self):
        return self.native_handle.size()

    def sum(self) -> float:
        return self.native_handle.sum()

    def put(self, time: float, value: float) -> None:
        self.native_handle.put(time, value)

    def to_df(self) -> pd.DataFrame:
        unit_type_string = self.metric.unit.name
        # Get the data log as a shared pointer and convert to DataFrame
        data_log = self.native_handle.get_data_log()
        df = pd.DataFrame(data_log, columns=[unit_type_string, self.metric.name])  # type: ignore
        df[unit_type_string] = df[unit_type_string] - self.time_offset
        return df

    def plot(self) -> None:
        df = self.to_df()

        Plotter.plot_time_series(
            df,
            self.metric.name,
            self.metric.unit.name,
            self.metric.aggregate_time_series,
            self.plot_dir,
            self.store_png,
        )

    def reset(self) -> None:
        self.time_offset = 0.0
        self.native_handle.reset()
