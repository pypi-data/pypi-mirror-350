"""Tests for the ESPN game model class."""
import datetime
import os
import unittest

import requests_mock
import requests_cache
from sportsball.data.espn.espn_game_model import create_espn_game_model
from sportsball.data.league import League
from sportsball.data.season_type import SeasonType


class TestESPNGameModel(unittest.TestCase):

    def setUp(self):
        self._session = requests_cache.CachedSession(backend="memory")
        self.dir = os.path.dirname(__file__)

    def test_dt(self):
        dt = datetime.datetime(2023, 9, 15, 0, 15)
        with requests_mock.Mocker() as m:

            game_model = create_espn_game_model(
                {
                    "date": dt.isoformat(),
                    "competitions": [],
                },
                1,
                1,
                self._session,
                League.NFL,
                2016,
                SeasonType.REGULAR,
            )

            self.assertEqual(game_model.dt, dt)
