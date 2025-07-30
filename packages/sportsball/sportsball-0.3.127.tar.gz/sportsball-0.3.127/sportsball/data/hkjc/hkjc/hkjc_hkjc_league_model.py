"""The HKJC league model."""

from typing import Iterator

import requests_cache

from ...game_model import GameModel
from ...league import League
from ...league_model import LeagueModel


class HKJCHKJCLeagueModel(LeagueModel):
    """HKJC HKJC implementation of the league model."""

    def __init__(
        self, session: requests_cache.CachedSession, position: int | None = None
    ) -> None:
        super().__init__(League.HKJC, session, position=position)

    @classmethod
    def name(cls) -> str:
        return "hkjc-league-model"

    @property
    def games(self) -> Iterator[GameModel]:  # type: ignore
        pass
