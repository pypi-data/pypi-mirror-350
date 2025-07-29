# ddnet
from collections import Counter
from datetime import datetime
from urllib.parse import quote

from pydantic import BaseModel, Field

from ddapi import slugify2
from ddapi.enum import MasterEnum

rm_list = ["DD-Persian", "/vDQMHSss8W", ""]


class DRank(BaseModel):
    points: int | None = None
    rank: int | None = None


class DPoints(BaseModel):
    total: int
    points: int | None = Field(default=None)
    rank: int | None = Field(default=None)


class DData(BaseModel):
    points: DPoints | None = Field(default=None)
    team_rank: DRank | None = Field(default=None)
    rank: DRank | None = Field(default=None)
    maps: dict | None = Field(default=None)


class DDType(BaseModel):
    Novice: DData | None = None
    Moderate: DData | None = None
    Brutal: DData | None = None
    Insane: DData | None = None
    Dummy: DData | None = None
    DDmaX_Easy: DData | None = Field(default=None, validation_alias="DDmaX.Easy")
    DDmaX_Next: DData | None = Field(default=None, validation_alias="DDmaX.Next")
    DDmaX_Nut: DData | None = Field(default=None, validation_alias="DDmaX.Nut")
    DDmaX_Pro: DData | None = Field(default=None, validation_alias="DDmaX.Pro")
    Oldschool: DData | None = Field(default=None)
    Race: DData | None = None
    Solo: DData | None = None
    total: DData | None = None


class MaxFinishes(BaseModel):
    rank: int
    player: str
    num: int
    time: float
    min_timestamp: int
    max_timestamp: int


class DDRanks(BaseModel):
    rank: int
    player: str
    time: float
    timestamp: int
    country: str


class DDTeamRanks(BaseModel):
    rank: int
    players: list[str]
    time: float
    timestamp: int
    country: str


class DMap(BaseModel):
    name: str
    website: str
    thumbnail: str
    web_preview: str
    type: str
    points: int
    difficulty: int
    mapper: str
    release: int | None = None
    median_time: float
    first_finish: int
    last_finish: int
    finishes: int
    finishers: int
    biggest_team: int
    width: int
    height: int
    tiles: list[str]
    team_ranks: list[DDTeamRanks]
    ranks: list[DDRanks]
    max_finishes: list[MaxFinishes]

    def url(self) -> str:
        return f"https://ddnet.org/maps/{quote(slugify2(self.name))}"

    @staticmethod
    def url_with_name(map_name: str) -> str:
        return f"https://ddnet.org/maps/{quote(slugify2(map_name))}"

    @staticmethod
    def api(map_name: str) -> str:
        return f"https://ddnet.org/maps/?json={quote(map_name)}"


class FirstFinish(BaseModel):
    timestamp: float
    map: str
    time: float


class LastFinish(BaseModel):
    timestamp: float
    map: str
    time: float
    country: str
    type: str | None = None


class FavoritePartner(BaseModel):
    name: str
    finishes: int


class Activity(BaseModel):
    date: str
    hours_played: int


class FavoriteServer(BaseModel):
    server: str


class DDPlayer(BaseModel):
    player: str
    points: DPoints
    team_rank: DRank | None = None
    rank: DRank | None = None
    points_last_year: DRank | None = None
    points_last_month: DRank | None = None
    points_last_week: DRank | None = None
    favorite_server: FavoriteServer
    first_finish: FirstFinish
    last_finishes: list[LastFinish]
    favorite_partners: list[FavoritePartner] | None = None
    types: DDType
    activity: list[Activity]
    hours_played_past_365_days: int

    def url(self) -> str:
        return f"https://ddnet.org/players/{quote(slugify2(self.player))}"

    @staticmethod
    def url_with_name(player: str) -> str:
        return f"https://ddnet.org/players/{quote(slugify2(player))}"

    @staticmethod
    def api(player: str) -> str:
        return f"https://ddnet.org/players/?json2={quote(player)}"


class Skin(BaseModel):
    name: str | None = None
    color_body: int | None = None
    color_feet: int | None = None


class Client(BaseModel):
    name: str
    clan: str
    country: int
    score: int
    is_player: bool | None = None
    skin: Skin | None = None
    afk: bool | None = None
    team: int | None = None


class Map(BaseModel):
    name: str
    sha256: str | None = None
    size: int | None = None


class Community(BaseModel):
    id: str
    icon: str
    admin: list[str]
    public_key: str | None = None
    signature: str | None = None


class Info(BaseModel):
    max_clients: int = None
    max_players: int = None
    passworded: bool = None
    game_type: str = None
    name: str = None
    map: Map = None
    version: str = None
    clients: list[Client] | None = None
    requires_login: bool | None = None
    community: Community | None = None

    def __len__(self) -> int:
        return len(self.clients)


class Server(BaseModel):
    addresses: list | str
    location: str = Field(default=None)
    info: Info

    def __len__(self) -> int:
        return self.count_client

    @property
    def count_client(self) -> int:
        if self.info.clients is not None:
            return len(self.info.clients)
        return 0


class CountServers(BaseModel):
    name: str
    address: str
    game_type: str
    count_clients: int


class Master(BaseModel):
    servers: list[Server]

    def __len__(self) -> int:
        return len(self.servers)

    def get_clans(
        self, rm: list[str] | None = None
    ) -> list[str] | list[tuple[str, int]]:
        remove_list = rm_list.copy() if rm is None else rm
        if not self.servers:
            return []

        dat: Counter[str] = Counter(
            client.clan
            for server in self.servers
            for client in server.info.clients
            if client != ""
        )

        for i in remove_list:
            del dat[i]
        return sorted(dat.items(), key=lambda x: x[1], reverse=True)

    @property
    def count_servers(self) -> list[CountServers]:
        return sorted(
            (
                CountServers(
                    count_clients=i.count_client,
                    address=i.addresses[0],
                    game_type=i.info.game_type,
                    name=i.info.name,
                )
                if isinstance(i.addresses, list)
                else CountServers(
                    count_clients=i.count_client,
                    address=i.addresses,
                    game_type=i.info.game_type,
                    name=i.info.name,
                )
                for i in self.servers
            ),
            key=lambda x: x.count_clients,
            reverse=True,
        )

    @property
    def count_clients(self) -> int:
        return sum(i.count_client for i in self.servers)

    @staticmethod
    def api(server: MasterEnum) -> str:
        return f"https://master{server}.ddnet.org/ddnet/15/servers.json"


class ReleasesMapsData(BaseModel):
    name: str
    website: str
    thumbnail: str
    web_preview: str
    type: str
    points: int
    difficulty: int
    mapper: str
    release: datetime | str
    width: int = None
    height: int = None
    tiles: list[str] = None


class ReleasesMaps(BaseModel):
    maps: list[ReleasesMapsData]

    @staticmethod
    def url() -> str:
        return "https://ddnet.org/releases"

    @staticmethod
    def api() -> str:
        return "https://ddnet.org/releases/maps.json"


class QueryData(BaseModel):
    points: int
    name: str


class Query(BaseModel):
    players: list[QueryData]

    @staticmethod
    def api(player: str) -> str:
        return f"https://ddnet.org/players/?query={quote(player)}"


class QueryMapperData(BaseModel):
    mapper: str
    num_maps: int


class QueryMapper(BaseModel):
    players: list[QueryMapperData]

    @staticmethod
    def api(player: str) -> str:
        return f"https://ddnet.org/maps/?qmapper={quote(player)}"


class QueryMapData(BaseModel):
    name: str
    type: str
    mapper: str


class QueryMap(BaseModel):
    maps: list[QueryMapData]

    @staticmethod
    def api(map_name: str) -> str:
        return f"https://ddnet.org/maps/?query={quote(map_name)}"


class DDStatusData(BaseModel):
    name: str = None
    type: str = None
    host: str = None
    location: str = None
    online4: bool = None
    online6: bool = None
    uptime: str = None
    load: float = None
    network_rx: int = None
    network_tx: int = None
    packets_rx: int = None
    packets_tx: int = None
    cpu: int = None
    memory_total: int = None
    memory_used: int = None
    swap_total: int = None
    swap_used: int = None
    hdd_total: int = None
    hdd_used: int = None


class DDStatus(BaseModel):
    servers: list[DDStatusData]

    @staticmethod
    def url() -> str:
        return "https://ddnet.org/status"

    @staticmethod
    def api() -> str:
        return "https://ddnet.org/status/json/stats.json"
