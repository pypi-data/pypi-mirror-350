from collections import defaultdict
from datetime import datetime
from typing import Literal

from moxn.models.prompt import PromptTemplate
from moxn.models.task import Task
from moxn.storage.base import StorageBackend


class InMemoryStorage(StorageBackend):
    def __init__(self):
        self._tasks: dict[str, dict[str, Task]] = defaultdict(dict)
        self._prompts: dict[str, dict[str, PromptTemplate]] = defaultdict(dict)
        self._last_polled: dict[tuple[str, Literal["task", "prompt"]], datetime] = {}

    async def store_task(self, task: Task) -> None:
        """Store a task version if not already stored."""
        task_id = str(task.id)  # Convert UUID to string if needed
        version_id = str(task.version_id)  # Convert UUID to string if needed
        if version_id not in self._tasks[task_id]:
            self._tasks[task_id][version_id] = task.model_copy(deep=True)

    async def store_prompt(self, prompt: PromptTemplate) -> None:
        """Store a prompt version if not already stored."""
        prompt_id = str(prompt.id)  # Convert UUID to string if needed
        version_id = str(prompt.version_id)  # Convert UUID to string if needed
        if version_id not in self._prompts[prompt_id]:
            self._prompts[prompt_id][version_id] = prompt.model_copy(deep=True)

    async def get_task(self, task_id: str, version_id: str | None) -> Task:
        try:
            if version_id:
                return self._tasks[task_id][version_id]
            else:
                # Sort versions by created_at and return the latest
                return max(
                    self._tasks[task_id].values(), key=lambda task: task.created_at
                ).model_copy(deep=True)
        except KeyError as e:
            raise KeyError(f"Task not found: {task_id} version: {version_id}") from e

    async def get_prompt(
        self, prompt_id: str, version_id: str | None
    ) -> PromptTemplate:
        try:
            if version_id:
                return self._prompts[prompt_id][version_id]
            else:
                # Sort versions by created_at and return the latest
                return max(
                    self._prompts[prompt_id].values(),
                    key=lambda prompt: prompt.created_at,
                ).model_copy(deep=True)
        except KeyError as e:
            raise KeyError(
                f"Prompt not found: {prompt_id} version: {version_id}"
            ) from e

    async def has_task_version(self, task_id: str, version_id: str) -> bool:
        return task_id in self._tasks and version_id in self._tasks[task_id]

    async def has_prompt_version(self, prompt_id: str, version_id: str) -> bool:
        return prompt_id in self._prompts and version_id in self._prompts[prompt_id]

    async def clear(self) -> None:
        self._tasks.clear()
        self._prompts.clear()

    async def get_last_polled(
        self, item_id: str, item_type: Literal["task", "prompt"]
    ) -> datetime | None:
        """Get the last time an item was polled for updates."""
        return self._last_polled.get((item_id, item_type))

    async def update_last_polled(
        self, item_id: str, item_type: Literal["task", "prompt"], timestamp: datetime
    ) -> None:
        """Update the last polled time for an item."""
        self._last_polled[(item_id, item_type)] = timestamp
