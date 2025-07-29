# ddstats.tw
from datetime import datetime
from typing import Optional
from urllib.parse import quote

from pydantic import BaseModel, Field


class PData(BaseModel):
    rank: int
    points: int


class PPoints(BaseModel):
    Novice: PData | None = None
    Moderate: PData | None = None
    Brutal: PData | None = None
    Insane: PData | None = None
    Dummy: PData | None = None
    DDmaX_Easy: PData | None = Field(default=None, validation_alias="DDmaX.Easy")
    DDmaX_Next: PData | None = Field(default=None, validation_alias="DDmaX.Next")
    DDmaX_Nut: PData | None = Field(default=None, validation_alias="DDmaX.Nut")
    DDmaX_Pro: PData | None = Field(default=None, validation_alias="DDmaX.Pro")
    Oldschool: PData | None = None
    Race: PData | None = None
    Solo: PData | None = None
    total: PData | None = None


class PointG(BaseModel):
    date: str
    points: int
    rank_points: int
    team_points: int


class Profile(BaseModel):
    name: str
    points: int
    clan: str | None
    country: int | None
    skin_name: str | None
    skin_color_body: int | None = None
    skin_color_feet: int | None = None


class DProfile(BaseModel):
    profile: Profile

    def url(self) -> str:
        return f"https://ddstats.tw/player/{quote(self.name)}"

    @staticmethod
    def url_with_name(player: str) -> str:
        return f"https://ddstats.tw/player/{quote(player)}"

    @staticmethod
    def api(player: str) -> str:
        return f"https://ddstats.tw/profile/json?player={quote(player)}"


class DDMap(BaseModel):
    map: str
    server: str
    points: int
    stars: int
    mapper: str
    timestamp: datetime | None = None


class RecentFinishes(BaseModel):
    map: DDMap
    time: float
    timestamp: datetime
    server: str
    cp1: float
    cp2: float
    cp3: float
    cp4: float
    cp5: float
    cp6: float
    cp7: float
    cp8: float
    cp9: float
    cp10: float
    cp11: float
    cp12: float
    cp13: float
    cp14: float
    cp15: float
    cp16: float
    cp17: float
    cp18: float
    cp19: float
    cp20: float
    cp21: float
    cp22: float
    cp23: float
    cp24: float
    cp25: float


class FavouriteTeammates(BaseModel):
    name: str
    ranks_together: int


class Finishes(BaseModel):
    map: DDMap
    name: str
    time: float
    timestamp: datetime | None
    server: str
    rank: int
    team_rank: int | None = None
    seconds_played: int | None = None


class UnfinishedMap(BaseModel):
    map: DDMap
    finishes: int
    finishes_rank: int | None = None
    median_time: float | None = None


class Points(BaseModel):
    weekly_points: PData | None = None
    monthly_points: PData | None = None
    yearly_points: PData | None = None
    points: PPoints
    rank_points: PPoints
    team_points: PPoints


class RecentActivity(BaseModel):
    name: str
    date: str
    map_name: str
    map: DDMap | None = Field(default=None)
    seconds_played: int


class RecentPlayerInfo(BaseModel):
    name: str
    clan: str
    country: int
    skin_name: str | None = None
    skin_color_body: int | None = None
    skin_color_feet: int | None = None
    last_seen: str
    seconds_played: int


class MostPlayedMaps(BaseModel):
    map_name: str
    seconds_played: int
    map: DDMap | None = None


class MostPlayed(BaseModel):
    key: str
    seconds_played: int


class PlaytimePerMonth(BaseModel):
    year_month: str
    month: str
    seconds_played: int


class FavouriteRank1sTeammates(BaseModel):
    name: str
    ranks_together: int


class AllTop10s(BaseModel):
    map: DDMap
    name: str
    time: float
    rank: int
    team_rank: int | None = None
    team_time: float | None = None


class RecentTop10s(BaseModel):
    rank_type: str
    map: str
    time: float
    rank: int
    timestamp: datetime | None = None
    server: str


class GeneralActivity(BaseModel):
    total_seconds_played: int
    start_of_playtime: datetime
    average_seconds_played: int


class Player(BaseModel):
    points_graph: list[PointG]
    recent_finishes: list[RecentFinishes]
    favourite_teammates: list[FavouriteTeammates] | None = None
    profile: Profile
    is_mapper: bool
    finishes: list[Finishes]
    unfinished_maps: list[UnfinishedMap] | None = None
    points: Points
    recent_activity: list[RecentActivity] | None = None
    recent_player_info: list[RecentPlayerInfo] | None = None
    most_played_maps: list[MostPlayedMaps] | None = None
    most_played_gametypes: list[MostPlayed] | None = None
    most_played_categories: list[MostPlayed] | None = None
    most_played_locations: list[MostPlayed] | None = None
    playtime_per_month: list[PlaytimePerMonth]
    general_activity: GeneralActivity | None = None
    favourite_rank1s_teammates: list[FavouriteRank1sTeammates] | None = None
    all_top_10s: list[AllTop10s] | None = None
    recent_top_10s: list[RecentTop10s] | None = None

    def url(self) -> str:
        return f"https://ddstats.tw/player/{quote(self.profile.name)}"

    @staticmethod
    def url_with_name(player: str) -> str:
        return f"https://ddstats.tw/player/{quote(player)}"

    @staticmethod
    def api(player: str) -> str:
        return f"https://ddstats.tw/player/json?player={quote(player)}"


class Maps(BaseModel):
    maps: list[DDMap]

    @staticmethod
    def api() -> str:
        return "https://ddstats.tw/maps/json"


class InfoSMap(BaseModel):
    map: DDMap
    finishes: int
    finishes_rank: int
    median_time: float


class RankingSMap(BaseModel):
    rank: int
    timestamp: datetime | None = None
    name: str
    time: float
    map: str
    server: str


class TeamRankingSMap(BaseModel):
    rank: int
    timestamp: datetime | None = None
    id: list[int]
    players: list[str]
    time: float
    map: str
    server: str


class TimeCpsSMap(BaseModel):
    name: str
    cp1: float
    cp2: float
    cp3: float
    cp4: float
    cp5: float
    cp6: float
    cp7: float
    cp8: float
    cp9: float
    cp10: float
    cp11: float
    cp12: float
    cp13: float
    cp14: float
    cp15: float
    cp16: float
    cp17: float
    cp18: float
    cp19: float
    cp20: float
    cp21: float
    cp22: float
    cp23: float
    cp24: float
    cp25: float
    time: float


class PlaytimeSMap(BaseModel):
    name: str
    seconds_played: int


class SMap(BaseModel):
    info: InfoSMap
    rankings: list[RankingSMap]
    team_rankings: list[TeamRankingSMap]
    time_cps: list[TimeCpsSMap]
    playtime: list[PlaytimeSMap]

    def url(self) -> str:
        return f"https://ddstats.tw/map/{quote(self.info.map.map)}"

    @staticmethod
    def url_with_name(map_name: str) -> str:
        return f"https://ddstats.tw/map/{quote(map_name)}"

    @staticmethod
    def api(map_name: str) -> str:
        return f"https://ddstats.tw/map/json?map={quote(map_name)}"
