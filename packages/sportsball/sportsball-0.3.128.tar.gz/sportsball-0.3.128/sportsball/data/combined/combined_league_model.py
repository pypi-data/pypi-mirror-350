"""Combined league model."""

# pylint: disable=raise-missing-from
import logging
import multiprocessing
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Iterator

import requests_cache

from ..game_model import GameModel
from ..league import League
from ..league_model import LeagueModel
from .combined_game_model import create_combined_game_model


def _produce_league_games(league_model: LeagueModel) -> list[dict[str, Any]]:
    return [x.model_dump() for x in league_model.games]


class CombinedLeagueModel(LeagueModel):
    """The class implementing the combined league model."""

    def __init__(
        self,
        session: requests_cache.CachedSession,
        league: League,
        league_models: list[LeagueModel],
        league_filter: str | None,
    ) -> None:
        super().__init__(league, session)
        if league_filter is not None:
            league_models = [x for x in league_models if x.name() == league_filter]
        if not league_models:
            raise ValueError("No league models to run")
        self._league_models = league_models

    @classmethod
    def team_identity_map(cls) -> dict[str, str]:
        """A map to resolve the different teams identities to a consistent identity."""
        raise NotImplementedError(
            "team_identity_map not implemented on CombinedLeagueModel parent class."
        )

    @classmethod
    def venue_identity_map(cls) -> dict[str, str]:
        """A map to resolve the different venue identities to a consistent identity."""
        raise NotImplementedError(
            "venue_identity_map not implemented on CombinedLeagueModel parent class."
        )

    @classmethod
    def player_identity_map(cls) -> dict[str, str]:
        """A map to resolve the different player identities to a consistent identity."""
        return {}

    @property
    def games(self) -> Iterator[GameModel]:
        games: dict[str, list[GameModel]] = {}
        team_identity_map = self.team_identity_map()
        for league_model in self._league_models:
            league_model.clear_session()
        with ThreadPoolExecutor(
            min(multiprocessing.cpu_count(), len(self._league_models))
        ) as p:
            # We want to terminate immediately if any of our runners runs into trouble.

            results = list(
                p.map(
                    _produce_league_games,
                    self._league_models,
                )
            )
        game_lists = [[GameModel.model_validate(y) for y in x] for x in results]

        for game_list in game_lists:
            for game_model in game_list:
                game_components = [str(game_model.dt.date())]
                for team in game_model.teams:
                    if team.identifier not in team_identity_map:
                        logging.warning(
                            "%s for team %s not found in team identity map.",
                            team.identifier,
                            team.name,
                        )
                    team_identifier = team_identity_map.get(
                        team.identifier, team.identifier
                    )
                    game_components.append(team_identifier)
                game_components = sorted(game_components)
                key = "-".join(game_components)
                games[key] = games.get(key, []) + [game_model]
        names: dict[str, str] = {}
        for game_models in games.values():
            yield create_combined_game_model(  # type: ignore
                game_models,
                self.venue_identity_map(),
                team_identity_map,
                self.player_identity_map(),
                self.session,
                names,
            )
