from dataclasses import dataclass
from typing import Callable
from datetime import datetime
import asyncio
import logging
from tenacity import retry, stop_after_attempt, wait_exponential

logger = logging.getLogger(__name__)


@dataclass
class PollingConfig:
    """Configuration for polling tasks and prompts."""

    interval: float
    tasks_to_track: list[str]
    prompts_to_track: list[str]
    max_retries: int = 3
    retry_delay: float = 1.0


class PollingManager:
    def __init__(
        self,
        config: PollingConfig,
        fetch_task: Callable,
        fetch_prompt: Callable,
        store_task: Callable,
        store_prompt: Callable,
        get_last_polled: Callable,
        update_last_polled: Callable,
    ):
        self.config = config
        self._fetch_task = fetch_task
        self._fetch_prompt = fetch_prompt
        self._store_task = store_task
        self._store_prompt = store_prompt
        self._get_last_polled = get_last_polled
        self._update_last_polled = update_last_polled
        self._polling_task: asyncio.Task | None = None
        self._should_stop = False

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        reraise=True,
    )
    async def _check_task_updates(self, task_id: str) -> None:
        """Check for new versions of a task."""
        try:
            # TODO: In future, first check latest version_id via API
            task = await self._fetch_task(task_id)

            # Store only if this version isn't already stored
            await self._store_task(task)
            await self._update_last_polled(task_id, "task", datetime.utcnow())

            logger.info(f"Successfully checked task {task_id} for updates")
        except Exception as e:
            logger.error(f"Error checking updates for task {task_id}: {e}")
            raise

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        reraise=True,
    )
    async def _check_prompt_updates(self, prompt_id: str) -> None:
        """Check for new versions of a prompt."""
        try:
            # TODO: In future, first check latest version_id via API
            prompt = await self._fetch_prompt(prompt_id)

            # Store only if this version isn't already stored
            await self._store_prompt(prompt)
            await self._update_last_polled(prompt_id, "prompt", datetime.utcnow())

            logger.info(f"Successfully checked prompt {prompt_id} for updates")
        except Exception as e:
            logger.error(f"Error checking updates for prompt {prompt_id}: {e}")
            raise

    async def _poll_loop(self) -> None:
        """Main polling loop."""
        while not self._should_stop:
            try:
                # Check task updates
                for task_id in self.config.tasks_to_track:
                    await self._check_task_updates(task_id)

                # Check prompt updates
                for prompt_id in self.config.prompts_to_track:
                    await self._check_prompt_updates(prompt_id)

                await asyncio.sleep(self.config.interval)
            except Exception as e:
                logger.error(f"Error in polling loop: {e}")
                await asyncio.sleep(self.config.retry_delay)

    async def start(self) -> None:
        """Start the polling background task."""
        if self._polling_task is not None:
            logger.warning("Polling task is already running")
            return

        self._should_stop = False
        self._polling_task = asyncio.create_task(self._poll_loop())
        logger.info("Started polling task")

    async def stop(self) -> None:
        """Stop the polling background task."""
        if self._polling_task is None:
            return

        self._should_stop = True
        await self._polling_task
        self._polling_task = None
        logger.info("Stopped polling task")
