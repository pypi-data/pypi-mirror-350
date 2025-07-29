from dataclasses import field
from typing import Optional

from vajra._native.configs import ModelConfig as ModelConfig_C
from vajra.config.parallel_config import ParallelConfig
from vajra.transformers_utils.config import get_config
from vajra.utils.dataclasses import frozen_dataclass
from vajra.utils.hf_utils import get_and_verify_dtype, get_and_verify_max_len


@frozen_dataclass
class ModelConfig:
    model: str = field(
        default="meta-llama/Meta-Llama-3-8B-Instruct",
        metadata={"help": "Name or path of the huggingface model to use."},
    )
    trust_remote_code: bool = field(
        default=True,
        metadata={
            "help": "Trust remote code (e.g., from HuggingFace) when downloading the model and tokenizer."
        },
    )
    download_dir: Optional[str] = field(
        default=None,
        metadata={
            "help": "Directory to download and load the weights, default to the default cache directory of huggingface."
        },
    )
    load_format: str = field(
        default="auto",
        metadata={
            "help": "The format of the model weights to load: 'auto', 'pt', 'safetensors', 'npcache', or 'dummy'."
        },
    )
    dtype: str = field(
        default="float16",
        metadata={
            "help": "Data type for model weights and activations. 'auto' will use FP16 for FP32 and FP16 models, and BF16 for BF16 models."
        },
    )
    seed: int = field(default=0, metadata={"help": "Random seed for reproducibility."})
    revision: Optional[str] = field(
        default=None,
        metadata={
            "help": "The specific model version to use. Can be a branch name, tag name, or commit id."
        },
    )
    max_model_len: int = field(
        default=-1,
        metadata={
            "help": "Maximum length of a sequence (including prompt and output). If None, will be derived from the model."
        },
    )
    override_num_layers: Optional[int] = field(
        default=None,
        metadata={
            "help": "Override the number of layers in the model. If None, will be derived from the model."
        },
    )

    def update_native_handle(self) -> None:
        self.native_handle = ModelConfig_C(
            self.model,
            self.trust_remote_code,
            self.download_dir,
            self.load_format,
            self.dtype,
            self.seed,
            self.revision,
            self.max_model_len,
            self.get_total_num_layers(),
        )

    def __post_init__(self):
        self._verify_load_format()

        self.hf_config = get_config(self.model, self.trust_remote_code, self.revision)

        if self.override_num_layers is not None:
            self.hf_config.num_hidden_layers = self.override_num_layers

        self.torch_dtype = get_and_verify_dtype(self.hf_config, self.dtype)
        self.hf_config.dtype = self.torch_dtype
        self.max_model_len = get_and_verify_max_len(self.hf_config, self.max_model_len)
        self.native_handle = ModelConfig_C(
            self.model,
            self.trust_remote_code,
            self.download_dir,
            self.load_format,
            self.dtype,
            self.seed,
            self.revision,
            self.max_model_len,
            self.get_total_num_layers(),
            self.get_total_num_q_heads(),
            self.get_total_num_kv_heads(),
            self.get_hidden_size(),
        )

    def _verify_load_format(self) -> None:
        load_format = self.load_format.lower()
        if load_format not in ["auto", "pt", "safetensors", "npcache", "dummy"]:
            raise ValueError(
                f"Unknown load format: {self.load_format}. Must be one of "
                "'auto', 'pt', 'safetensors', 'npcache', or 'dummy'."
            )
        self.load_format = load_format

    def verify_with_parallel_config(
        self,
        parallel_config: ParallelConfig,
    ) -> None:
        total_num_attention_heads = self.hf_config.num_attention_heads
        tensor_parallel_size = parallel_config.tensor_parallel_size
        if total_num_attention_heads % tensor_parallel_size != 0:
            raise ValueError(
                f"Total number of attention heads ({total_num_attention_heads})"
                " must be divisible by tensor parallel size "
                f"({tensor_parallel_size})."
            )

        total_num_hidden_layers = self.hf_config.num_hidden_layers
        pipeline_parallel_size = parallel_config.pipeline_parallel_size
        if total_num_hidden_layers % pipeline_parallel_size != 0:
            raise ValueError(
                f"Total number of hidden layers ({total_num_hidden_layers}) "
                "must be divisible by pipeline parallel size "
                f"({pipeline_parallel_size})."
            )

    def get_total_num_q_heads(self) -> int:
        return self.hf_config.num_attention_heads

    def get_total_num_kv_heads(self) -> int:
        if getattr(self.hf_config, "num_key_value_heads", None) is not None:
            return self.hf_config.num_key_value_heads
        return self.hf_config.num_attention_heads

    def get_hidden_size(self) -> int:
        return self.hf_config.hidden_size

    def get_head_size(self) -> int:
        # NOTE(Amey): This may not be true for all models.
        return self.hf_config.hidden_size // self.hf_config.num_attention_heads

    def get_num_kv_heads(self, parallel_config: ParallelConfig) -> int:
        # NOTE(Amey): This may not be true for all models.
        if getattr(self.hf_config, "num_key_value_heads", None) is not None:
            return (
                self.hf_config.num_key_value_heads
                // parallel_config.tensor_parallel_size
            )
        total_num_attention_heads = self.hf_config.num_attention_heads
        return total_num_attention_heads // parallel_config.tensor_parallel_size

    def get_num_q_heads(self, parallel_config: ParallelConfig) -> int:
        if getattr(self.hf_config, "num_attention_heads", None) is not None:
            return (
                self.hf_config.num_attention_heads
                // parallel_config.tensor_parallel_size
            )
        raise ValueError("num_attention_heads is not defined in the model config")

    def get_num_layers(self, parallel_config: ParallelConfig) -> int:
        total_num_hidden_layers = self.hf_config.num_hidden_layers
        return total_num_hidden_layers // parallel_config.pipeline_parallel_size

    def get_total_num_layers(self) -> int:
        return self.hf_config.num_hidden_layers
