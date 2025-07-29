from ddapi._api import API
from ddapi.scheme import (
    DDPlayer,
    DDStatus,
    ReleasesMaps,
    Query,
    QueryMap,
    QueryMapper,
    Master,
    DMap,
)

__all__ = ("DDnetApi",)

from ddapi.enum import MasterEnum


class DDnetApi(API):
    @property
    def domain(self) -> str:
        return "ddnet.org"

    @staticmethod
    def powered() -> str:
        return DDnetApi().domain

    async def player(self, player: str) -> DDPlayer:
        """Fetch player data from the API and return it as a dictionary."""
        return await self._generate_model_instance(DDPlayer.api(player), DDPlayer)

    async def status(self) -> DDStatus:
        return await self._generate_model_instance(DDStatus.api(), DDStatus)

    async def releases_map(self) -> ReleasesMaps:
        return await self._generate_model_instance(
            ReleasesMaps.api(), ReleasesMaps, "maps"
        )

    async def query(self, player: str) -> Query:
        return await self._generate_model_instance(Query.api(player), Query, "players")

    async def query_map(self, map_name: str) -> QueryMap:
        return await self._generate_model_instance(
            QueryMap.api(map_name), QueryMap, "maps"
        )

    async def query_mapper(self, player: str) -> QueryMapper:
        return await self._generate_model_instance(
            QueryMapper.api(player), QueryMapper, "players"
        )

    async def master(self, master: MasterEnum = MasterEnum.master1) -> Master:
        return await self._generate_model_instance(Master.api(master), Master)

    async def map(self, map_name: str) -> DMap:
        return await self._generate_model_instance(DMap.api(map_name), DMap)
