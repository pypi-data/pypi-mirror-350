from typing import List, Optional, Tuple

import torch
import torch.distributed

from vajra._native.model_executor import LLMModelRunner as LLMModelRunnerC
from vajra._native.model_executor.layers import Sampler
from vajra.config import LlmReplicaControllerConfig
from vajra.datatypes import (
    SamplerOutputs,
    SamplingParams,
    Sequence,
    SequenceMetadata,
)
from vajra.logger import init_logger
from vajra.metrics_store import CpuTimer, MetricsStoreHandle, MetricType
from vajra.model_executor import get_model, set_random_seed
from vajra.model_executor.base_model_runner import BaseModelRunner
from vajra.model_executor.layers.attention import AttentionWrapper  # type: ignore
from vajra.model_executor.parallel_utils import (
    recv_from_last_pipeline_stage,
    send_to_next_pipeline_stage,
)
from vajra.model_executor.parallel_utils.parallel_state import (
    get_process_group_wrapper,
    is_pipeline_first_stage,
    is_pipeline_last_stage,
)
from vajra.model_executor.utils import (
    pad_to_alignment,
    round_up_to_multiple,
    use_native_backend,
)
from vajra.utils import get_gpu_memory
from vajra.worker.cache_engine import CacheEngine

logger = init_logger(__name__)


class LLMModelRunner(BaseModelRunner):

    def __init__(
        self,
        config: LlmReplicaControllerConfig,
        device: torch.device,
        rank: int,
    ):
        self.config = config
        self.device = device
        self.rank = rank

        AttentionWrapper.initialize_static_args(
            config.model_config.get_num_q_heads(config.parallel_config),
            config.model_config.get_num_kv_heads(config.parallel_config),
            config.model_config.get_head_size(),
            config.cache_config.block_size,
            device,
            config.model_config.torch_dtype,
        )
        self.model = get_model(config)

        self.sampler: Optional[Sampler] = None
        if self.model.lm_head:
            self.sampler = Sampler(
                self.model.lm_head.weight,
                self.model.config.vocab_size,
                get_process_group_wrapper(),
            )

        self.is_pipeline_first_stage = is_pipeline_first_stage()
        self.is_pipeline_last_stage = is_pipeline_last_stage()
        self.send_stream = torch.cuda.Stream(device=self.device)
        self.recv_stream = torch.cuda.Stream(device=self.device)

        self.prepare_inputs_timer = CpuTimer(MetricType.PREPARE_INPUTS, rank=self.rank)
        self.sampler_timer = CpuTimer(MetricType.SAMPLER, rank=self.rank)
        self.model_execution_timer = CpuTimer(
            MetricType.MODEL_EXECUTION, rank=self.rank
        )
        self.attn_begin_forward_timer = CpuTimer(
            MetricType.ATTN_BEGIN_FORWARD, rank=self.rank
        )

        self._use_native_execution_backend = self.model.use_native_execution_backend

        self.native_handle: Optional[LLMModelRunnerC] = None
        if self.use_native_execution_backend:
            self.native_handle = LLMModelRunnerC(
                self.config.native_handle,
                self.device,
                self.rank,
                self.model.native_handle,
                get_process_group_wrapper(),
                MetricsStoreHandle.get_instance().native_handle,
                self.sampler,
            )

    @property
    def use_native_execution_backend(self) -> bool:
        return (
            self._use_native_execution_backend
            and self.model.is_native_execution_backend_supported()
        )

    @use_native_backend
    def _prepare_inputs(
        self,
        seqs: List[Sequence],
        seq_metadata_list: List[SequenceMetadata],
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        input_tokens: List[int] = []
        input_positions: List[int] = []

        for seq, seq_metadata in zip(seqs, seq_metadata_list):
            num_q_tokens = seq_metadata.num_q_tokens
            input_tokens.extend(seq.get_last_n_token_ids(num_q_tokens))

            start_position = seq.get_num_tokens_stage_processed()
            end_position = start_position + num_q_tokens
            input_positions.extend(range(start_position, end_position))

        # Optimization: Pad the input length to be a multiple of 8.
        # This is required for utilizing the Tensor Cores in NVIDIA GPUs.
        input_tokens = pad_to_alignment(input_tokens, multiple_of=8)
        input_positions = pad_to_alignment(input_positions, multiple_of=8)

        # Convert to tensors.
        tokens_tensor = torch.tensor(input_tokens, dtype=torch.long, device=self.device)
        positions_tensor = torch.tensor(
            input_positions, dtype=torch.long, device=self.device
        )

        return tokens_tensor, positions_tensor

    @torch.inference_mode()
    def profile_num_available_blocks(
        self,
        block_size: int,
        gpu_memory_utilization: float,
    ) -> int:
        torch.cuda.set_device(self.device)

        # Profile the memory usage of the model and get the maximum number of
        # cache blocks that can be allocated with the remaining free memory.
        torch.cuda.empty_cache()
        torch.cuda.reset_peak_memory_stats()

        # Enable top-k sampling to reflect the accurate memory usage.
        vocab_size = self.model.config.vocab_size
        sampling_params = SamplingParams(top_p=0.99, top_k=vocab_size - 1)

        seqs: List[Sequence] = []
        seq_metadata_list: List[SequenceMetadata] = []

        # Profile memory usage with a single `chunk_size` chunk
        # which is the last chunk in the longest supported sequence.
        seq_len = int(self.config.model_config.max_model_len)

        chunk_size = int(min(self.config.scheduler_config.max_chunk_size, seq_len))

        seq = Sequence(
            seq_id=str(0),
            prompt="",
            prompt_token_ids=[0] * seq_len,
            block_size=block_size,
            eos_token_id=1,
            arrival_time=0.0,
            sampling_params=sampling_params,
        )
        seq_metadata = SequenceMetadata(
            schedule_id=0,
            seq_id=seq.seq_id,
            num_q_tokens=chunk_size,
            num_kv_tokens=seq_len,
            block_table=[],
            kvp_group_ids=[],
            save_kv_cache=True,
        )
        seqs.append(seq)
        seq_metadata_list.append(seq_metadata)

        input_tokens, input_positions = self._prepare_inputs(seqs, seq_metadata_list)
        AttentionWrapper.get_or_create_thread_local_instance().begin_forward(
            seq_metadata_list
        )

        if not self.is_pipeline_first_stage:
            # hidden_states_shape: num_tokens x hidden_size
            input_tokens = torch.empty(
                (input_positions.shape[0], self.model.config.hidden_size),
                dtype=self.model.config.dtype,
                device=self.device,
            )

        # Execute the model.
        num_layers = self.config.model_config.get_num_layers(
            self.config.parallel_config
        )
        self.model(
            input_positions,
            input_tokens,
            [torch.empty(1)] * num_layers,
        )

        # Calculate the number of blocks that can be allocated with the
        # profiled peak memory.
        torch.cuda.synchronize()
        peak_memory = torch.cuda.max_memory_allocated()
        total_gpu_memory = get_gpu_memory()
        logger.info(
            f"Completed profiling, peak_memory: {peak_memory}, total_gpu_memory: {total_gpu_memory}, gpu_memory_utilization: {gpu_memory_utilization}, block_size: {block_size}"
        )
        cache_block_size = CacheEngine.get_cache_block_size(
            block_size, self.config.model_config, self.config.parallel_config
        )
        num_gpu_blocks = int(
            (total_gpu_memory * gpu_memory_utilization - peak_memory)
            // cache_block_size
        )
        num_gpu_blocks = max(num_gpu_blocks, 0)
        torch.cuda.empty_cache()

        AttentionWrapper.get_or_create_thread_local_instance().end_forward()

        # Reset the seed to ensure that the random state is not affected by
        # the model initialization and profiling.
        set_random_seed(self.config.model_config.seed)
        return num_gpu_blocks

    @use_native_backend
    def run(
        self,
        seqs: List[Sequence],
        seq_metadata_list: List[SequenceMetadata],
        gpu_cache: Optional[List[torch.Tensor]] = None,
    ) -> Optional[SamplerOutputs]:
        if not seq_metadata_list:
            return []

        batch_num_tokens = round_up_to_multiple(
            sum(m.num_q_tokens for m in seq_metadata_list), multiple_of=8
        )

        hidden_states: Optional[torch.Tensor] = None
        if not self.is_pipeline_first_stage:
            with torch.cuda.stream(self.recv_stream):  # type: ignore
                hidden_states = recv_from_last_pipeline_stage(
                    (batch_num_tokens, self.model.config.hidden_size),
                    self.model.config.dtype,
                    self.device,
                    self.config.parallel_config.enable_chunked_pipeline_comm_opt,
                )

        with self.prepare_inputs_timer:
            input_tokens, input_positions = self._prepare_inputs(
                seqs, seq_metadata_list
            )

        if not self.is_pipeline_first_stage:
            input_tensor = hidden_states
        else:
            input_tensor = input_tokens

        with self.attn_begin_forward_timer:
            AttentionWrapper.get_or_create_thread_local_instance().begin_forward(
                seq_metadata_list
            )

        torch.cuda.synchronize()

        with self.model_execution_timer:
            output = self.model(
                input_positions,
                input_tensor,
                gpu_cache,
            )
        torch.cuda.synchronize()

        AttentionWrapper.get_or_create_thread_local_instance().end_forward()

        if self.sampler is not None:
            with self.sampler_timer:
                output = self.sampler(output, seqs, seq_metadata_list)
        else:  # is not last stage
            assert not self.is_pipeline_last_stage
            # Get the communication stream for send operation
            with torch.cuda.stream(self.send_stream):  # type: ignore
                send_to_next_pipeline_stage(
                    output, self.config.parallel_config.enable_chunked_pipeline_comm_opt
                )
                # No need to wait for send to complete - it will happen asynchronously

        return output
