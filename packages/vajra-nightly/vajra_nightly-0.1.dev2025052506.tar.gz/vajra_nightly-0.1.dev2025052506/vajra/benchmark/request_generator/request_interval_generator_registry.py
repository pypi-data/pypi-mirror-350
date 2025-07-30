from vajra.benchmark.request_generator.gamma_request_interval_generator import (
    GammaRequestIntervalGenerator,
)
from vajra.benchmark.request_generator.poisson_request_interval_generator import (
    PoissonRequestIntervalGenerator,
)
from vajra.benchmark.request_generator.static_request_interval_generator import (
    StaticRequestIntervalGenerator,
)
from vajra.benchmark.request_generator.trace_request_interval_generator import (
    TraceRequestIntervalGenerator,
)
from vajra.enums import RequestIntervalGeneratorType
from vajra.utils.base_registry import BaseRegistry


class RequestIntervalGeneratorRegistry(BaseRegistry):
    pass


RequestIntervalGeneratorRegistry.register(
    RequestIntervalGeneratorType.GAMMA, GammaRequestIntervalGenerator
)
RequestIntervalGeneratorRegistry.register(
    RequestIntervalGeneratorType.POISSON, PoissonRequestIntervalGenerator
)
RequestIntervalGeneratorRegistry.register(
    RequestIntervalGeneratorType.STATIC, StaticRequestIntervalGenerator
)
RequestIntervalGeneratorRegistry.register(
    RequestIntervalGeneratorType.TRACE, TraceRequestIntervalGenerator
)
