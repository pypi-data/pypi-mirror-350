from urllib.parse import quote

from ddapi._api import API
from ddapi.scheme import (
    Info,
    BannedMaster,
    List,
    ListData,
    ListPl,
    ListPlData,
    MasterTw,
    ServerTwOne,
    Charts,
    ChartEnum,
    Stats,
)

__all__ = ("Status",)


class Status(API):
    @property
    def domain(self) -> str:
        return "status.tw"

    @staticmethod
    def powered() -> str:
        return Status().domain

    async def info(self) -> Info:
        return await self._generate_model_instance(
            f"https://api.{self.domain}/info", Info
        )

    async def master_bans(self) -> BannedMaster:
        return await self._generate_model_instance(
            f"https://api.{self.domain}/master/bans/list", BannedMaster, "servers"
        )

    async def map_list(self) -> List:
        return await self._generate_model_instance(
            f"https://api.{self.domain}/map/list", List, "data"
        )

    async def map(self, name: str) -> ListData:
        return await self._generate_model_instance(
            f"https://api.{self.domain}/map/name/{quote(name)}", ListData
        )

    async def gametype_list(self) -> List:
        return await self._generate_model_instance(
            f"https://api.{self.domain}/gametype/list", List, "data"
        )

    async def gametype(self, name: str) -> ListData:
        return await self._generate_model_instance(
            f"https://api.{self.domain}/gametype/name/{quote(name)}", ListData
        )

    async def version_list(self) -> List:
        return await self._generate_model_instance(
            f"https://api.{self.domain}/version/list", List, "data"
        )

    async def version(self, name: str) -> ListData:
        return await self._generate_model_instance(
            f"https://api.{self.domain}/version/name/{quote(name)}", ListData
        )

    async def server_list(self) -> MasterTw:
        """Fetch player data from the API and return it as a dictionary."""
        return await self._generate_model_instance(
            f"https://api.{self.domain}/server/list", MasterTw, "servers"
        )

    async def server(self, ip: str, port: int | str) -> ServerTwOne:
        return await self._generate_model_instance(
            f"https://api.{self.domain}/server/{quote(ip)}/{port}",
            ServerTwOne,
        )

    async def server_charts(
        self, ip: str, port: int | str, chart: ChartEnum = ChartEnum.day
    ) -> Charts:
        return await self._generate_model_instance(
            f"https://api.{self.domain}/server/{quote(ip)}/{port}/chart/{chart}",
            Charts,
            "charts",
        )

    async def server_history(self, ip: str, port: int | str) -> None:
        # TODO: https://api.status.tw/server/{ip}/{port}/history
        raise NotImplementedError

    async def server_stats(self, ip: str, port: int | str) -> None:
        # TODO: https://api.status.tw/server/{ip}/{port}/stats
        raise NotImplementedError

    async def clan_list(self) -> ListPl:
        return await self._generate_model_instance(
            f"https://api.{self.domain}/clan/list", ListPl, "data"
        )

    async def clan(self, name: str) -> ListPlData:
        return await self._generate_model_instance(
            f"https://api.{self.domain}/clan/name/{quote(name)}", ListPlData
        )

    async def player_list(self) -> ListPl:
        return await self._generate_model_instance(
            f"https://api.{self.domain}/player/list", ListPl, "data"
        )

    async def player(self, name: str) -> ListPlData:
        return await self._generate_model_instance(
            f"https://api.{self.domain}/player/name/{quote(name)}", ListPlData
        )

    async def player_history(self, name: str) -> None:
        # TODO:  https://api.status.tw/player/name/{name}/history
        raise NotImplementedError

    async def stats(self) -> Stats:
        return await self._generate_model_instance(
            f"https://api.{self.domain}/stats", Stats
        )

    async def stats_players(self, t: str) -> None:
        # TODO: https://api.status.tw/stats/players/day | week | month
        raise NotImplementedError

    async def stats_servers(self, t: str) -> None:
        # TODO:  https://api.status.tw/stats/servers/week | month
        raise NotImplementedError
