import time

import pytest

from vajra.datatypes import (
    LogicalTokenBlock,
    SamplerOutput,
    SamplingParams,
    SamplingType,
    SequenceState,
    SequenceStatus,
)


@pytest.mark.unit
def test_logical_token_block_cpp():
    block = LogicalTokenBlock(1, 5)

    # Test initial state
    assert block.is_empty is True
    assert block.num_empty_slots == 5
    assert block.is_full is False

    # Append tokens
    block.append_tokens([10, 20, 30])
    assert block.is_empty is False
    assert block.num_empty_slots == 2
    assert block.is_full is False
    assert block.get_last_token_id() == 30

    # Fill the block
    block.append_tokens([40, 50])
    assert block.is_full is True
    assert block.num_empty_slots == 0
    assert block.get_last_token_id() == 50

    # Ensure overfilling is not allowed
    with pytest.raises(RuntimeError):
        block.append_tokens([60])


@pytest.mark.unit
def test_sampler_output_cpp():
    output = SamplerOutput(
        schedule_id=1,
        seq_id="foo",
        output_tokens=[1, 2, 3],
    )

    assert (
        str(output) == "SamplerOutput(ScheduleId: 1,SeqId: foo,OutputTokens: 1, 2, 3)"
    )

    outputs = [output]
    outputs.append(SamplerOutput(2, "bar", [4, 5]))
    outputs.append(None)
    assert len(outputs) == 3


@pytest.mark.unit
def test_sequence_status_cpp():
    status = SequenceStatus.WAITING
    assert SequenceStatus.is_finished(status) == False
    assert SequenceStatus.is_executing(status) == False
    assert SequenceStatus.is_waiting(status) == True
    assert SequenceStatus.is_waiting_preempted(status) == False
    assert SequenceStatus.is_paused(status) == False
    assert SequenceStatus.is_running(status) == False
    assert SequenceStatus.get_finished_reason(status) == None

    status = SequenceStatus.WAITING_PREEMPTED
    assert SequenceStatus.is_finished(status) == False
    assert SequenceStatus.is_executing(status) == False
    assert SequenceStatus.is_waiting(status) == False
    assert SequenceStatus.is_waiting_preempted(status) == True
    assert SequenceStatus.is_paused(status) == False
    assert SequenceStatus.is_running(status) == False
    assert SequenceStatus.get_finished_reason(status) == None

    status = SequenceStatus.RUNNING
    assert SequenceStatus.is_finished(status) == False
    assert SequenceStatus.is_executing(status) == True
    assert SequenceStatus.is_waiting(status) == False
    assert SequenceStatus.is_waiting_preempted(status) == False
    assert SequenceStatus.is_paused(status) == False
    assert SequenceStatus.is_running(status) == True
    assert SequenceStatus.get_finished_reason(status) == None

    status = SequenceStatus.PAUSED
    assert SequenceStatus.is_finished(status) == False
    assert SequenceStatus.is_executing(status) == True
    assert SequenceStatus.is_waiting(status) == False
    assert SequenceStatus.is_waiting_preempted(status) == False
    assert SequenceStatus.is_paused(status) == True
    assert SequenceStatus.is_running(status) == False
    assert SequenceStatus.get_finished_reason(status) == None

    status = SequenceStatus.FINISHED_STOPPED
    assert SequenceStatus.is_finished(status) == True
    assert SequenceStatus.is_executing(status) == False
    assert SequenceStatus.is_waiting(status) == False
    assert SequenceStatus.is_waiting_preempted(status) == False
    assert SequenceStatus.is_paused(status) == False
    assert SequenceStatus.is_running(status) == False
    assert SequenceStatus.get_finished_reason(status) == "stop"

    status = SequenceStatus.FINISHED_LENGTH_CAPPED
    assert SequenceStatus.is_finished(status) == True
    assert SequenceStatus.is_executing(status) == False
    assert SequenceStatus.is_waiting(status) == False
    assert SequenceStatus.is_waiting_preempted(status) == False
    assert SequenceStatus.is_paused(status) == False
    assert SequenceStatus.is_running(status) == False
    assert SequenceStatus.get_finished_reason(status) == "length"

    status = SequenceStatus.FINISHED_IGNORED
    assert SequenceStatus.is_finished(status) == True
    assert SequenceStatus.is_executing(status) == False
    assert SequenceStatus.is_waiting(status) == False
    assert SequenceStatus.is_waiting_preempted(status) == False
    assert SequenceStatus.is_paused(status) == False
    assert SequenceStatus.is_running(status) == False
    assert SequenceStatus.get_finished_reason(status) == "length"


@pytest.mark.unit
def test_sampling_params_cpp():
    params = SamplingParams(top_p=0.99, top_k=100)
    assert params.sampling_type == SamplingType.RANDOM

    with pytest.raises(ValueError, match=r"temperature must be non-negative, got -2"):
        params = SamplingParams(temperature=-2)
    with pytest.raises(ValueError, match=r"top_p must be in \(0, 1], got -1"):
        params = SamplingParams(top_p=-1)
    with pytest.raises(ValueError, match=r"top_p must be in \(0, 1], got 5"):
        params = SamplingParams(top_p=5)
    with pytest.raises(
        ValueError, match=r"top_k must be -1 \(disable\) or at least 1, got -2"
    ):
        params = SamplingParams(top_k=-2)
    with pytest.raises(ValueError, match=r"max_tokens must be at least 1, got 0"):
        params = SamplingParams(max_tokens=0)

    params = SamplingParams(temperature=1e-6, top_p=1, top_k=-1)
    assert params.sampling_type == SamplingType.GREEDY

    with pytest.raises(ValueError, match=r"top_p must be 1 when using greedy sampling"):
        params = SamplingParams(temperature=1e-6, top_p=0.99)
    with pytest.raises(
        ValueError, match=r"top_k must be -1 when using greedy sampling"
    ):
        params = SamplingParams(temperature=1e-6, top_p=1, top_k=100)


@pytest.mark.unit
def test_sequence_state_cpp():
    state = SequenceState("0", time.time(), 100)
    assert state.id == "0"
    assert state.status == SequenceStatus.WAITING
    assert state.num_output_tokens == 0
    assert state.is_scheduled == False
    assert state.is_completed == False

    state.status = SequenceStatus.RUNNING
    assert state.is_scheduled
    assert state.scheduled_at is not None

    state.status = SequenceStatus.PAUSED
    state.status = SequenceStatus.RUNNING
    state.status = SequenceStatus.WAITING_PREEMPTED

    state.on_prompt_processing_completed()
    assert state.prompt_processing_completed_at is not None

    with pytest.raises(
        RuntimeError,
        match=r"Invalid state transition from waiting_preempted to paused for request 0",
    ):
        state.status = SequenceStatus.PAUSED

    state.status = SequenceStatus.RUNNING
    with pytest.raises(
        RuntimeError,
        match=r"Invalid state transition from running to finished_stopped for request 0",
    ):
        state.status = SequenceStatus.FINISHED_STOPPED

    state.on_token_generated()
    state.on_token_generated()
    state.on_token_generated()
    assert state.num_output_tokens == 3

    state.status = SequenceStatus.PAUSED
    state.status = SequenceStatus.FINISHED_STOPPED

    assert state.e2e_time is not None
