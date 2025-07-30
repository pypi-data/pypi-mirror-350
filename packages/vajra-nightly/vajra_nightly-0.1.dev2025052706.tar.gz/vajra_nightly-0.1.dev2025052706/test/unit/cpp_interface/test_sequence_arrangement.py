from typing import List

import pytest

from vajra.datatypes import SequenceMetadata
from vajra.model_executor.layers.attention import SequenceArrangement


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


def is_equal_sequence_metadata(
    metadata1: SequenceMetadata, metadata2: SequenceMetadata
) -> bool:
    if (
        metadata1.schedule_id != metadata2.schedule_id
        or metadata1.seq_id != metadata2.seq_id
        or metadata1.num_q_tokens != metadata2.num_q_tokens
        or metadata1.num_kv_tokens != metadata2.num_kv_tokens
        or metadata1.block_table != metadata2.block_table
        or metadata1.kvp_group_ids != metadata2.kvp_group_ids
        or metadata1.save_kv_cache != metadata2.save_kv_cache
    ):
        return False
    return True


def is_equal_splits(
    splits1: List[List[SequenceMetadata]], splits2: List[List[SequenceMetadata]]
) -> bool:
    if len(splits1) != len(splits2):
        return False
    for split1, split2 in zip(splits1, splits2):
        if len(split1) != len(split2):
            return False
        for seq1, seq2 in zip(split1, split2):
            if not is_equal_sequence_metadata(seq1, seq2):
                return False
    return True


def is_equal_arranged(
    arranged1: List[SequenceMetadata], arranged2: List[SequenceMetadata]
) -> bool:
    if len(arranged1) != len(arranged2):
        return False
    for seq1, seq2 in zip(arranged1, arranged2):
        if not is_equal_sequence_metadata(seq1, seq2):
            return False
    return True


@pytest.mark.unit
class TestSequenceArrangement:
    def test_empty_sequence_list(self):
        """Test behavior with an empty sequence list."""
        sequence_arrangement = SequenceArrangement()

        # Process empty sequence list
        sequence_arrangement.check_arrangement_and_extend([])

        # Get splits
        splits = sequence_arrangement.get_splits()

        # Check splits are correct
        expected_splits = [
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
        ]

        assert is_equal_splits(splits, expected_splits)

    def test_single_sequence(self):
        """Test behavior with a single sequence."""
        sequence_arrangement = SequenceArrangement()

        # Create a single sequence
        seq_metadata = create_sequence_metadata("test_seq", 4, 8, [0, 1, 2, 3], True)

        # Process the sequence
        sequence_arrangement.check_arrangement_and_extend([seq_metadata])

        # Get splits
        splits = sequence_arrangement.get_splits()

        # Check splits are correct
        expected_splits = [
            [],
            [],
            [seq_metadata],
            [],
            [],
            [],
            [],
            [],
        ]

        assert is_equal_splits(splits, expected_splits)

    def test_multiple_sequences(self):
        """Test behavior with multiple sequences."""
        sequence_arrangement = SequenceArrangement()

        # Create multiple sequences
        seq_metadata1 = create_sequence_metadata(
            "test_seq1", 4, 8, [1, 2, 3, 4], True, [0]
        )
        seq_metadata2 = create_sequence_metadata(
            "test_seq2", 2, 12, [4, 5, 6, 7], True, [0, 1]
        )
        seq_metadata3 = create_sequence_metadata(
            "test_seq3", 8, 4, [8, 9, 10, 11], False, [0]
        )
        seq_metadata4 = create_sequence_metadata(
            "test_seq4", 6, 8, [12, 13, 14, 15], False, [0, 1]
        )
        seq_metadata5 = create_sequence_metadata(
            "test_seq5", 1, 8, [16, 17, 18, 19], True, [0]
        )
        seq_metadata6 = create_sequence_metadata(
            "test_seq6", 1, 12, [20, 21, 22, 23], True, [0, 1]
        )
        seq_metadata7 = create_sequence_metadata(
            "test_seq7", 1, 4, [24, 25, 26, 27], False, [0]
        )
        seq_metadata8 = create_sequence_metadata(
            "test_seq8", 1, 8, [28, 29, 30, 31], False, [0, 1]
        )

        # Process the sequences
        sequence_arrangement.check_arrangement_and_extend(
            [
                seq_metadata1,
                seq_metadata2,
                seq_metadata3,
                seq_metadata4,
                seq_metadata5,
                seq_metadata6,
                seq_metadata7,
                seq_metadata8,
            ]
        )

        # Get splits
        splits = sequence_arrangement.get_splits()

        # Check splits are correct
        expected_splits = [
            [],
            [],
            [seq_metadata1, seq_metadata2],
            [seq_metadata3, seq_metadata4],
            [],
            [],
            [seq_metadata5, seq_metadata6],
            [seq_metadata7, seq_metadata8],
        ]

        assert is_equal_splits(splits, expected_splits)

        # Get arranged output
        arranged = sequence_arrangement.get_arranged()

        # Check arranged output is correct
        expected_arranged = [
            seq_metadata1,
            seq_metadata2,
            seq_metadata3,
            seq_metadata4,
            seq_metadata5,
            seq_metadata6,
            seq_metadata7,
            seq_metadata8,
        ]

        assert is_equal_arranged(arranged, expected_arranged)

    def test_num_splits(self):
        """Test the number of splits."""
        sequence_arrangement = SequenceArrangement()

        # Create sequences
        seq_metadata1 = create_sequence_metadata(
            "test_seq1", 4, 8, [0, 1, 2, 3], True, [0]
        )
        seq_metadata2 = create_sequence_metadata(
            "test_seq2", 2, 12, [4, 5, 6, 7], True, [0, 1]
        )

        # Process the sequences
        sequence_arrangement.check_arrangement_and_extend(
            [seq_metadata1, seq_metadata2]
        )

        # Check number of splits
        assert sequence_arrangement.get_num_splits() == 8
        assert len(sequence_arrangement.get_splits()) == 8
