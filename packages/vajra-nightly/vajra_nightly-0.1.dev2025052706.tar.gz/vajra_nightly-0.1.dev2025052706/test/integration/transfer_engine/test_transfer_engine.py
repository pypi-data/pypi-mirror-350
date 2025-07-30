import ast
import json
import os
import time
from pathlib import Path

import pytest
import torch
import torch.distributed
import yaml
from rich.console import Console

from vajra._native.configs import ReplicaResourceConfig, TransferEngineConfig
from vajra._native.enums import TransferBackendType
from vajra._native.transfer_engine.interface import (
    BaseTransferEngine,
)
from vajra.config import ModelConfig, ParallelConfig

console: Console = Console(
    record=True, force_terminal=True
)  # force_terminal required for GitHub Actions


@pytest.fixture(scope="module")
def write_latency_data_output_txt():
    return False


@pytest.fixture(scope="module")
def model_config():
    model_config = ModelConfig(
        model="meta-llama/Meta-Llama-3-8B", override_num_layers=12
    )
    return model_config


@pytest.fixture(scope="module")
def parallel_config():
    parallel_config = ParallelConfig(
        pipeline_parallel_size=1,
        tensor_parallel_size=1,
        kv_parallel_size=1,
        enable_sequence_pipeline_parallel=False,
        enable_chunked_pipeline_comm_opt=False,
    )
    return parallel_config


@pytest.fixture(scope="module")
def pipeline_parallel_config():
    parallel_config = ParallelConfig(
        pipeline_parallel_size=2,
        tensor_parallel_size=1,
        kv_parallel_size=1,
        enable_sequence_pipeline_parallel=False,
        enable_chunked_pipeline_comm_opt=False,
    )
    return parallel_config


@pytest.fixture(scope="module")
def tp_parallel_config():
    parallel_config = ParallelConfig(
        pipeline_parallel_size=1,
        tensor_parallel_size=2,
        kv_parallel_size=1,
        enable_sequence_pipeline_parallel=False,
        enable_chunked_pipeline_comm_opt=False,
    )
    return parallel_config


def create_replica_resource_config(parallel_config, model_config):
    return ReplicaResourceConfig(
        parallel_config.native_handle, model_config.native_handle
    )


def create_transfer_engine(
    transfer_backend_type, global_rank, replica_resource_mapping, world_group
):
    transfer_engine_config = TransferEngineConfig(
        transfer_backend_type,
        global_rank,
        replica_resource_mapping,
        world_group,
    )
    transfer_engine = BaseTransferEngine.create_from(transfer_engine_config)
    return transfer_engine


def load_test_cases():
    config_path = Path(__file__).parent / "test_spec.yml"
    with open(config_path) as f:
        config = yaml.safe_load(f)

    test_cases = []
    for name, params in config["transfer_engine_tests"].items():
        # Convert string representations to Python objects
        params["send_ranks"] = ast.literal_eval(params["send_ranks"])
        params["recv_ranks"] = ast.literal_eval(params["recv_ranks"])
        if params["send_page_list"] != "all":
            params["send_page_list"] = ast.literal_eval(params["send_page_list"])
            params["recv_page_list"] = ast.literal_eval(params["recv_page_list"])
        params["pp_list"] = ast.literal_eval(params["pp_list"])
        params["tp_list"] = ast.literal_eval(params["tp_list"])

        test_cases.append(
            pytest.param(
                *(params.values()),  # Pass parameters as positional arguments
                id=name,
            )
        )
    return test_cases


def get_rank_times_json_file(tmp_path: Path, rank: int) -> Path:
    return tmp_path / f"test_transfer_engine_rank{rank}_times.json"


def run_transfer_engine_test(
    rank,
    world_size,
    num_replicas,
    send_replica_id,
    recv_replica_id,
    send_ranks,
    recv_ranks,
    send_page_list,
    recv_page_list,
    pp_list,
    tp_list,
    layer_id,
    parallel_config,
    pipeline_parallel_config,
    tp_parallel_config,
    model_config,
    test_embedding_send,
    tmp_path,
):
    os.environ["MASTER_ADDR"] = "localhost"
    os.environ["MASTER_PORT"] = "12355"
    torch.distributed.init_process_group("nccl", rank=rank, world_size=world_size)
    world_group = torch.distributed.group.WORLD

    torch.set_default_dtype(torch.float16)

    replica_resource_mapping = []
    replica_id = -1
    seen_num_gpus = 0
    should_add_mm_replica = test_embedding_send

    for i in range(num_replicas):
        current_parallel_config = parallel_config
        if pp_list[i]:
            current_parallel_config = pipeline_parallel_config
        elif tp_list[i]:
            current_parallel_config = tp_parallel_config
        replica_resource_config = create_replica_resource_config(
            current_parallel_config, model_config
        )

        replica_resource_mapping.append(replica_resource_config)
        seen_num_gpus += current_parallel_config.world_size
        if replica_id == -1 and seen_num_gpus > rank:
            replica_id = i

    transfer_engine = create_transfer_engine(
        TransferBackendType.TORCH, rank, replica_resource_mapping, world_group
    )
    all_pages_test = isinstance(send_page_list, str) and send_page_list == "all"
    num_pages = 8096
    if not all_pages_test:
        assert isinstance(send_page_list, list) and isinstance(
            recv_page_list, list
        ), "If not running all test, provide send and recv page lists"
        num_pages = max(max(send_page_list), max(recv_page_list)) + 1
    page_size = 16
    num_heads = 8
    llama3_head_dim = 128
    gemma_hidden_dim = 3072
    head_dim = llama3_head_dim if not test_embedding_send else gemma_hidden_dim

    device = torch.device(f"cuda:{rank}")

    if all_pages_test:
        send_page_list = range(num_pages)
        recv_page_list = send_page_list

    if not test_embedding_send:
        head_dim = head_dim // 2 if tp_list[replica_id] else head_dim
        send_tensor = torch.zeros((num_pages, 2, page_size, num_heads, head_dim)).to(
            device
        )
        recv_tensor = torch.zeros((num_pages, 2, page_size, num_heads, head_dim)).to(
            device
        )
    else:
        # num pages -> num embedding tokens
        # there is more than one way to send, but just testing this simple way for now
        send_tensor = torch.zeros((1, num_pages, head_dim)).to(device)
        recv_tensor = torch.zeros((1, num_pages, head_dim)).to(device)

    # warmup
    warmup_iters = 3
    while warmup_iters > 0:
        if rank in send_ranks:
            work = transfer_engine.async_send(
                dst_replica_id=recv_replica_id,
                page_tensor=send_tensor,
                page_list=send_page_list,
                layer_id=layer_id,
                send_to_all=test_embedding_send,
            )
            success = work.synchronize()
            assert success

        elif rank in recv_ranks:
            work = transfer_engine.async_recv(
                src_replica_id=send_replica_id,
                page_tensor=recv_tensor,
                page_list=recv_page_list,
                layer_id=layer_id,
                recv_from_single_rank=test_embedding_send,
            )
            success = work.synchronize()
            assert success
        warmup_iters -= 1

    # prepare send inputs
    for i in range(num_pages):
        if test_embedding_send:
            send_tensor[0, i, :] = i
        else:
            send_tensor[i, :] = i

    start_time = 0
    end_time = 0
    torch.distributed.barrier()
    if rank in send_ranks:
        start_time = time.perf_counter()
        work = transfer_engine.async_send(
            dst_replica_id=recv_replica_id,
            page_tensor=send_tensor,
            page_list=send_page_list,
            layer_id=layer_id,
            send_to_all=test_embedding_send,
        )
        success = work.synchronize()
        end_time = time.perf_counter()
        assert success
    elif rank in recv_ranks:
        start_time = time.perf_counter()
        work = transfer_engine.async_recv(
            src_replica_id=send_replica_id,
            page_tensor=recv_tensor,
            page_list=recv_page_list,
            layer_id=layer_id,
            recv_from_single_rank=test_embedding_send,
        )
        success = work.synchronize()
        end_time = time.perf_counter()
        assert success
    page_shape = send_tensor[0].shape
    element_size_bytes = send_tensor.element_size()
    page_size_bytes = torch.prod(torch.tensor(page_shape)) * element_size_bytes
    time_data = {
        "start_time": start_time,
        "end_time": end_time,
        "page_size_in_bytes": page_size_bytes.item(),
        "total_bytes_transfer": page_size_bytes.item()
        * len(send_page_list)
        * len(send_ranks),
        "num_pages_transfer": len(send_page_list),
    }
    with open(get_rank_times_json_file(tmp_path, rank), "w") as f:
        json.dump(time_data, f)

    torch.distributed.barrier()

    send_page_list_tensor = torch.tensor(send_page_list)
    recv_page_list_tensor = torch.tensor(recv_page_list)

    if rank in recv_ranks:
        assert torch.allclose(
            send_tensor[send_page_list_tensor], recv_tensor[recv_page_list_tensor]
        )
    torch.distributed.barrier()
    torch.distributed.destroy_process_group()


@pytest.mark.integration
@pytest.mark.gpu
@pytest.mark.parametrize(
    "world_size, num_replicas, send_replica_id, recv_replica_id, send_ranks, recv_ranks, send_page_list, recv_page_list, pp_list, tp_list, layer_id, test_embedding_send",
    load_test_cases(),
)
@pytest.mark.skip(
    reason="Skipping transfer engine due to sigabrt failures --- see https://github.com/vajra-ai/vajra/issues/248"
)
def test_integration_send_recv(
    world_size,
    num_replicas,
    send_replica_id,
    recv_replica_id,
    send_ranks,
    recv_ranks,
    send_page_list,
    recv_page_list,
    pp_list,
    tp_list,
    layer_id,
    parallel_config,
    pipeline_parallel_config,
    tp_parallel_config,
    model_config,
    test_embedding_send,
    write_latency_data_output_txt,
    tmp_path,
    test_number,
):
    """Tests sends and receives between replicas.
    Parameterize must have correct send and recv rank and send and recv replica ids.
    It is not calculated automatically
    (for the integration test frontend, but the transfer engine does do that)"""
    assert len(send_page_list) == len(
        recv_page_list
    ), "Send and receive page lists must have the same length"

    torch.multiprocessing.spawn(  # type: ignore
        run_transfer_engine_test,
        args=(
            world_size,
            num_replicas,
            send_replica_id,
            recv_replica_id,
            send_ranks,
            recv_ranks,
            send_page_list,
            recv_page_list,
            pp_list,
            tp_list,
            layer_id,
            parallel_config,
            pipeline_parallel_config,
            tp_parallel_config,
            model_config,
            test_embedding_send,
            tmp_path,
        ),
        nprocs=world_size,
        join=True,
    )

    min_start_time = float("inf")
    max_end_time = 0
    total_bytes_transfer = 0
    page_size_in_bytes = 0

    # we just call one of the send rank's latency the transfer engine latency for now
    # it's a bit hard to quantify it exactly
    rank = list(send_ranks)[0]
    times_json_path = get_rank_times_json_file(tmp_path, rank)
    with open(times_json_path, "r") as f:
        time_data = json.load(f)
    start_time = time_data["start_time"]
    end_time = time_data["end_time"]
    min_start_time = min(min_start_time, start_time)
    total_bytes_transfer = time_data["total_bytes_transfer"]
    page_size_in_bytes = time_data["page_size_in_bytes"]
    num_pages_transfer = time_data["num_pages_transfer"]
    max_end_time = max(max_end_time, end_time)
    latency = max_end_time - min_start_time
    latency *= 1000 * 1000  # convert to microseconds
    to_mb = 1024**2

    console.print(
        f"--- Transfer Engine Latency and Data for Test #{test_number} ---",
        style="bold blue underline",
    )
    console.print(f"[b]World Size:[/b] [blue]{world_size}[/blue]")
    console.print(f"[b]Send Ranks:[/b] [red]{send_ranks}[/red]")
    console.print(f"[b]Receive Ranks:[/b] [red]{recv_ranks}[/red]")
    console.print(f"[b]Latency:[/b] [green]{latency:.5f} microseconds[/green]")
    console.print(
        f"[b]Number of Pages Transferred:[/b] [cyan]{num_pages_transfer}[/cyan]"
    )
    console.print(
        f"[b]Page Size:[/b] [yellow]{page_size_in_bytes / to_mb}[/yellow] megabytes"
    )
    console.print(
        f"[b]Total Megabytes Transferred:[/b] [magenta]{total_bytes_transfer / to_mb}[/magenta] megabytes"
    )
    if write_latency_data_output_txt:
        with open("transfer_engine_latency_output.txt", "a") as file:
            file.write(console.export_text())
