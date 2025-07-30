"""Tests for the team model class."""
import unittest

from sportsball.data.team_model import TeamModel


class TestTeamModel(unittest.TestCase):

    def setUp(self):
        self._team_model = TeamModel(
            identifier="A",
            name="B",
            location=None,
            players=[],
            odds=[],
            points=2.0,
            ladder_rank=10,
            kicks=None,
            news=[],
            social=[],
            field_goals=None,
        )

    def test_notnull(self):
        self.assertIsNotNone(self._team_model)
