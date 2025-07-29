from .base import CacheABC
from ddapi.types import T


class EmptyCache(CacheABC):
    async def get(self, key: str, default: T = None) -> T:  # noqa: ARG002
        return default

    async def set(self, key: str, value: T, delay: int | None = None) -> bool:  # noqa: ARG002
        return True

    def delete(self, key: str) -> bool:  # noqa: ARG002
        return True
