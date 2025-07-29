from unittest.mock import MagicMock, patch

import pytest
import torch
import torch.nn as nn


# Mock the necessary imports and functions
class MockConfig:
    def __init__(
        self,
        num_hidden_layers=24,
        hidden_size=4096,
        num_attention_heads=32,
        num_key_value_heads=32,
    ):
        self.num_hidden_layers = num_hidden_layers
        self.hidden_size = hidden_size
        self.num_attention_heads = num_attention_heads
        self.num_key_value_heads = num_key_value_heads


# Mock parallel state functions
@pytest.fixture
def mock_parallel_state():
    with patch(
        "vajra.model_executor.weight_loader.get_tensor_model_parallel_rank"
    ) as mock_tp_rank, patch(
        "vajra.model_executor.weight_loader.get_tensor_model_parallel_world_size"
    ) as mock_tp_size, patch(
        "vajra.model_executor.weight_loader.get_pipeline_model_parallel_rank"
    ) as mock_pp_rank, patch(
        "vajra.model_executor.weight_loader.get_pipeline_model_parallel_world_size"
    ) as mock_pp_size:

        mock_tp_rank.return_value = 0
        mock_tp_size.return_value = 2
        mock_pp_rank.return_value = 0
        mock_pp_size.return_value = 2

        yield {
            "tp_rank": mock_tp_rank,
            "tp_size": mock_tp_size,
            "pp_rank": mock_pp_rank,
            "pp_size": mock_pp_size,
        }


# Mock weight loading functions
@pytest.fixture
def mock_weight_loader():
    with patch(
        "vajra.model_executor.weight_loader._default_weight_loader"
    ) as mock_loader, patch(
        "vajra.model_executor.weight_loader._load_padded_tensor_parallel_vocab"
    ) as mock_vocab_loader, patch(
        "vajra.model_executor.weight_loader._hf_model_weights_iterator"
    ) as mock_iterator:

        mock_loader.return_value = None
        mock_vocab_loader.return_value = None

        # Create a mock iterator that returns test weights
        def create_mock_weights():
            weights = [
                # Embedding weights
                ("model.embed_tokens.weight", torch.randn(32000, 4096)),
                # Layer weights
                ("model.layers.0.self_attn.q_proj.weight", torch.randn(4096, 4096)),
                ("model.layers.0.self_attn.k_proj.weight", torch.randn(4096, 4096)),
                ("model.layers.0.self_attn.v_proj.weight", torch.randn(4096, 4096)),
                ("model.layers.0.self_attn.o_proj.weight", torch.randn(4096, 4096)),
                ("model.layers.0.mlp.gate_proj.weight", torch.randn(11008, 4096)),
                ("model.layers.0.mlp.up_proj.weight", torch.randn(11008, 4096)),
                ("model.layers.0.mlp.down_proj.weight", torch.randn(4096, 11008)),
                ("model.layers.0.input_layernorm.weight", torch.randn(4096)),
                ("model.layers.0.post_attention_layernorm.weight", torch.randn(4096)),
                # Final layer weights
                ("model.layers.12.self_attn.q_proj.weight", torch.randn(4096, 4096)),
                ("model.layers.12.self_attn.k_proj.weight", torch.randn(4096, 4096)),
                ("model.layers.12.self_attn.v_proj.weight", torch.randn(4096, 4096)),
                # Norm and head weights
                ("model.norm.weight", torch.randn(4096)),
                ("lm_head.weight", torch.randn(32000, 4096)),
            ]
            return iter(weights)

        mock_iterator.return_value = create_mock_weights()

        yield {
            "default_loader": mock_loader,
            "vocab_loader": mock_vocab_loader,
            "iterator": mock_iterator,
        }


# Create a simple model class for testing - renamed to avoid pytest collection
class MockLlamaModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.config = MockConfig()

        # Create model components
        self.embed_tokens = nn.Embedding(32000, 4096)

        # Create layers
        self.layers = nn.ModuleList([self._create_layer() for _ in range(12)])

        self.norm = nn.LayerNorm(4096)
        self.lm_head = nn.Linear(4096, 32000, bias=False)

    def _create_layer(self):
        layer = nn.Module()

        # Attention components
        layer.self_attn = nn.Module()
        layer.self_attn.qkv_proj = nn.Linear(4096, 4096 * 3, bias=False)
        layer.self_attn.o_proj = nn.Linear(4096, 4096, bias=False)

        # MLP components
        layer.mlp = nn.Module()
        layer.mlp.gate_up_proj = nn.Linear(4096, 11008 * 2, bias=False)
        layer.mlp.down_proj = nn.Linear(11008, 4096, bias=False)

        # Layernorms
        layer.input_layernorm = nn.LayerNorm(4096)
        layer.post_attention_layernorm = nn.LayerNorm(4096)

        return layer

    def forward(self, x):
        # Not needed for weight loading tests
        pass


# Import the actual class we're testing
from vajra.model_executor.weight_loader import TransformerAutoWeightsLoader


@pytest.mark.integration
class TestTransformerAutoWeightsLoader:

    @pytest.mark.integration
    @pytest.fixture
    def test_model(self):
        model = MockLlamaModel()

        # Add weight_loader methods to parameters that need them
        for name, param in model.named_parameters():
            if "qkv_proj" in name:
                param.weight_loader = MagicMock()  # type: ignore
            elif "gate_up_proj" in name:
                # No need to mock this as we handle it directly
                pass
            elif "embed_tokens" in name or "lm_head" in name:
                param.weight_loader = MagicMock()  # type: ignore
            elif any(p in name for p in ["o_proj", "down_proj"]):
                param.weight_loader = MagicMock()  # type: ignore
            else:
                # Default parameters don't need special handling
                pass

        return model

    @pytest.mark.integration
    def test_init(self, test_model):
        """Test the initialization of the TransformerAutoWeightsLoader."""
        column_parallel_layers = ["qkv_proj"]
        row_parallel_layers = ["o_proj", "down_proj"]

        loader = TransformerAutoWeightsLoader(
            test_model,
            column_parallel_layers,
            row_parallel_layers,
            skip_prefixes=["rotary_emb"],
        )

        assert loader.config == test_model.config
        assert len(loader.state_dict) > 0
        assert len(loader.named_parameters) > 0
        assert loader._column_parallel_layers == column_parallel_layers
        assert loader._row_parallel_layers == row_parallel_layers
        assert loader.skip_prefixes == ["rotary_emb"]

    @pytest.mark.integration
    def test_should_skip_weight(self, test_model):
        """Test the weight skipping logic."""
        loader = TransformerAutoWeightsLoader(
            test_model,
            column_parallel_layers=["qkv_proj"],
            row_parallel_layers=["o_proj", "down_proj"],
        )

        # Should skip rotary embedding weights
        assert loader._should_skip_weight(
            "model.layers.0.self_attn.rotary_emb.inv_freq", 0, 2
        )

        # Should skip embed_tokens if not in first pipeline stage
        assert loader._should_skip_weight("model.embed_tokens.weight", 1, 2)
        assert not loader._should_skip_weight("model.embed_tokens.weight", 0, 2)

        # Should skip lm_head if not in last pipeline stage
        assert loader._should_skip_weight("lm_head.weight", 0, 2)
        assert not loader._should_skip_weight("lm_head.weight", 1, 2)

        # Should skip model.norm if not in last pipeline stage
        assert loader._should_skip_weight("model.norm.weight", 0, 2)
        assert not loader._should_skip_weight("model.norm.weight", 1, 2)

    @pytest.mark.integration
    @patch("vajra.model_executor.weight_loader._load_padded_tensor_parallel_vocab")
    def test_handle_embed_and_lm_head_weights(self, mock_vocab_loader, test_model):
        """Test handling of embedding and LM head weights."""
        loader = TransformerAutoWeightsLoader(
            test_model,
            column_parallel_layers=["qkv_proj"],
            row_parallel_layers=["o_proj", "down_proj"],
        )

        # Test embed_tokens
        param = test_model.embed_tokens.weight
        loaded_weight = torch.randn(32000, 4096)
        result = loader._handle_embed_and_lm_head_weights(
            "model.embed_tokens.weight", param, loaded_weight, 0
        )
        assert result is True
        mock_vocab_loader.assert_called_once()

        # Reset mock
        mock_vocab_loader.reset_mock()

        # Test lm_head
        param = test_model.lm_head.weight
        result = loader._handle_embed_and_lm_head_weights(
            "lm_head.weight", param, loaded_weight, 0
        )
        assert result is True
        mock_vocab_loader.assert_called_once()

        # Test non-matching param
        result = loader._handle_embed_and_lm_head_weights(
            "model.layers.0.self_attn.q_proj.weight", param, loaded_weight, 0
        )
        assert result is False

    @pytest.mark.integration
    def test_handle_attention_weights(self, test_model):
        """Test handling of attention weights."""
        loader = TransformerAutoWeightsLoader(
            test_model,
            column_parallel_layers=["qkv_proj"],
            row_parallel_layers=["o_proj", "down_proj"],
        )

        # We need to make sure the parameter exists in the model and is properly registered
        # The correct parameter name should be used based on the model structure
        qkv_param_name = "model.layers.0.self_attn.qkv_proj.weight"

        # Add this parameter to the loader's named_parameters dictionary
        loader.named_parameters = {
            qkv_param_name: test_model.layers[0].self_attn.qkv_proj.weight
        }

        # Replace qkv_proj parameter with a mock
        param = test_model.layers[0].self_attn.qkv_proj.weight
        param.weight_loader = MagicMock()

        # Test q_proj
        name = "model.layers.0.self_attn.q_proj.weight"
        loaded_weight = torch.randn(4096, 4096)
        result = loader._handle_attention_weights(name, loaded_weight, 2, 0)
        assert result is True
        param.weight_loader.assert_called_once()

        # Reset mock
        param.weight_loader.reset_mock()

        # Test k_proj
        name = "model.layers.0.self_attn.k_proj.weight"
        result = loader._handle_attention_weights(name, loaded_weight, 2, 0)
        assert result is True
        param.weight_loader.assert_called_once()

        # Reset mock
        param.weight_loader.reset_mock()

        # Test v_proj
        name = "model.layers.0.self_attn.v_proj.weight"
        result = loader._handle_attention_weights(name, loaded_weight, 2, 0)
        assert result is True
        param.weight_loader.assert_called_once()

        # Test non-matching param
        result = loader._handle_attention_weights(
            "model.layers.0.mlp.gate_proj.weight", loaded_weight, 2, 0
        )
        assert result is False

    @pytest.mark.integration
    def test_handle_gate_up_weights(self, test_model):
        """Test handling of gate/up projection weights."""
        loader = TransformerAutoWeightsLoader(
            test_model,
            column_parallel_layers=["qkv_proj"],
            row_parallel_layers=["o_proj", "down_proj"],
        )

        # Create a state dict with the gate_up_proj parameter
        state_dict = {}
        param = torch.randn(11008 * 2, 4096)  # Combined gate_up projection
        state_dict["model.layers.0.mlp.gate_up_proj.weight"] = param

        # Test gate_proj
        name = "model.layers.0.mlp.gate_proj.weight"
        loaded_weight = torch.randn(11008, 4096)
        result = loader._handle_gate_up_weights(name, loaded_weight, state_dict, 0)
        assert result is True

        # Test up_proj
        name = "model.layers.0.mlp.up_proj.weight"
        result = loader._handle_gate_up_weights(name, loaded_weight, state_dict, 0)
        assert result is True

        # Test non-matching param
        result = loader._handle_gate_up_weights(
            "model.layers.0.mlp.down_proj.weight", loaded_weight, state_dict, 0
        )
        assert result is False
