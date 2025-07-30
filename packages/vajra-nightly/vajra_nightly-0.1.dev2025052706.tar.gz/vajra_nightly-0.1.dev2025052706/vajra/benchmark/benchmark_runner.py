import logging
import threading
import time
from typing import Any, Dict, Tuple

import ray
import wandb
from tqdm import tqdm

from vajra.benchmark.config import BenchmarkConfig
from vajra.benchmark.entities import Request
from vajra.benchmark.request_generator import RequestGeneratorRegistry
from vajra.benchmark.utils.random import set_seeds
from vajra.datatypes import SamplingParams
from vajra.engine.inference_engine import InferenceEngine

logger = logging.getLogger(__name__)


class BenchmarkRunner:

    def __init__(
        self,
        config: BenchmarkConfig,
    ) -> None:
        self.config = config
        set_seeds(self.config.seed)
        request_generator = RequestGeneratorRegistry.get(
            self.config.request_generator_config.get_type(),
            self.config.request_generator_config,
        )
        self.requests = request_generator.generate()
        engine_config = self.config.inference_engine_config
        self.engine = InferenceEngine(engine_config)

        if wandb.run is not None:
            wandb.config.update(self.config.to_dict())

    def _get_input_params(self, request: Request) -> Dict[str, Any]:
        sampling_params = SamplingParams(
            ignore_eos=True,
            max_tokens=request.num_decode_tokens,
            temperature=0.5,
            top_p=0.9,
        )
        prompt_token_ids = [1] * request.num_prefill_tokens

        return {
            "prompt": "",
            "prompt_token_ids": prompt_token_ids,
            "sampling_params": sampling_params,
        }

    def warmup(self) -> None:
        self.engine.add_request(**self._get_input_params(self.requests[0]))

        while True:
            step_outputs = self.engine.get_outputs()
            if step_outputs and step_outputs[0].finished:
                break

        self.engine.reset_metrics()

    def _run_all_requests(self) -> Tuple[int, float, float]:
        num_processed_requests = 0
        num_steps = 0
        pbar = tqdm(
            total=len(self.requests),
            desc=f"Processed requests",
        )
        start_time = time.time()

        # Sort requests by arrival time
        self.requests.sort(key=lambda x: x.arrived_at)

        # Flag to signal the request adder thread to stop
        stop_thread = threading.Event()

        # Create a thread-safe queue to track requests that have been added
        request_added_count = 0

        # Define the request adder function that will run in a separate thread
        def request_adder():
            nonlocal request_added_count
            request_add_index = 0

            while not stop_thread.is_set() and request_add_index < len(self.requests):
                elapsed_time = time.time() - start_time

                # Check if we've hit time limit
                if (
                    self.config.time_limit is not None
                    and elapsed_time > self.config.time_limit
                ):
                    break

                # Add all requests that have "arrived" based on elapsed time
                while (
                    request_add_index < len(self.requests)
                    and self.requests[request_add_index].arrived_at <= elapsed_time
                ):
                    self.engine.add_request(
                        **self._get_input_params(self.requests[request_add_index])
                    )
                    request_add_index += 1
                    request_added_count += 1

                time.sleep(0.001)

        # Start the request adder thread
        adder_thread = threading.Thread(target=request_adder, daemon=True)
        adder_thread.start()

        # Run the engine in the main thread
        while num_processed_requests < len(self.requests):
            elapsed_time = time.time() - start_time
            if (
                self.config.time_limit is not None
                and elapsed_time > self.config.time_limit
            ):
                break

            # Get outputs from the engine
            # Block if there are pending requests (added but not processed) -> we dont want a spinning loop
            step_outputs = self.engine.get_outputs(
                block=((request_added_count - num_processed_requests) > 0)
            )
            num_steps += 1

            for output in step_outputs:
                if output.finished:
                    num_processed_requests += 1
                    pbar.update(1)

        # Signal the request adder thread to stop
        stop_thread.set()
        adder_thread.join(timeout=1.0)  # Wait for the thread to finish

        end_time = time.time()
        pbar.close()

        return num_steps, start_time, end_time

    def _run(self) -> None:
        logger.info(f"Starting warmpup")
        self.warmup()

        self.engine.reset_metrics()

        logger.info(f"Starting benchmark")

        num_steps, start_time, end_time = self._run_all_requests()

        logger.info(
            f"Exiting after processing {len(self.requests)} requests ({num_steps} iterations), Total time taken: {end_time - start_time:.2f} seconds"
        )

    def run(self) -> None:
        self.engine.reset_metrics()
        self._run()
        self.engine.plot_metrics()
        wandb.finish()
        ray.shutdown()
