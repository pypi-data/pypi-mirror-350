from abc import ABC, abstractmethod

import pandas as pd

from vajra._native.metrics_store import Metric


class AbstractDataStore(ABC):
    def __init__(
        self,
        metric: Metric,
        plot_dir: str,
        store_png: bool = False,
    ) -> None:
        self.metric = metric
        self.plot_dir = plot_dir
        self.store_png = store_png

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, AbstractDataStore)
            and self.metric == other.metric
            and self.plot_dir == other.plot_dir
            and self.store_png == other.store_png
        )

    @abstractmethod
    def sum(self) -> float:
        pass

    @abstractmethod
    def merge(self, other: "AbstractDataStore") -> None:
        pass

    @abstractmethod
    def __len__(self) -> int:
        pass

    @abstractmethod
    def put(self, *args, **kwargs) -> None:
        pass

    @abstractmethod
    def to_df(self) -> pd.DataFrame:
        pass

    @abstractmethod
    def plot(self) -> None:
        pass

    def __str__(self) -> str:
        return f"DataStore(metric={self.metric}, plot_dir={self.plot_dir}, store_png={self.store_png})"

    def __repr__(self) -> str:
        return self.__str__()
