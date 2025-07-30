"""Tests for the player model class."""
import unittest

from sportsball.data.player_model import PlayerModel


class TestPlayerModel(unittest.TestCase):

    def setUp(self):
        self._player_model = PlayerModel(
            identifier="a",
            jersey="45",
            kicks=None,
            fumbles=None,
            fumbles_lost=None,
            field_goals=None,
            field_goals_attempted=10,
            offensive_rebounds=None,
            assists=None,
            turnovers=None,
            name="James Jones",
            marks=None,
            handballs=None,
            disposals=None,
            goals=None,
            behinds=None,
            hit_outs=None,
            tackles=None,
            rebounds=None,
            insides=None,
            clearances=None,
            clangers=None,
            free_kicks_for=None,
            free_kicks_against=None,
            brownlow_votes=None,
            contested_possessions=None,
            uncontested_possessions=None,
            contested_marks=None,
            marks_inside=None,
            one_percenters=None,
            bounces=None,
            goal_assists=None,
            percentage_played=None,
            birth_date=None,
        )

    def test_field_goals_attempted(self):
        self.assertEqual(self._player_model.field_goals_attempted, 10)
