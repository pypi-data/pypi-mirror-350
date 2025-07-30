"""Combined coach model."""

from ..coach_model import CoachModel
from .null_check import is_null


def create_combined_coach_model(
    coach_models: list[CoachModel], identifier: str
) -> CoachModel:
    """Create a coach model by combining many coach models."""
    name = None
    birth_date = None
    age = None
    for coach_model in coach_models:
        coach_model_name = coach_model.name
        if not is_null(coach_model_name):
            name = coach_model_name
        coach_model_birthdate = coach_model.birth_date
        if not is_null(coach_model_birthdate):
            birth_date = coach_model_birthdate
        coach_model_age = coach_model.age
        if not is_null(coach_model_age):
            age = coach_model_age
    if name is None:
        raise ValueError("name is null.")
    return CoachModel(
        identifier=identifier,
        name=name,
        birth_date=birth_date,
        age=age,
    )
