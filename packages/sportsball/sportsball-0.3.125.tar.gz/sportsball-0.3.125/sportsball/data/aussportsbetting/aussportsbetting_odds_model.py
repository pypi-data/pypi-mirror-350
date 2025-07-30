"""Aussportsbetting odds model."""

from ...cache import MEMORY
from ..team_model import OddsModel
from .aussportsbetting_bookie_model import create_aussportsbetting_bookie_model


@MEMORY.cache
def create_aussportsbetting_odds_model(odds: float) -> OddsModel:
    """Create an odds model based off aus sports betting."""
    bookie = create_aussportsbetting_bookie_model()
    return OddsModel(odds=odds, bookie=bookie, dt=None, canonical=True)  # pyright: ignore
