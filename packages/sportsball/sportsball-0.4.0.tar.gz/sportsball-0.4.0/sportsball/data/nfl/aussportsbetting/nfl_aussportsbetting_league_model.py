"""NFL aussportsbetting league model."""

import requests_cache

from ...aussportsbetting.aussportsbetting_league_model import \
    AusSportsBettingLeagueModel
from ...league import League


class NFLAusSportsBettingLeagueModel(AusSportsBettingLeagueModel):
    """NFL AusSportsBetting implementation of the league model."""

    def __init__(
        self, session: requests_cache.CachedSession, position: int | None = None
    ) -> None:
        super().__init__(League.NFL, session, position=position)

    @classmethod
    def name(cls) -> str:
        return "nfl-aussportsbetting-league-model"
