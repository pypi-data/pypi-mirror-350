"""HKJC HKJC team model."""

# pylint: disable=duplicate-code,too-many-arguments,too-many-locals
import datetime

import pytest_is_running
import requests_cache

from ....cache import MEMORY
from ...odds_model import OddsModel
from ...team_model import TeamModel
from ..position import Position
from .hkjc_hkjc_coach_model import create_hkjc_hkjc_coach_model
from .hkjc_hkjc_player_model import create_hkjc_hkjc_player_model


def _create_hkjc_hkjc_team_model(
    session: requests_cache.CachedSession,
    horse_url: str,
    jockey_url: str,
    trainer_url: str,
    points: float,
    jersey: str,
    handicap_weight: float,
    horse_weight: float | None,
    starting_position: Position | None,
    lbw: float,
    end_dt: datetime.datetime | None,
    odds: list[OddsModel],
) -> TeamModel:
    horse_player = create_hkjc_hkjc_player_model(
        session=session,
        url=horse_url,
        jersey=jersey,
        handicap_weight=handicap_weight,
        starting_position=starting_position,
        weight=horse_weight,
    )
    jockey_player = create_hkjc_hkjc_player_model(
        session=session,
        url=jockey_url,
        jersey=jersey,
        handicap_weight=None,
        starting_position=starting_position,
        weight=None,
    )
    players = [horse_player, jockey_player]
    coach = create_hkjc_hkjc_coach_model(session=session, url=trainer_url)
    name = " - ".join([x.name for x in players])
    return TeamModel(
        identifier=name,
        name=name,
        location=None,
        players=players,
        odds=odds,
        points=points,
        ladder_rank=None,
        news=[],
        social=[],
        field_goals=None,
        coaches=[coach],
        lbw=lbw,
        end_dt=end_dt,
    )


@MEMORY.cache(ignore=["session"])
def _cached_create_hkjc_hkjc_team_model(
    session: requests_cache.CachedSession,
    horse_url: str,
    jockey_url: str,
    trainer_url: str,
    points: float,
    jersey: str,
    handicap_weight: float,
    horse_weight: float | None,
    starting_position: Position | None,
    lbw: float,
    end_dt: datetime.datetime | None,
    odds: list[OddsModel],
) -> TeamModel:
    return _create_hkjc_hkjc_team_model(
        session=session,
        horse_url=horse_url,
        jockey_url=jockey_url,
        trainer_url=trainer_url,
        points=points,
        jersey=jersey,
        handicap_weight=handicap_weight,
        horse_weight=horse_weight,
        starting_position=starting_position,
        lbw=lbw,
        end_dt=end_dt,
        odds=odds,
    )


def create_hkjc_hkjc_team_model(
    session: requests_cache.CachedSession,
    horse_url: str,
    jockey_url: str,
    trainer_url: str,
    points: float,
    jersey: str,
    handicap_weight: float,
    horse_weight: float | None,
    starting_position: Position | None,
    lbw: float,
    end_dt: datetime.datetime | None,
    odds: list[OddsModel],
) -> TeamModel:
    """Create team model from HKJC."""
    if not pytest_is_running.is_running():
        return _cached_create_hkjc_hkjc_team_model(
            session=session,
            horse_url=horse_url,
            jockey_url=jockey_url,
            trainer_url=trainer_url,
            points=points,
            jersey=jersey,
            handicap_weight=handicap_weight,
            horse_weight=horse_weight,
            starting_position=starting_position,
            lbw=lbw,
            end_dt=end_dt,
            odds=odds,
        )
    return _create_hkjc_hkjc_team_model(
        session=session,
        horse_url=horse_url,
        jockey_url=jockey_url,
        trainer_url=trainer_url,
        points=points,
        jersey=jersey,
        handicap_weight=handicap_weight,
        horse_weight=horse_weight,
        starting_position=starting_position,
        lbw=lbw,
        end_dt=end_dt,
        odds=odds,
    )
