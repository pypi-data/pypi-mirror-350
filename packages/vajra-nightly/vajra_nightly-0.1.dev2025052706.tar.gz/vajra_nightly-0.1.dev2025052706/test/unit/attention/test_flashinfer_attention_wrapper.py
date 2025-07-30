from typing import Any, Dict, List

import pytest
import torch

from vajra.datatypes import SequenceMetadata
from vajra.model_executor.layers.attention import FlashinferAttentionWrapper


def create_sequence_metadata(
    seq_id: str,
    num_q_tokens: int,
    num_kv_tokens: int,
    block_table: List[int],
    save_kv_cache: bool = True,
    kvp_group_ids: List[int] = [0],
) -> SequenceMetadata:
    """Helper function to create a sequence metadata object for testing."""
    metadata = SequenceMetadata(
        0,
        seq_id,
        num_q_tokens,
        num_kv_tokens,
        block_table,
        kvp_group_ids,
        save_kv_cache,
    )

    return metadata


@pytest.mark.unit
class TestFlashinferAttentionWrapper:
    @pytest.fixture
    def setup_wrapper(self) -> Dict[str, Any]:
        """Setup the wrapper for testing."""
        # Parameters
        num_q_heads = 8
        num_kv_heads = 8
        head_dim = 64
        block_size = 4
        device = torch.device("cuda")

        # Create wrapper for testing
        wrapper = FlashinferAttentionWrapper(
            num_q_heads=num_q_heads,
            num_kv_heads=num_kv_heads,
            head_dim=head_dim,
            block_size=block_size,
            device=device,
        )

        return {
            "wrapper": wrapper,
            "device": device,
        }

    def test_initialization(self, setup_wrapper: Dict[str, Any]):
        """Test that the wrapper initializes correctly."""
        wrapper = setup_wrapper["wrapper"]

        # Check initial state
        assert wrapper.is_metadata_initialized is False
        assert wrapper.is_no_op is False
        assert wrapper.should_save_kv_cache is False
        assert wrapper.num_q_tokens == 0

    def test_empty_sequence_list(self, setup_wrapper: Dict[str, Any]):
        """Test behavior with an empty sequence list."""
        wrapper = setup_wrapper["wrapper"]

        # Process empty sequence list
        wrapper.begin_forward([])

        # Check state after processing
        assert wrapper.is_metadata_initialized is True
        assert wrapper.is_no_op is True
        assert wrapper.num_q_tokens == 0

    def test_single_sequence(self, setup_wrapper: Dict[str, Any]):
        """Test behavior with a single sequence."""
        wrapper = setup_wrapper["wrapper"]
        device = setup_wrapper["device"]

        # Create a single sequence
        seq_metadata = create_sequence_metadata("test_seq", 4, 8, [0, 1, 2, 3], True)

        # Process the sequence
        wrapper.begin_forward([seq_metadata])

        # Check state after processing
        assert wrapper.is_no_op is False
        assert wrapper.num_q_tokens == 4
        assert wrapper.should_save_kv_cache is True

        # Check that slot_mapping_tensor is created with the correct size
        assert wrapper.slot_mapping_tensor is not None
        assert wrapper.slot_mapping_tensor.size(0) == 4

        # Check that slot_mapping_tensor is correct
        expected_slot_mapping_tensor = torch.tensor(
            [8, 9, 10, 11], dtype=torch.int64, device=device
        )
        assert torch.equal(wrapper.slot_mapping_tensor, expected_slot_mapping_tensor)

    def test_multiple_sequences(self, setup_wrapper: Dict[str, Any]):
        """Test behavior with multiple sequences."""
        wrapper = setup_wrapper["wrapper"]
        device = setup_wrapper["device"]

        # Create multiple sequences
        seq_metadata1 = create_sequence_metadata("test_seq1", 4, 8, [0, 1, 2, 3], True)
        seq_metadata2 = create_sequence_metadata("test_seq2", 2, 12, [4, 5, 6, 7], True)

        # Process the sequences
        wrapper.begin_forward([seq_metadata1, seq_metadata2])

        # Check state after processing
        assert wrapper.is_no_op is False
        assert wrapper.num_q_tokens == 6
        assert wrapper.should_save_kv_cache is True

        # Check that slot_mapping_tensor is created with the correct size
        assert wrapper.slot_mapping_tensor is not None
        assert wrapper.slot_mapping_tensor.size(0) == 6

        # Check that slot_mapping_tensor is correct
        expected_slot_mapping_tensor = torch.tensor(
            [8, 9, 10, 11, 28, 29], dtype=torch.int64, device=device
        )
        assert torch.equal(wrapper.slot_mapping_tensor, expected_slot_mapping_tensor)

    def test_no_save_kv_cache(self, setup_wrapper: Dict[str, Any]):
        """Test behavior when not saving KV cache."""
        wrapper = setup_wrapper["wrapper"]

        # Create sequences that don't save KV cache
        seq_metadata1 = create_sequence_metadata(
            "test_seq1", 4, 8, [0, 1, 2, 3], False, [0, 1]
        )
        seq_metadata2 = create_sequence_metadata(
            "test_seq2", 2, 12, [4, 5, 6, 7], False, [0, 1]
        )

        # Process the sequences
        wrapper.begin_forward([seq_metadata1, seq_metadata2])

        # Check state after processing
        assert wrapper.num_q_tokens == 6
        assert wrapper.should_save_kv_cache is False

        # slot_mapping_tensor should not be created when not saving KV cache
        assert (
            not hasattr(wrapper, "slot_mapping_tensor")
            or wrapper.slot_mapping_tensor is None
        )

    def test_end_forward(self, setup_wrapper: Dict[str, Any]):
        """Test the end_forward method."""
        wrapper = setup_wrapper["wrapper"]

        # Create and process a sequence
        seq_metadata = create_sequence_metadata("test_seq", 4, 8, [0, 1, 2, 3], True)
        wrapper.begin_forward([seq_metadata])

        # End forward
        wrapper.end_forward()

        # Check that metadata is no longer initialized
        assert wrapper.is_metadata_initialized is False
