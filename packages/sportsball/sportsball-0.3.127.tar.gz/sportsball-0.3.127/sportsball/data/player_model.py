"""The prototype class for a player."""

import datetime
from typing import Literal

from pydantic import BaseModel, Field

from .field_type import TYPE_KEY, FieldType

PLAYER_KICKS_COLUMN: Literal["kicks"] = "kicks"
PLAYER_IDENTIFIER_COLUMN: Literal["identifier"] = "identifier"
PLAYER_FUMBLES_COLUMN: Literal["fumbles"] = "fumbles"
PLAYER_FUMBLES_LOST_COLUMN: Literal["fumbles_lost"] = "fumbles_lost"
FIELD_GOALS_COLUMN: Literal["field_goals"] = "field_goals"
FIELD_GOALS_ATTEMPTED_COLUMN: Literal["field_goals_attempted"] = "field_goals_attempted"
OFFENSIVE_REBOUNDS_COLUMN: Literal["offensive_rebounds"] = "offensive_rebounds"
ASSISTS_COLUMN: Literal["assists"] = "assists"
TURNOVERS_COLUMN: Literal["turnovers"] = "turnovers"
PLAYER_MARKS_COLUMN: Literal["marks"] = "marks"
PLAYER_HANDBALLS_COLUMN: Literal["handballs"] = "handballs"
PLAYER_DISPOSALS_COLUMN: Literal["disposals"] = "disposals"
PLAYER_GOALS_COLUMN: Literal["goals"] = "goals"
PLAYER_BEHINDS_COLUMN: Literal["behinds"] = "behinds"
PLAYER_HIT_OUTS_COLUMN: Literal["hit_outs"] = "hit_outs"
PLAYER_TACKLES_COLUMN: Literal["tackles"] = "tackles"
PLAYER_REBOUNDS_COLUMN: Literal["rebounds"] = "rebounds"
PLAYER_INSIDES_COLUMN: Literal["insides"] = "insides"
PLAYER_CLEARANCES_COLUMN: Literal["clearances"] = "clearances"
PLAYER_CLANGERS_COLUMN: Literal["clangers"] = "clangers"
PLAYER_FREE_KICKS_FOR_COLUMN: Literal["free_kicks_for"] = "free_kicks_for"
PLAYER_FREE_KICKS_AGAINST_COLUMN: Literal["free_kicks_against"] = "free_kicks_against"
PLAYER_BROWNLOW_VOTES_COLUMN: Literal["brownlow_votes"] = "brownlow_votes"
PLAYER_CONTESTED_POSSESSIONS_COLUMN: Literal["contested_possessions"] = (
    "contested_possessions"
)
PLAYER_UNCONTESTED_POSSESSIONS_COLUMN: Literal["uncontested_possessions"] = (
    "uncontested_possessions"
)
PLAYER_CONTESTED_MARKS_COLUMN: Literal["contested_marks"] = "contested_marks"
PLAYER_MARKS_INSIDE_COLUMN: Literal["marks_inside"] = "marks_inside"
PLAYER_ONE_PERCENTERS_COLUMN: Literal["one_percenters"] = "one_percenters"
PLAYER_BOUNCES_COLUMN: Literal["bounces"] = "bounces"
PLAYER_GOAL_ASSISTS_COLUMN: Literal["goal_assists"] = "goal_assists"
PLAYER_PERCENTAGE_PLAYED_COLUMN: Literal["percentage_played"] = "percentage_played"
PLAYER_NAME_COLUMN: Literal["name"] = "name"
PLAYER_BIRTH_DATE_COLUMN: Literal["birth_date"] = "birth_date"


class PlayerModel(BaseModel):
    """The serialisable player class."""

    identifier: str = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.CATEGORICAL},
        alias=PLAYER_IDENTIFIER_COLUMN,
    )
    jersey: str | None = Field(..., json_schema_extra={TYPE_KEY: FieldType.CATEGORICAL})
    kicks: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_KICKS_COLUMN,
    )
    fumbles: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_FUMBLES_COLUMN,
    )
    fumbles_lost: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_FUMBLES_LOST_COLUMN,
    )
    field_goals: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=FIELD_GOALS_COLUMN,
    )
    field_goals_attempted: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=FIELD_GOALS_ATTEMPTED_COLUMN,
    )
    offensive_rebounds: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=OFFENSIVE_REBOUNDS_COLUMN,
    )
    assists: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=ASSISTS_COLUMN,
    )
    turnovers: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=TURNOVERS_COLUMN,
    )
    name: str = Field(..., alias=PLAYER_NAME_COLUMN)
    marks: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_MARKS_COLUMN,
    )
    handballs: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_HANDBALLS_COLUMN,
    )
    disposals: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_DISPOSALS_COLUMN,
    )
    goals: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_GOALS_COLUMN,
    )
    behinds: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_BEHINDS_COLUMN,
    )
    hit_outs: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_HIT_OUTS_COLUMN,
    )
    tackles: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_TACKLES_COLUMN,
    )
    rebounds: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_REBOUNDS_COLUMN,
    )
    insides: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_INSIDES_COLUMN,
    )
    clearances: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_CLEARANCES_COLUMN,
    )
    clangers: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_CLANGERS_COLUMN,
    )
    free_kicks_for: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_FREE_KICKS_FOR_COLUMN,
    )
    free_kicks_against: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_FREE_KICKS_AGAINST_COLUMN,
    )
    brownlow_votes: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_BROWNLOW_VOTES_COLUMN,
    )
    contested_possessions: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_CONTESTED_POSSESSIONS_COLUMN,
    )
    uncontested_possessions: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_UNCONTESTED_POSSESSIONS_COLUMN,
    )
    contested_marks: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_CONTESTED_MARKS_COLUMN,
    )
    marks_inside: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_MARKS_INSIDE_COLUMN,
    )
    one_percenters: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_ONE_PERCENTERS_COLUMN,
    )
    bounces: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_BOUNCES_COLUMN,
    )
    goal_assists: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_GOAL_ASSISTS_COLUMN,
    )
    percentage_played: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_PERCENTAGE_PLAYED_COLUMN,
    )
    birth_date: datetime.date | None = Field(..., alias=PLAYER_BIRTH_DATE_COLUMN)
