import pytest
import torch

from vajra.model_executor.layers.activation import SiluAndMul  # type: ignore
from vajra.model_executor.layers.fused_moe import fused_moe

NUM_EXPERTS = [8, 64]
TOP_KS = [2, 6]


@pytest.mark.gpu
@pytest.mark.unit
@pytest.mark.parametrize("m", [1, 33, 64, 222, 1024 * 128])
@pytest.mark.parametrize("n", [128, 1024, 2048])
@pytest.mark.parametrize("k", [128, 511, 1024])
@pytest.mark.parametrize("e", NUM_EXPERTS)
@pytest.mark.parametrize("topk", TOP_KS)
@pytest.mark.parametrize("dtype", [torch.float16, torch.bfloat16])
def test_fused_moe(
    m: int,
    n: int,
    k: int,
    e: int,
    topk: int,
    dtype: torch.dtype,
):
    a = torch.randn((m, k), device="cuda", dtype=dtype) / 10
    w1 = torch.randn((e, 2 * n, k), device="cuda", dtype=dtype) / 10
    w2 = torch.randn((e, k, n), device="cuda", dtype=dtype) / 10

    score = torch.randn((m, e), device="cuda", dtype=dtype)
    triton_output = fused_moe(a, w1, w2, score, topk, renormalize=False)
    torch_output = torch_moe(a, w1, w2, score, topk)
    torch.testing.assert_close(triton_output, torch_output, atol=2e-2, rtol=0)


def torch_moe(a, w1, w2, score, topk):
    B, D = a.shape
    a = a.view(B, -1, D).repeat(1, topk, 1).reshape(-1, D)
    out = torch.zeros(B * topk, w2.shape[1], dtype=a.dtype, device=a.device)
    score = torch.softmax(score, dim=-1, dtype=torch.float32)
    topk_weight, topk_ids = torch.topk(score, topk)
    topk_weight = topk_weight.view(-1)
    topk_ids = topk_ids.view(-1)
    for i in range(w1.shape[0]):
        mask = topk_ids == i
        if mask.sum():
            out[mask] = SiluAndMul()(a[mask] @ w1[i].transpose(0, 1)) @ w2[i].transpose(
                0, 1
            )
    return (
        out.view(B, -1, w2.shape[1]) * topk_weight.view(B, -1, 1).to(out.dtype)
    ).sum(dim=1)
