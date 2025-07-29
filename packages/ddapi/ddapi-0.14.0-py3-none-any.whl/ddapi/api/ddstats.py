from urllib.parse import quote

from ddapi._api import API
from ddapi.scheme import (
    DProfile,
    SMap,
    Maps,
    Player,
)

__all__ = ("DDstats",)


class DDstats(API):
    @property
    def domain(self) -> str:
        return "ddstats.tw"

    @staticmethod
    def powered() -> str:
        return DDstats().domain

    async def profile(self, player: str) -> DProfile:
        return await self._generate_model_instance(
            DProfile.api(player),
            DProfile,
            "profile",
        )

    async def map(self, map_name: str) -> SMap:
        return await self._generate_model_instance(SMap.api(map_name), SMap)

    async def maps(self) -> Maps:
        return await self._generate_model_instance(Maps.api(), Maps, "maps")

    async def player(self, player: str) -> Player:
        """Fetch player data from the API and return it as a dictionary."""
        return await self._generate_model_instance(Player.api(player), Player)
