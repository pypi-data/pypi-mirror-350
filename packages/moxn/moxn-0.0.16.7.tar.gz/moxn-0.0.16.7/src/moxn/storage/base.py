from abc import ABC, abstractmethod
from typing import TypeVar

from moxn.models.prompt import PromptTemplate
from moxn.models.task import Task

T = TypeVar("T", Task, PromptTemplate)


class StorageBackend(ABC):
    """Abstract base class for storage backends."""

    @abstractmethod
    async def store_task(self, task: Task) -> None:
        """Store a task version."""
        pass

    @abstractmethod
    async def store_prompt(self, prompt: PromptTemplate) -> None:
        """Store a prompt version."""
        pass

    @abstractmethod
    async def get_task(self, task_id: str, version_id: str) -> Task:
        """Retrieve a task version."""
        pass

    @abstractmethod
    async def get_prompt(self, prompt_id: str, version_id: str) -> PromptTemplate:
        """Retrieve a prompt version."""
        pass

    @abstractmethod
    async def has_task_version(self, task_id: str, version_id: str) -> bool:
        """Check if a task version exists."""
        pass

    @abstractmethod
    async def has_prompt_version(self, prompt_id: str, version_id: str) -> bool:
        """Check if a prompt version exists."""
        pass

    @abstractmethod
    async def clear(self) -> None:
        """Clear all stored data."""
        pass
