import logging
import os
from datetime import datetime

import yaml

from vajra.benchmark.benchmark_runner import BenchmarkRunner
from vajra.benchmark.config import BenchmarkConfig
from vajra.benchmark.constants import LOGGER_FORMAT, LOGGER_TIME_FORMAT
from vajra.benchmark.utils.random import set_seeds
from vajra.logger import init_logger

logger = init_logger(__name__)


def main() -> None:
    config = BenchmarkConfig.create_from_cli_args()

    # override configs
    # TODO(Amey): Find a cleaner way to implement this

    if config.use_dummy_weights:
        # override model load format to dummy
        object.__setattr__(
            config.inference_engine_config.controller_config.replica_controller_config.model_config,
            "load_format",
            "dummy",
        )

        # update native handle to use dummy weights
        config.inference_engine_config.controller_config.replica_controller_config.model_config.update_native_handle()

    output_dir = (
        f"{config.output_dir}/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S-%f')}"
    )

    object.__setattr__(config, "output_dir", output_dir)
    object.__setattr__(
        config.inference_engine_config.metrics_config, "output_dir", output_dir
    )
    # Call __post_init__ to update native handler with new output_dir
    config.inference_engine_config.metrics_config.__post_init__()

    os.makedirs(config.output_dir, exist_ok=True)
    with open(os.path.join(config.output_dir, "config.yaml"), "w") as f:
        yaml.dump(config.to_dict(), f)

    logger.info(f"Starting benchmark with config: {config}")

    set_seeds(config.seed)

    log_level = getattr(logging, config.log_level.upper())
    logging.basicConfig(
        format=LOGGER_FORMAT, level=log_level, datefmt=LOGGER_TIME_FORMAT
    )

    runner = BenchmarkRunner(config)
    runner.run()


if __name__ == "__main__":
    main()
