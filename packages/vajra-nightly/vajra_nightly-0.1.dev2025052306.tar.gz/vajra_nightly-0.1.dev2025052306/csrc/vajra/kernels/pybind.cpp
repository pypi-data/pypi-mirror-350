#include <torch/extension.h>

#include "commons/Logging.h"
#include "kernels/ops.h"

PYBIND11_MODULE(TORCH_EXTENSION_NAME, m) {
  google::InitGoogleLogging("vajra-kernels");
  vajra::Logger::InitializeLogLevel();
  // Activation ops
  m.def("silu_and_mul", &silu_and_mul, "Activation function used in SwiGLU.");
  m.def("gelu_new", &gelu_new, "GELU implementation used in GPT-2.");
  m.def("gelu_fast", &gelu_fast, "Approximate GELU implementation.");

  // Layernorm
  m.def("rms_norm", &rms_norm,
        "Apply Root Mean Square (RMS) Normalization to the input tensor.");

  // Rotary embedding
  m.def("rotary_embedding", &rotary_embedding,
        "Apply GPT-NeoX or GPT-J style rotary embedding to query and key");

  m.def("topk_softmax", &topk_softmax,
        "Apply topk softmax to the gating outputs.");

  m.def("moe_align_block_size", &moe_align_block_size,
        "Aligning the number of tokens to be processed by each expert such "
        "that it is divisible by the block size.");

  m.def("reshape_and_cache_flashinfer", &reshape_and_cache_flashinfer,
        "Reshape and cache the key and value tensors for FlashInfer.");
}
