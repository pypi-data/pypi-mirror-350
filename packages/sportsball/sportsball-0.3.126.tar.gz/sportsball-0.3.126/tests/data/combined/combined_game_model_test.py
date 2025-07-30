"""Tests for the combined game model class."""
import datetime
import os
import unittest

import requests_mock
import requests_cache
from sportsball.data.combined.combined_game_model import create_combined_game_model
from sportsball.data.league import League
from sportsball.data.season_type import SeasonType
from sportsball.data.game_model import GameModel


class TestCombinedGameModel(unittest.TestCase):

    def setUp(self):
        self._session = requests_cache.CachedSession(backend="memory")
        self.dir = os.path.dirname(__file__)

    def test_dt(self):
        dt = datetime.datetime(2023, 9, 15, 0, 15)
        with requests_mock.Mocker() as m:
            game_model = GameModel(
                dt=dt,
                week=None,
                game_number=None,
                venue=None,
                teams=[],
                end_dt=None,
                attendance=None,
                league=str(League.NBA),
                year=None,
                season_type=SeasonType.REGULAR,
                postponed=True,
                play_off=None,
            )
            names = {}
            combined_game_model = create_combined_game_model(
                [game_model],
                {},
                {},
                {},
                self._session,
                names,
            )
            self.assertEqual(combined_game_model.dt, dt)
