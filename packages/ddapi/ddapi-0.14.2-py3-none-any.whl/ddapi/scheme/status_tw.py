# Status.tw
from datetime import datetime
from enum import StrEnum
from typing import Optional

from pydantic import BaseModel, Field


class ChartEnum(StrEnum):
    day = "day"
    week = "week"
    month = "month"


class DataTw(BaseModel):
    name: str
    created_at: datetime = Field(alias="createdAt")


class VersionTw(BaseModel):
    version: str
    created_at: datetime = Field(alias="createdAt")


class CountryTw(BaseModel):
    identifier: str
    code: int
    icon_url: str = Field(alias="iconUrl")


class ClientTw(BaseModel):
    name: str
    country: CountryTw
    score: int
    is_player: bool = Field(alias="isPlayer")
    is_afk: bool = Field(alias="isAfk")
    team: int
    created_at: datetime = Field(alias="createdAt")
    clan: DataTw | None
    server: "ServerTw" = None


class ServerTw(BaseModel):
    ip: str
    port: int
    name: str
    num_clients: int = Field(alias="numClients")
    num_players: int = Field(alias="numPlayers")
    max_clients: int = Field(alias="maxClients")
    max_players: int = Field(alias="maxPlayers")
    has_password: bool = Field(alias="hasPassword")
    supports6: bool
    supports7: bool
    created_at: datetime = Field(alias="createdAt")
    relevance_score: int = Field(alias="relevanceScore")
    client_score_kind: str | None = Field(alias="clientScoreKind")
    logo_url: str = Field(alias="logoUrl")
    map: DataTw
    website: str | None = None
    discord_invite: str | None = Field(None, alias="discordInvite")
    description: str | None = None
    game_type: DataTw = Field(alias="gameType")
    version: VersionTw
    clients: list[ClientTw]


class ServerTwOne(BaseModel):
    ip: str
    port: int
    online: ServerTw


class Chart(BaseModel):
    avg_players: float = Field(alias="avgPlayers")
    max_players: int = Field(alias="maxPlayers")
    min_players: int = Field(alias="minPlayers")
    timestamp: datetime


class Charts(BaseModel):
    charts: list[Chart]


class MasterTw(BaseModel):
    servers: list[ServerTw]


class Info(BaseModel):
    app: str
    version: str


class BannedMasterData(BaseModel):
    ip: str
    is_active: bool = Field(alias="isActive")
    reason: str | None
    unban_date: datetime | None = Field(alias="unbanDate")
    created_at: datetime = Field(alias="createdAt")


class BannedMaster(BaseModel):
    servers: list[BannedMasterData]


class ListData(BaseModel):
    name: str
    created_at: datetime = Field(alias="createdAt")
    servers: list[ServerTw]


class List(BaseModel):
    data: list[ListData]


class ListPlData(BaseModel):
    name: str
    created_at: datetime = Field(alias="createdAt")
    players: list[ClientTw]


class ListPl(BaseModel):
    data: list[ListPlData]


class Stats(BaseModel):
    num_players: int = Field(alias="numPlayers")
    num_clans: int = Field(alias="numClans")
    num_servers: int = Field(alias="numServers")
    num_maps: int = Field(alias="numMaps")
    num_game_types: int = Field(alias="numGameTypes")
    num_versions: int = Field(alias="numVersions")
