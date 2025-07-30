"""Combined team model."""

# pylint: disable=too-many-locals
import re
import unicodedata

from ..news_model import NewsModel
from ..odds_model import OddsModel
from ..player_model import PlayerModel
from ..social_model import SocialModel
from ..team_model import TeamModel
from .combined_player_model import create_combined_player_model
from .null_check import is_null

REGEX = re.compile("[^a-zA-Z]")


def _normalise_player_name(name: str) -> str:
    # Handle "Surname, Firstname"
    if "," in name:
        name = " ".join(reversed([x.strip() for x in name.split(",")]))
    return REGEX.sub("", unicodedata.normalize("NFC", name).lower().strip())


def create_combined_team_model(
    team_models: list[TeamModel],
    identifier: str,
    player_identity_map: dict[str, str],
    names: dict[str, str],
) -> TeamModel:
    """Create a team model by combining many team models."""
    location = None
    players: dict[str, list[PlayerModel]] = {}
    odds: dict[str, list[OddsModel]] = {}
    news: dict[str, NewsModel] = {}
    social: dict[str, SocialModel] = {}
    points = None
    ladder_rank = None
    field_goals = None
    for team_model in team_models:
        team_model_location = team_model.location
        if team_model_location is not None:
            location = team_model_location
        for player_model in team_model.players:
            player_id = player_model.identifier
            player_name_key = _normalise_player_name(player_model.name)
            if player_model.identifier in player_identity_map:
                player_id = player_identity_map[player_id]
            elif player_name_key in names:
                player_id = names[player_name_key]
            else:
                names[player_name_key] = player_id
            players[player_id] = players.get(player_id, []) + [player_model]
        for odds_model in team_model.odds:
            key = f"{odds_model.bookie.identifier}-{odds_model.odds}"
            odds[key] = odds.get(key, []) + [odds_model]
        team_model_points = team_model.points
        if not is_null(team_model_points):
            points = team_model_points
        team_model_ladder_rank = team_model.ladder_rank
        if not is_null(team_model_ladder_rank):
            ladder_rank = team_model_ladder_rank
        for news_model in team_model.news:
            news_key = "-".join(
                [
                    news_model.title,
                    str(news_model.published),
                    news_model.summary,
                    news_model.source,
                ]
            )
            news[news_key] = news_model
        for social_model in team_model.social:
            social_key = "-".join(
                [social_model.network, social_model.post, str(social_model.published)]
            )
            social[social_key] = social_model
        team_model_field_goals = team_model.field_goals
        if not is_null(team_model_field_goals):
            field_goals = team_model_field_goals

    return TeamModel(
        identifier=identifier,
        name=team_models[0].name,
        location=location,
        players=[  # pyright: ignore
            create_combined_player_model(v, k) for k, v in players.items()
        ],
        odds=[x[0] for x in odds.values()],
        points=points,
        ladder_rank=ladder_rank,
        news=sorted(news.values(), key=lambda x: x.published),
        social=sorted(social.values(), key=lambda x: x.published),
        field_goals=field_goals,
    )
