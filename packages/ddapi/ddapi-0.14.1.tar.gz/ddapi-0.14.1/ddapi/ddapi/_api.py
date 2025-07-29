import asyncio
import atexit
import logging
from http import HTTPStatus
from json import JSONDecoder
from typing import Optional

import aiohttp
from aiohttp import ClientSession

from ddapi.cache import CacheABC, EmptyCache
from ddapi.types import T

try:
    import orjson

    DEFAULT_JSON_DECODER = orjson.loads
except ImportError:
    from aiohttp.typedefs import DEFAULT_JSON_DECODER

logger = logging.getLogger(__name__)


class API:
    def __init__(
        self,
        session: ClientSession = None,
        *,
        autoclose: bool = True,
        cache: CacheABC = None,
        json_loads: JSONDecoder = DEFAULT_JSON_DECODER,
    ) -> None:
        self.__session = session
        self.cache = cache or EmptyCache()
        self.json_loads = json_loads
        self.autoclose = autoclose

        if self.__session is None:
            self.__session = aiohttp.ClientSession()

        atexit.register(self.close_api)

    async def __aenter__(self) -> "API":
        if self.__session is None:
            self.__session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, _exc_type, _exc_val, _exc_tb) -> None:  # noqa: ANN001
        if self.autoclose:
            await self.close()

    async def _get(self, url: str) -> dict | None:
        """Send a GET request to the given URL and return the response as JSON."""
        logger.debug("Sending GET request to %s.", url)
        async with self.__session.get(url) as req:
            if req.status == HTTPStatus.OK.value:
                logger.debug("Received response from %s: %s.", url, req.status)
                return await req.json(loads=self.json_loads)
            logger.error("Failed to get response from %s: %s.", url, req.status)
            return None

    async def _generate_model_instance(
        self,
        url: str,
        model: type[T],
        k: str | None = None,
        cache_timeout: int = 300,
    ) -> T | None:
        """Generate a model instance from the given URL and optional keyword arguments.

        Args:
            url (str): The URL to fetch data from.
            model (Type[ModelType]): The model class to instantiate.
            k (str, optional): An optional keyword to wrap the data in a dictionary.

        Returns:
            Optional[ModelType]: A model instance.
        """
        cache = await self.cache.get(url)
        if cache is not None:
            return cache

        dat = await self._get(url)
        if dat is None or not dat:
            logger.warning("No data received from %s.", url)
            return None

        data = model(**{k: dat} if k is not None else dat)
        await self.cache.set(url, data, cache_timeout)
        return data

    async def is_closed(self) -> bool:
        """True is closed, False otherwise."""
        return self.__session is None or self.__session.closed

    async def close(self) -> None:
        """Close the aiohttp session."""
        if self.__session is not None:
            await self.__session.close()
        self.__session = None
        self.cache = None

    @property
    def domain(self) -> str:
        return ""

    @staticmethod
    def powered() -> None:
        return None

    def close_api(self) -> None:
        asyncio.run(self.close())
