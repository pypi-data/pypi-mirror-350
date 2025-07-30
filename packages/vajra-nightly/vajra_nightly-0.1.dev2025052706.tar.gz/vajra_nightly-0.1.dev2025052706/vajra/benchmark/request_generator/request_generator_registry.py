from vajra.benchmark.request_generator.synthetic_request_generator import (
    SyntheticRequestGenerator,
)
from vajra.benchmark.request_generator.trace_request_generator import (
    TraceRequestGenerator,
)
from vajra.enums import RequestGeneratorType
from vajra.utils.base_registry import BaseRegistry


class RequestGeneratorRegistry(BaseRegistry):
    pass


RequestGeneratorRegistry.register(
    RequestGeneratorType.SYNTHETIC, SyntheticRequestGenerator
)
RequestGeneratorRegistry.register(RequestGeneratorType.TRACE, TraceRequestGenerator)
