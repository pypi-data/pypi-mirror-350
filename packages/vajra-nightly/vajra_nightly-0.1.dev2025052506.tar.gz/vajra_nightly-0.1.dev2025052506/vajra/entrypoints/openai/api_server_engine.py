import asyncio
import functools
from typing import AsyncIterator, Dict, List, Optional

from vajra.datatypes import RequestOutput, SamplingParams
from vajra.engine.inference_engine import InferenceEngine
from vajra.logger import init_logger

logger = init_logger(__name__)


class ApiServerEngine:
    """
    Manages asynchronous interaction with a synchronous InferenceEngine.

    This class provides an asyncio-friendly interface to an InferenceEngine
    that is assumed to have synchronous, potentially blocking methods.
    It handles:
    - Submitting generation requests to the engine via `run_in_executor`.
    - Aborting requests in the engine via `run_in_executor`.
    - A dedicated asyncio task (`_output_polling_task`) that continuously polls
      the engine's `get_outputs` method (using `run_in_executor` with a
      blocking call and a timeout).
    - Dispatching outputs from the engine to the appropriate asynchronous
      generator streams.
    - Graceful startup and shutdown of the polling task.
    - "Fail-fast" behavior for the critical output polling task: if the poller
      encounters an unrecoverable error from the engine, it terminates,
      and the ApiServerEngine will stop accepting new requests.

    Assumptions about `InferenceEngine`:
    - `engine.add_request(...)` is thread-safe for concurrent calls.
    - `engine.abort(request_id)` is thread-safe for concurrent calls.
    - `engine.get_outputs(block: bool, timeout: float)` exists, is thread-safe,
      and blocks efficiently when `block=True` until outputs are available or
      the timeout is reached.
    """

    def __init__(
        self,
        engine: InferenceEngine,
    ):
        """
        Initializes the ApiServerEngine.

        Args:
            engine: An instance of the synchronous InferenceEngine.
            loop: The asyncio event loop to use. If None, `asyncio.get_running_loop()` is used.
            get_outputs_block_timeout_sec: Timeout in seconds for the blocking
                `engine.get_outputs()` call within the polling loop. This allows
                the poller to periodically check for shutdown signals.
        """
        self.engine: InferenceEngine = engine
        self.loop: asyncio.AbstractEventLoop = asyncio.get_running_loop()

        self._request_output_queues: Dict[str, asyncio.Queue[RequestOutput]] = {}
        self._output_polling_task: Optional[asyncio.Task[None]] = None
        self._shutdown_requested: bool = False

        self._service_healthy: bool = True  # Tracks health based on poller

        logger.info("ApiServerEngine initialized.")

    async def start(self) -> None:
        """
        Starts the background asyncio task that polls for engine outputs.

        This method should be called once when the server or application starts
        and needs the ApiServerEngine to be active. Idempotent if already started.
        """
        if self._output_polling_task and not self._output_polling_task.done():
            logger.warning("Engine output polling task is already running.")
            return

        self._shutdown_requested = False
        self._service_healthy = True  # Assume healthy on start
        self._output_polling_task = self.loop.create_task(
            self._poll_engine_outputs(), name="ApiServerEngine-OutputPoller"
        )
        self._output_polling_task.add_done_callback(self._handle_poller_completion)
        logger.info("Engine output polling task started.")

    def _handle_poller_completion(self, task: asyncio.Task[None]) -> None:
        """
        Callback executed when the `_output_polling_task` finishes.
        Logs any unhandled exceptions and marks the service as unhealthy.
        """
        try:
            task.result()  # Re-raises exception if task failed.
            # If result() doesn't raise, and it wasn't cancelled, it means normal completion (e.g. shutdown).
            if not task.cancelled():
                logger.info(
                    "Output polling task '%s' completed normally.", task.get_name()
                )
        except asyncio.CancelledError:
            logger.info("Output polling task '%s' was cancelled.", task.get_name())
        except Exception:
            logger.exception(
                "Output polling task '%s' failed with an unhandled error. "
                "Service will be marked as unhealthy.",
                task.get_name(),
            )
            self._service_healthy = False  # Critical component failed
            # Consider additional actions: e.g., trigger application-level shutdown.
        # If task is done for any reason other than explicit shutdown, and it wasn't cancelled,
        # it might be an issue.
        if not self._shutdown_requested and not task.cancelled():
            logger.warning(
                "Output polling task '%s' finished unexpectedly. Service health may be affected.",
                task.get_name(),
            )
            self._service_healthy = False

    async def _poll_engine_outputs(self) -> None:
        """
        Continuously polls `engine.get_outputs()` and dispatches results.

        This is the core background task. It uses `run_in_executor` to call
        the potentially blocking `engine.get_outputs(block=True)`.
        If `engine.get_outputs()` raises an unrecoverable error, this task
        will terminate, and `_handle_poller_completion` will log the error
        and mark the service as unhealthy.
        """

        try:
            while not self._shutdown_requested:
                try:
                    get_outputs_with_args = functools.partial(
                        self.engine.get_outputs,
                        block=True,  # Crucial for efficient waiting
                    )
                    outputs: List[RequestOutput] = await self.loop.run_in_executor(
                        None, get_outputs_with_args
                    )
                except Exception as e:
                    logger.exception(
                        f"Critical error during 'engine.get_outputs' call {e}"
                    )
                    raise  # Propagates to _handle_poller_completion

                if (
                    self._shutdown_requested
                ):  # Re-check after potentially long blocking call
                    break

                if not outputs:  # Timeout occurred in get_outputs without new data
                    continue

                for output in outputs:
                    queue = self._request_output_queues.get(output.request_id)
                    if queue:
                        try:
                            await queue.put(output)
                        except (
                            asyncio.QueueFull
                        ):  # Should ideally not happen with unbounded Queues
                            logger.warning(
                                f"Output queue full for request_id {output.request_id}. "
                                "Consumer might be stuck or queue too small."
                            )
                        except Exception as e:  # Should be rare for asyncio.Queue.put
                            logger.error(
                                f"Error putting output to queue for request_id {output.request_id}: {e}"
                            )

                        if output.finished:
                            logger.debug(
                                f"Request_id {output.request_id} finished. Removing its queue."
                            )
                            self._request_output_queues.pop(output.request_id, None)
                    elif (
                        not output.finished
                    ):  # Log only if not a late 'finished' signal
                        logger.warning(
                            f"Polled output for unknown or cleaned-up request_id {output.request_id}."
                        )
        except asyncio.CancelledError:
            logger.info("Engine output polling task was cancelled.")
            raise  # Propagate cancellation
        finally:
            for request_id, q in list(self._request_output_queues.items()):
                logger.warning(
                    f"Forcing cleanup for request_id {request_id} due to engine shutdown.",
                )
                # Use a synthetic output to unblock any awaiters on the queue.
                final_output = RequestOutput(
                    seq_id=request_id,
                    prompt="",
                    finished=True,
                    text="",
                    finished_reason=f"Engine shutdown while request was active.",
                )
                try:
                    q.put_nowait(final_output)
                except asyncio.QueueFull:
                    logger.warning(
                        f"Failed to put final shutdown output for request_id {request_id}, queue full."
                    )
                except Exception as e_put:
                    logger.debug(
                        f"Error putting final shutdown output for request_id {request_id}: {e_put}"
                    )
                self._request_output_queues.pop(request_id, None)  # Ensure removal

    async def generate(
        self,
        request_id: str,
        prompt: str,
        sampling_params: SamplingParams,
    ) -> AsyncIterator[RequestOutput]:
        """
        Generates completion for the given prompt asynchronously.

        Submits the request to the InferenceEngine and returns an async iterator
        that yields `RequestOutput` objects as they become available.

        Args:
            request_id: A unique identifier for this generation request.
            prompt: The input prompt string.
            sampling_params: Sampling parameters for the generation.
            kwargs: Additional keyword arguments to pass to `engine.add_request`.

        Raises:
            RuntimeError: If the ApiServerEngine is not healthy (e.g., output poller crashed)
                          or fails to start the poller.
            ValueError: If the `request_id` is already in use.
            Exception: Propagates exceptions from `engine.add_request` or other unexpected errors.

        Important:
            The call to `self.engine.add_request` inside this method must
            match the actual signature of your `InferenceEngine.add_request`
            method, including any additional required arguments.
        """
        if not self._service_healthy:
            logger.error(
                "Cannot process request '%s': ApiServerEngine is unhealthy (output poller may have failed).",
                request_id,
            )
            raise RuntimeError("ApiServerEngine service is unhealthy.")

        if not self._output_polling_task or self._output_polling_task.done():
            logger.warning(
                "Output polling task not running or has finished for request '%s'. Attempting to restart.",
                request_id,
            )
            await self.start()  # Attempt to restart
            await asyncio.sleep(0.01)  # Brief moment for task scheduling
            if (
                not self._output_polling_task
                or self._output_polling_task.done()
                or not self._service_healthy
            ):
                logger.error(
                    "Failed to ensure output polling task is running for request '%s'.",
                    request_id,
                )
                raise RuntimeError(
                    "Failed to start/ensure output polling task is running."
                )

        if request_id in self._request_output_queues:
            logger.error(
                f"Request ID '{request_id}' already exists. Cannot process duplicate."
            )
            raise ValueError(f"Request ID '{request_id}' already exists.")

        output_q: asyncio.Queue[RequestOutput] = asyncio.Queue()
        self._request_output_queues[request_id] = output_q

        try:
            logger.debug(f"Submitting request '{request_id}' to InferenceEngine.")
            add_request_func = functools.partial(
                self.engine.add_request,
                prompt,
                sampling_params,
                [],
                request_id,
            )
            await self.loop.run_in_executor(None, add_request_func)
            logger.debug(f"Request '{request_id}' submitted to InferenceEngine.")

            while True:
                response = await output_q.get()
                yield response
                if response.finished:
                    logger.debug(
                        f"Async iterator for request '{request_id}' finished normally."
                    )
                    break
        except asyncio.CancelledError:
            logger.info(
                f"Generation for request '{request_id}' was cancelled by client."
            )
            await self.abort(request_id)  # Attempt to abort in engine
            raise
        except Exception as e:
            logger.exception(f"Error during generation for request '{request_id}'.")
            # Try to send a final error output to the client.
            error_msg = f"Error during generation: {type(e).__name__}: {e}"
            final_error_output = RequestOutput(
                seq_id=request_id,
                prompt=prompt,
                finished=True,
                text="",
                finished_reason=error_msg,
            )
            if (
                request_id in self._request_output_queues
            ):  # Queue might have been removed
                try:
                    self._request_output_queues[request_id].put_nowait(
                        final_error_output
                    )
                except (
                    asyncio.QueueFull,
                    Exception,
                ) as put_e:  # Broad catch for put_nowait
                    logger.debug(
                        f"Error sending final error output for '{request_id}': {put_e}"
                    )
            raise
        finally:
            if self._request_output_queues.pop(request_id, None):
                logger.debug(
                    "Cleaned up output queue for request '%s' from generate's fallback.",
                    request_id,
                )

    async def abort(self, request_id: str) -> None:
        """
        Aborts a running generation request in the InferenceEngine.

        This method attempts to tell the engine to stop processing for the
        given `request_id`. It assumes `engine.abort(request_id)` is
        thread-safe.

        Args:
            request_id: The unique identifier of the request to abort.
        """
        logger.info(f"Attempting to abort request '{request_id}' in InferenceEngine.")
        try:
            await self.loop.run_in_executor(None, self.engine.abort, request_id)
            logger.info(f"Engine abort call for request '{request_id}' completed.")
        except Exception as e:
            logger.error(f"Error calling engine.abort for request '{request_id}': {e}")

    async def close(self) -> None:
        """
        Gracefully shuts down the ApiServerEngine.

        This involves cancelling the output polling task and waiting for it
        to complete its cleanup.
        """
        logger.info("Initiating shutdown of ApiServerEngine...")
        self._shutdown_requested = True
        self._service_healthy = False  # No longer healthy once shutdown is initiated

        if self._output_polling_task and not self._output_polling_task.done():
            logger.info("Cancelling engine output polling task...")
            self._output_polling_task.cancel()
            try:
                await self._output_polling_task
            except asyncio.CancelledError:
                logger.info(
                    "Engine output polling task successfully cancelled during close."
                )

        # Clear any remaining request queues that might not have been cleaned by poller
        for request_id, q in list(self._request_output_queues.items()):
            logger.warning(
                f"Force-clearing queue for request '{request_id}' during final shutdown."
            )
            self._request_output_queues.pop(request_id, None)

        logger.info("ApiServerEngine shutdown complete.")

    @property
    def is_healthy(self) -> bool:
        """
        Indicates if the ApiServerEngine's critical components (like the poller) are running.
        """
        return (
            self._service_healthy
            and self._output_polling_task is not None
            and not self._output_polling_task.done()
        )
