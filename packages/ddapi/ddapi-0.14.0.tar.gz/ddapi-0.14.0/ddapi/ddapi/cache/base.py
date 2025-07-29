import asyncio
from abc import ABC, abstractmethod
from typing import Generic

from ddapi.types import T


class CacheABC(ABC, Generic[T]):
    def __init__(self) -> None:
        self._cache = {}
        self._lock = asyncio.Lock()
        self._remove_tasks: dict[str, asyncio.Task] = {}

    @abstractmethod
    async def get(self, key: str, default: T = None) -> T:
        return default

    @abstractmethod
    async def set(self, key: str, value: T, delay: int | None = None) -> bool:
        return True

    @abstractmethod
    def delete(self, key: str) -> bool:
        return True

    async def get_or_set(self, key: str, value: T = None) -> T:
        result = await self.get(key)
        if result is not None:
            return result

        await self.set(key, value)
        return value

    async def exists(self, key: str) -> bool:
        return await self.get(key) is not None
