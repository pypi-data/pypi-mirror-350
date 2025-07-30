import numpy as np
import pandas as pd

from vajra._native.metrics_store import (
    Metric,
)
from vajra._native.metrics_store.datastores import (
    UnlabeledCdfDataStore as UnlabeledCdfDataStoreC,
)

from ..datastores.abstract_datastore import AbstractDataStore
from ..datastores.base_cdf_datastore import BaseCDFDataStore

SKETCH_RELATIVE_ACCURACY = 0.001
SKETCH_NUM_QUANTILES_IN_DF = 101


class UnlabeledCDFDataStore(BaseCDFDataStore):

    def __init__(
        self,
        metric: Metric,
        plot_dir: str,
        store_png: bool = False,
    ) -> None:
        super().__init__(metric, plot_dir, store_png)

        assert not metric.requires_label

        # Use the native C++ implementation
        self._native_handle = UnlabeledCdfDataStoreC(
            relative_accuracy=SKETCH_RELATIVE_ACCURACY
        )

    @property
    def native_handle(self) -> UnlabeledCdfDataStoreC:
        return self._native_handle

    def sum(self) -> float:
        return self._native_handle.sum()

    def __len__(self):
        return int(self._native_handle.count())

    def merge(self, other: AbstractDataStore) -> None:
        assert isinstance(other, UnlabeledCDFDataStore)
        assert self == other

        self._native_handle.merge(other.native_handle)

    def put(self, label: str, value: float) -> None:
        self._native_handle.put(value)

    def to_series(self) -> pd.Series:
        # Check if sketch is empty
        if self._native_handle.count() == 0:
            # Return an empty series to avoid potential issues
            return pd.Series(name=self.metric.name)

        # get quantiles at 1% intervals
        quantiles = np.linspace(0, 1, num=SKETCH_NUM_QUANTILES_IN_DF)
        # get quantile values
        quantile_values = [self._native_handle.get_quantile_value(q) for q in quantiles]
        # create dataframe
        series = pd.Series(quantile_values, name=self.metric.name)

        series *= self.value_multiplier

        return series

    def to_df(self) -> pd.DataFrame:
        return self.to_series().to_frame()

    def reset(self) -> None:
        self._native_handle.reset()
