import asyncio

from .base import CacheABC
from ddapi.types import T


class MemoryCache(CacheABC):
    async def get(self, key: str, default: T = None) -> T:
        async with self._lock:
            return self._cache.get(key, default)

    async def set(self, key: str, value: T, delay: int | None = None) -> bool:
        async with self._lock:
            self._cache[key] = value
            if delay is not None:
                if existing_task := self._remove_tasks.get(key):
                    existing_task.cancel()

                self._remove_tasks[key] = asyncio.create_task(
                    self._remove_after_sleep(key, delay)
                )
            return True

    async def delete(self, key: str) -> bool:
        async with self._lock:
            if key in self._cache:
                self._cache.pop(key, None)
                await self._remove_tasks.pop(key, None)
                if existing_task := self._remove_tasks.get(key):
                    existing_task.cancel()
                return True
            return False

    async def _remove_after_sleep(self, key: str, delay: int) -> None:
        try:
            await asyncio.sleep(delay)
            self._cache.pop(key, None)
            await self._remove_tasks.pop(key, None)
        except asyncio.CancelledError:
            pass
