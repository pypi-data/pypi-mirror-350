import logging

import pandas as pd

from vajra._native.metrics_store import Metric
from vajra._native.metrics_store.datastores import (
    LabeledCdfDataStore as LabeledCdfDataStoreC,
)

from ..datastores.abstract_datastore import AbstractDataStore
from ..datastores.base_cdf_datastore import BaseCDFDataStore

logger = logging.getLogger(__name__)


class LabeledCDFDataStore(BaseCDFDataStore):

    def __init__(
        self,
        metric: Metric,
        plot_dir: str,
        store_png: bool = False,
    ) -> None:
        super().__init__(metric, plot_dir, store_png)
        assert metric.requires_label
        assert metric.label_type is not None

        # Create the native handle for efficient data storage and operations
        self._native_handle = LabeledCdfDataStoreC()

    @property
    def native_handle(self) -> LabeledCdfDataStoreC:
        return self._native_handle

    def merge(self, other: AbstractDataStore):
        assert isinstance(other, LabeledCDFDataStore)
        assert self == other, f"Cannot merge {other.metric} into {self.metric}"

        if len(other) == 0:
            return

        # Use the native handle to merge
        self.native_handle.merge(other.native_handle)

    def sum(self) -> float:
        # Use the native handle to compute the sum
        return self.native_handle.sum()

    def __len__(self) -> int:
        # Use the native handle to get the size
        return self.native_handle.size()

    def put(self, label: str, value: float) -> None:
        # Use the native handle to add data
        self.native_handle.put(label, value)

    def to_df(self):
        assert self.metric.label_type is not None

        # Get the data from the native handle
        self.native_handle.dedupe_and_normalize()
        data_log = self.native_handle.get_data_log()

        # Create a DataFrame with the data
        label_type_string = self.metric.label_type.name
        df = pd.DataFrame(data_log, columns=[label_type_string, self.metric.name])  # type: ignore

        # make sure that there are no duplicates
        assert df[label_type_string].is_unique

        df[self.metric.name] *= self.value_multiplier
        df[label_type_string] = df[label_type_string].astype(str)

        return df

    def to_series(self) -> pd.Series:
        df = self.to_df()
        return df[self.metric.name]  # type: ignore

    def reset(self) -> None:
        self.native_handle.reset()
