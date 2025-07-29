from __future__ import annotations

import asyncio
import logging
import traceback
from typing import Any, TypeAlias, TypeVar

from moxn.settings import get_moxn_settings
from moxn_types.telemetry import SpanEventLogRequest, SpanLogRequest

_Sendable: TypeAlias = SpanLogRequest | SpanEventLogRequest
T = TypeVar("T")
logger = logging.getLogger(__name__)


class TelemetryDispatcher:
    """
    Background-worker pool that delivers telemetry envelopes to the backend.

    Calls to `enqueue()` never block on I/O – they just put the envelope on
    an asyncio.Queue. One or more workers drain that queue.
    """

    def __init__(
        self,
        backend: Any,
        *,
        concurrency: int = 4,
        queue_maxsize: int = 10_000,
    ) -> None:
        self._backend = backend
        self._q: asyncio.Queue[_Sendable] = asyncio.Queue(maxsize=queue_maxsize)
        self._workers: list[asyncio.Task[None]] = []
        self._closing = asyncio.Event()
        self._concurrency = max(1, concurrency)
        # Add a debug counter to track pending items
        self._pending_count = 0
        self._debug = logger.isEnabledFor(logging.DEBUG)

    async def __aenter__(self) -> "TelemetryDispatcher":
        await self.start()
        return self

    async def __aexit__(self, exc_t, exc, tb) -> None:
        await self.stop()

    # --------------------------------------------------------------------- #
    # public API
    # --------------------------------------------------------------------- #

    async def start(self) -> None:
        """Spawn background workers (idempotent)."""
        if self._workers:
            return
        for i in range(self._concurrency):
            self._workers.append(
                asyncio.create_task(self._worker(), name=f"telemetry-worker-{i}")
            )
        logger.debug(f"Started {len(self._workers)} telemetry workers")

    async def enqueue(self, item: _Sendable) -> None:
        """Put an envelope on the queue without awaiting network I/O."""
        await self._q.put(item)
        self._pending_count += 1
        if self._debug:
            logger.debug(
                f"Enqueued {type(item).__name__} - pending: {self._pending_count}"
            )

    async def flush(self, timeout: float | None = get_moxn_settings().timeout) -> None:
        """
        Block until the queue is empty (or timeout).

        Use this in serverless handlers before returning.
        """
        if self._pending_count > 0 or not self._q.empty():
            logger.debug(
                f"Flushing {self._pending_count} pending telemetry items (timeout: {timeout}s)"
            )
            try:
                await asyncio.wait_for(self._q.join(), timeout=timeout)
                logger.debug("Telemetry queue flushed successfully")
            except asyncio.TimeoutError:
                logger.warning(
                    f"Flush timed out after {timeout}s with {self._pending_count} items remaining"
                )
                raise

    async def stop(self) -> None:
        """Flush and cancel workers."""
        try:
            # First try to flush with a reasonable timeout
            await self.flush(timeout=get_moxn_settings().timeout)
        except asyncio.TimeoutError:
            logger.warning("Failed to flush all telemetry before stopping")

        # Signal workers to stop and wait for them
        self._closing.set()
        if self._workers:
            logger.debug(f"Stopping {len(self._workers)} telemetry workers")
            for t in self._workers:
                t.cancel()
            await asyncio.gather(*self._workers, return_exceptions=True)
            self._workers.clear()
            logger.debug("All telemetry workers stopped")

    # --------------------------------------------------------------------- #
    # internal
    # --------------------------------------------------------------------- #

    async def _worker(self) -> None:
        """Worker loop that processes queue items."""
        logger.debug(
            f"Telemetry worker {getattr(asyncio.current_task(), 'get_name', lambda: 'unknown')} started"
        )

        while not self._closing.is_set():
            try:
                # Get the next item or wait for a closing signal
                item = await asyncio.wait_for(
                    self._q.get(),
                    timeout=0.5,  # Check for closing every 0.5s
                )
            except asyncio.TimeoutError:
                continue  # No items, check closing and try again
            except asyncio.CancelledError:
                logger.debug(
                    f"Worker {getattr(asyncio.current_task(), 'get_name', lambda: 'unknown')} cancelled"
                )
                break

            success = False
            try:
                if self._debug:
                    logger.debug(f"Processing {type(item).__name__}")

                # Actually send the telemetry (this is the part that can take time)
                await self._backend.send_telemetry_log(item)
                success = True

                if self._debug:
                    logger.debug(f"Successfully sent {type(item).__name__}")
            except Exception as e:
                logger.error(f"Failed to send telemetry: {e}\n{traceback.format_exc()}")
            finally:
                # CRITICAL: Mark the item as done regardless of success/failure
                # This is what makes q.join() resolve when the queue is empty
                self._q.task_done()
                self._pending_count -= 1

                if self._debug:
                    status = "✓" if success else "✗"
                    logger.debug(
                        f"{status} Completed {type(item).__name__} - remaining: {self._pending_count}"
                    )

        logger.debug(
            f"Telemetry worker {getattr(asyncio.current_task(), 'get_name', lambda: 'unknown')} exiting"
        )
