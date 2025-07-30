"""Aussportsbetting bookie model."""

from ...cache import MEMORY
from ..bookie_model import BookieModel


@MEMORY.cache
def create_aussportsbetting_bookie_model() -> BookieModel:
    """Create bookie model from aus sports betting."""
    return BookieModel(identifier="bet365", name="Bet365")
