"""ESPN team model."""

# pylint: disable=too-many-arguments,too-many-locals,duplicate-code

import datetime
from typing import Any

import pytest_is_running
import requests_cache

from ...cache import MEMORY
from ..google.google_news_model import create_google_news_models
from ..league import League
from ..odds_model import OddsModel
from ..team_model import TeamModel
from ..x.x_social_model import create_x_social_model
from .espn_coach_model import create_espn_coach_model
from .espn_player_model import create_espn_player_model


def _create_espn_team_model(
    session: requests_cache.CachedSession,
    team: dict[str, Any],
    roster_dict: dict[str, Any],
    odds: list[OddsModel],
    score_dict: dict[str, Any],
    dt: datetime.datetime,
    league: League,
    positions_validator: dict[str, str],
) -> TeamModel:
    identifier = team["id"]
    name = team.get("name", team.get("fullName", team.get("displayName")))
    if name is None:
        raise ValueError("name is null")
    location = team["location"]
    players = []
    for entity in roster_dict.get("entries", []):
        player = create_espn_player_model(session, entity, dt, positions_validator)
        players.append(player)
    points = score_dict["value"]
    coaches_response = session.get(team["coaches"]["$ref"])
    coaches_response.raise_for_status()
    coaches_urls = [x["$ref"] for x in coaches_response.json()["items"]]
    return TeamModel(
        identifier=identifier,
        name=name,
        location=location,
        players=players,
        odds=odds,
        points=points,
        ladder_rank=None,
        news=create_google_news_models(name, session, dt, league),
        social=create_x_social_model(identifier, session, dt),
        field_goals=None,
        coaches=[create_espn_coach_model(session, dt, x) for x in coaches_urls],
        lbw=None,
        end_dt=None,
    )


@MEMORY.cache(ignore=["session"])
def _cached_create_espn_team_model(
    session: requests_cache.CachedSession,
    team: dict[str, Any],
    roster_dict: dict[str, Any],
    odds: list[OddsModel],
    score_dict: dict[str, Any],
    dt: datetime.datetime,
    league: League,
    positions_validator: dict[str, str],
) -> TeamModel:
    return _create_espn_team_model(
        session, team, roster_dict, odds, score_dict, dt, league, positions_validator
    )


def create_espn_team_model(
    session: requests_cache.CachedSession,
    team: dict[str, Any],
    roster_dict: dict[str, Any],
    odds: list[OddsModel],
    score_dict: dict[str, Any],
    dt: datetime.datetime,
    league: League,
    positions_validator: dict[str, str],
) -> TeamModel:
    """Create team model from ESPN."""
    if (
        not pytest_is_running.is_running()
        and dt < datetime.datetime.now() - datetime.timedelta(days=7)
    ):
        return _cached_create_espn_team_model(
            session,
            team,
            roster_dict,
            odds,
            score_dict,
            dt,
            league,
            positions_validator,
        )
    with session.cache_disabled():
        return _create_espn_team_model(
            session,
            team,
            roster_dict,
            odds,
            score_dict,
            dt,
            league,
            positions_validator,
        )
