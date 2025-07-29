import pytest
import torch

from vajra._native.transfer_engine.backend import TransferEngineUtils


@pytest.mark.unit
@pytest.mark.parametrize(
    "num_splits, dst_num_pages, block_size, num_heads, head_dim, page_list_input",
    [
        (
            1,
            4096,
            16,
            8,
            128,
            torch.randperm(4096)[: 1024 // 16].sort().values.cpu(),
        ),
        (
            2,
            4096,
            16,
            8,
            128,
            torch.randperm(4096)[: 1024 // 16].sort().values.cpu(),
        ),
        (
            4,
            4096,
            16,
            8,
            128,
            torch.randperm(4096)[: 1024 // 16].sort().values.cpu(),
        ),
        (
            8,
            8192,
            16,
            8,
            128,
            torch.randperm(8192)[: 32 // 16].sort().values.cpu(),
        ),
        (
            8,
            8192,
            16,
            8,
            128,
            torch.randperm(8192)[: 2048 // 16].sort().values.cpu(),
        ),
    ],
)
def test_copy_merge_pages_cache(
    num_splits, dst_num_pages, block_size, num_heads, head_dim, page_list_input
):
    src_device = torch.device("cuda")
    dst_device = torch.device("cuda")
    dtype = torch.float32
    head_dim_per_src = head_dim // (num_splits)

    page_list = page_list_input.tolist()

    src_shape = (len(page_list), 2, block_size, num_heads, head_dim_per_src)
    dst_shape = (
        dst_num_pages,
        2,
        block_size,
        num_heads,
        head_dim,
    )

    src_list = [
        [torch.zeros(src_shape, dtype=dtype, device=src_device).reshape(src_shape)]
        for _ in range(num_splits)
    ]
    for i in range(num_splits):
        src_list[i][0][:] = float(i + 1)

    dst = torch.zeros(dst_shape, dtype=dtype, device=dst_device).reshape(dst_shape)

    TransferEngineUtils.copy_merge_pages_cache(src_list, dst, page_list)

    expected_slices = []
    for i in range(num_splits):
        expected_slices.append(src_list[i][0])
    expected_tensor_full_dst = torch.cat(expected_slices, -1)

    expected = torch.zeros_like(dst)
    for i in range(len(page_list)):
        dst_page_number = page_list[i]
        expected[dst_page_number] = expected_tensor_full_dst[i]

    assert torch.equal(
        dst, expected
    ), f"Test failed for num_splits={num_splits}, dst_num_pages={dst_num_pages}, block_size={block_size}, num_heads={num_heads}, head_dim={head_dim}, page_list={page_list}"
