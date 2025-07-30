from typing import Optional

from vajra.enums import MetricsStoreType
from vajra.utils.base_registry import BaseRegistry

from .base_metrics_store import BaseMetricsStore
from .engine_metrics_store import EngineMetricsStore
from .worker_metrics_store import WorkerMetricsStore


class MetricsStoreRegistry(BaseRegistry):
    pass


MetricsStoreRegistry.register(MetricsStoreType.ENGINE, EngineMetricsStore)
MetricsStoreRegistry.register(MetricsStoreType.WORKER, WorkerMetricsStore)


class MetricsStoreHandle:
    _instance: Optional["BaseMetricsStore"] = None

    @classmethod
    def get_or_create_instance(
        cls,
        store_type: MetricsStoreType,
        *args,
        **kwargs,
    ) -> "BaseMetricsStore":
        """
        Get the instance of the BaseMetricsStore if it exists, otherwise create a new instance.

        Returns:
            The BaseMetricsStore instance
        """
        cls._instance = MetricsStoreRegistry.get(store_type, *args, **kwargs)
        assert cls._instance is not None
        return cls._instance

    @classmethod
    def get_instance(cls) -> "BaseMetricsStore":
        """
        Get the instance of the BaseMetricsStore.

        Returns:
            The BaseMetricsStore instance
        """
        assert cls._instance is not None, "BaseMetricsStore not initialized"
        return cls._instance
