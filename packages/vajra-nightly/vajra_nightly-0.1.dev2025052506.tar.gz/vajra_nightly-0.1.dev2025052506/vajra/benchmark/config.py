import sys
from dataclasses import field
from typing import Optional

from vajra.config import BaseEndpointConfig
from vajra.config.base_poly_config import BasePolyConfig
from vajra.enums import (
    RequestGeneratorType,
    RequestIntervalGeneratorType,
    RequestLengthGeneratorType,
)
from vajra.logger import init_logger
from vajra.utils.dataclasses import frozen_dataclass

logger = init_logger(__name__)


@frozen_dataclass
class BaseRequestIntervalGeneratorConfig(BasePolyConfig):
    seed: int = field(
        default=42, metadata={"help": "Random seed for the request interval generator."}
    )


@frozen_dataclass
class BaseRequestLengthGeneratorConfig(BasePolyConfig):
    seed: int = field(
        default=42, metadata={"help": "Random seed for the request length generator."}
    )


@frozen_dataclass
class TraceRequestIntervalGeneratorConfig(BaseRequestIntervalGeneratorConfig):
    trace_file: str = field(
        default="data/processed_traces/AzureFunctionsInvocationTraceForTwoWeeksJan2021Processed.csv",
        metadata={"help": "Path to the trace file for request intervals."},
    )
    start_time: str = field(
        default="1970-01-04 12:00:00", metadata={"help": "Start time for the trace."}
    )
    end_time: str = field(
        default="1970-01-04 15:00:00", metadata={"help": "End time for the trace."}
    )
    time_scale_factor: float = field(
        default=0.3,
        metadata={"help": "Factor to scale the time intervals in the trace."},
    )

    @staticmethod
    def get_type():
        return RequestIntervalGeneratorType.TRACE


@frozen_dataclass
class PoissonRequestIntervalGeneratorConfig(BaseRequestIntervalGeneratorConfig):
    qps: float = field(
        default=1.0,
        metadata={"help": "Queries per second for the Poisson distribution."},
    )

    @staticmethod
    def get_type():
        return RequestIntervalGeneratorType.POISSON


@frozen_dataclass
class GammaRequestIntervalGeneratorConfig(BaseRequestIntervalGeneratorConfig):
    qps: float = field(
        default=1.0, metadata={"help": "Queries per second for the Gamma distribution."}
    )
    cv: float = field(
        default=0.5,
        metadata={"help": "Coefficient of variation for the Gamma distribution."},
    )

    @staticmethod
    def get_type():
        return RequestIntervalGeneratorType.GAMMA


@frozen_dataclass
class StaticRequestIntervalGeneratorConfig(BaseRequestIntervalGeneratorConfig):
    @staticmethod
    def get_type():
        return RequestIntervalGeneratorType.STATIC


@frozen_dataclass
class TraceRequestLengthGeneratorConfig(BaseRequestLengthGeneratorConfig):
    trace_file: str = field(
        default="data/processed_traces/sharegpt_8k_stats_llama2_tokenizer_filtered_v2.csv",
        metadata={"help": "Path to the trace file for request lengths."},
    )
    prefill_scale_factor: float = field(
        default=1, metadata={"help": "Scale factor for prefill tokens."}
    )
    decode_scale_factor: float = field(
        default=1, metadata={"help": "Scale factor for decode tokens."}
    )
    max_tokens: int = field(
        default=4096, metadata={"help": "Maximum number of tokens allowed."}
    )

    @staticmethod
    def get_type():
        return RequestLengthGeneratorType.TRACE


@frozen_dataclass
class ZipfRequestLengthGeneratorConfig(BaseRequestLengthGeneratorConfig):
    theta: float = field(
        default=0.6, metadata={"help": "Theta parameter for the Zipf distribution."}
    )
    scramble: bool = field(
        default=False, metadata={"help": "Whether to scramble the Zipf distribution."}
    )
    min_tokens: int = field(
        default=1024, metadata={"help": "Minimum number of tokens."}
    )
    max_tokens: int = field(
        default=4096, metadata={"help": "Maximum number of tokens."}
    )
    prefill_to_decode_ratio: float = field(
        default=20.0, metadata={"help": "Ratio of prefill tokens to decode tokens."}
    )

    @staticmethod
    def get_type():
        return RequestLengthGeneratorType.ZIPF


@frozen_dataclass
class UniformRequestLengthGeneratorConfig(BaseRequestLengthGeneratorConfig):
    min_tokens: int = field(
        default=1024, metadata={"help": "Minimum number of tokens."}
    )
    max_tokens: int = field(
        default=4096, metadata={"help": "Maximum number of tokens."}
    )
    prefill_to_decode_ratio: float = field(
        default=20.0, metadata={"help": "Ratio of prefill tokens to decode tokens."}
    )

    @staticmethod
    def get_type():
        return RequestLengthGeneratorType.UNIFORM


@frozen_dataclass
class FixedRequestLengthGeneratorConfig(BaseRequestLengthGeneratorConfig):
    prefill_tokens: int = field(
        default=4096, metadata={"help": "Number of prefill tokens."}
    )
    decode_tokens: int = field(
        default=512, metadata={"help": "Number of decode tokens."}
    )

    @staticmethod
    def get_type():
        return RequestLengthGeneratorType.FIXED


@frozen_dataclass
class BaseRequestGeneratorConfig(BasePolyConfig):
    seed: int = field(
        default=42, metadata={"help": "Random seed for the request generator."}
    )


@frozen_dataclass
class SyntheticRequestGeneratorConfig(BaseRequestGeneratorConfig):
    length_generator_config: BaseRequestLengthGeneratorConfig = field(
        default_factory=TraceRequestLengthGeneratorConfig
    )
    interval_generator_config: BaseRequestIntervalGeneratorConfig = field(
        default_factory=PoissonRequestIntervalGeneratorConfig
    )
    num_requests: int = field(
        default=64, metadata={"help": "Number of requests to generate."}
    )
    duration: Optional[float] = field(
        default=None, metadata={"help": "Duration of the synthetic request generation."}
    )

    @staticmethod
    def get_type():
        return RequestGeneratorType.SYNTHETIC


@frozen_dataclass
class TraceRequestGeneratorConfig(BaseRequestGeneratorConfig):
    trace_file: str = field(
        default="data/processed_traces/sydney_enterprise.csv",
        metadata={"help": "Path to the trace file for request generation."},
    )
    date: Optional[str] = field(
        default=None, metadata={"help": "Date for the trace data."}
    )
    prefill_scale_factor: float = field(
        default=1, metadata={"help": "Scale factor for prefill tokens."}
    )
    decode_scale_factor: float = field(
        default=1, metadata={"help": "Scale factor for decode tokens."}
    )
    time_scale_factor: float = field(
        default=1, metadata={"help": "Scale factor for time intervals."}
    )
    max_tokens: Optional[int] = field(
        default=None, metadata={"help": "Maximum number of tokens allowed."}
    )

    @staticmethod
    def get_type():
        return RequestGeneratorType.TRACE


@frozen_dataclass
class BenchmarkConfig(BaseEndpointConfig):
    seed: int = field(default=42, metadata={"help": "Random seed for the benchmark."})
    output_dir: str = field(
        default="benchmark_output",
        metadata={"help": "Directory to store benchmark output."},
    )
    write_json_trace: bool = field(
        default=True, metadata={"help": "Whether to write JSON trace output."}
    )
    time_limit: int = field(
        default=sys.maxsize,
        metadata={"help": "Time limit for the benchmark in seconds."},
    )
    request_generator_config: BaseRequestGeneratorConfig = field(
        default_factory=SyntheticRequestGeneratorConfig
    )
    use_dummy_weights: bool = field(
        default=False, metadata={"help": "Whether to use dummy weights."}
    )
