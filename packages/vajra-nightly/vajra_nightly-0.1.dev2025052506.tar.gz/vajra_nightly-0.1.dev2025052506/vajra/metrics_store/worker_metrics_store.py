from typing import List, Optional, Type

import torch

from vajra._native.metrics_store import (
    MetricType,
)
from vajra._native.metrics_store import WorkerMetricsStore as WorkerMetricsStoreC
from vajra._native.metrics_store import (
    get_gpu_operation_metrics_types,
)
from vajra.config import MetricsConfig
from vajra.datatypes import SchedulerOutput, SequenceMetadata
from vajra.logger import init_logger

from .base_metrics_store import BaseMetricsStore, check_enabled, if_write_metrics
from .datastores.base_cdf_datastore import BaseCDFDataStore

logger = init_logger(__name__)


PROFILE_LAYER_ID = 1


class WorkerMetricsStore(BaseMetricsStore):
    def __init__(
        self,
        config: MetricsConfig,
        model_num_layers: int,
        rank: int,
    ):
        self.model_num_layers = model_num_layers
        self.rank = rank
        super().__init__(config)

    def _get_native_handle_impl(self) -> Type[WorkerMetricsStoreC]:
        return WorkerMetricsStoreC

    def _get_native_handle_extra_args(self) -> List:
        return [self.rank]

    @property
    def native_handle(self) -> WorkerMetricsStoreC:
        return self._native_handle

    @check_enabled
    def reset(self):
        super().reset()

        gpu_op_metrics_types = get_gpu_operation_metrics_types()
        for metric_type in gpu_op_metrics_types:
            if not metric_type in self.cdf_datastores:
                continue
            datastore = self.cdf_datastores[metric_type]
            assert isinstance(datastore, BaseCDFDataStore)
            datastore.set_value_multiplier(self.model_num_layers)

        self.native_handle.reset()

    def is_operation_enabled(
        self,
        metric_type: MetricType,
        layer_id: Optional[int] = None,
        **kwargs,
    ) -> bool:
        return self.native_handle.is_operation_enabled(metric_type, layer_id)

    @check_enabled
    @if_write_metrics
    def on_batch_stage_start(
        self,
        scheduler_output: SchedulerOutput,
    ):
        self.native_handle.on_batch_stage_start(scheduler_output)

    @check_enabled
    @if_write_metrics
    def on_batch_stage_end(
        self,
        replica_id: int,
        seq_metadata_list: List[SequenceMetadata],
        tensor_parallel_rank: int,
        pipeline_parallel_rank: int,
        kv_parallel_rank: int,
        start_time: float,
        end_time: float,
    ) -> None:

        self.native_handle.on_batch_stage_end(
            replica_id,
            seq_metadata_list,
            tensor_parallel_rank,
            pipeline_parallel_rank,
            kv_parallel_rank,
            start_time,
            end_time,
        )

    @check_enabled
    @if_write_metrics
    def push_operation_metric_cuda_events(
        self,
        metric_type: MetricType,
        start_event: torch.cuda.Event,
        end_event: torch.cuda.Event,
    ):

        self.native_handle.push_operation_metric_cuda_events(
            metric_type, start_event, end_event
        )

    @check_enabled
    @if_write_metrics
    def push_gpu_operation_metric(
        self,
        metric_type: MetricType,
        time: float,
    ):
        self.native_handle.push_gpu_operation_metric(metric_type, time)

    def __getstate__(self):
        """Custom serialization method to exclude native handle.

        This method is called when pickling the object. It returns a dict of attributes
        that will be pickled, excluding the native handle which cannot be serialized.
        """
        state = self.__dict__.copy()
        # Remove the native handle from the state
        if "_native_handle" in state:
            del state["_native_handle"]
        return state

    def __setstate__(self, state):
        """Custom deserialization method to recreate native handle.

        This method is called when unpickling the object. It restores the object's state
        and recreates the native handle.
        """
        self.__dict__.update(state)
        # Recreate the native handle
        self._native_handle = self._create_native_handle()
