"""unit tests for finding game ids"""

from ...src.core import GameId
from ...src.data import Team


class TestGameId:
    def test_find_all_games_on_single_day(self):

        # expected result
        expected = ["2022020466", "2022020467", "2022020468"]

        # actual result
        game_ids = GameId(on_date="2022-12-14")
        game_ids.find_ids()

        actual = game_ids.ids

        assert isinstance(actual, list)
        assert all(isinstance(id, str) for id in actual)
        assert len(expected) == len(actual)
        assert expected == actual

    def test_find_all_games_between_two_dates(self):

        # expected result
        expected = [str(x) for x in range(2022020448, 2022020469)]

        # actual result
        game_ids = GameId(between_dates=("2022-12-12", "2022-12-14"))
        game_ids.find_ids()

        actual = game_ids.ids

        assert isinstance(actual, list)
        assert all(isinstance(id, str) for id in actual)
        assert len(expected) == len(actual)
        assert expected == actual

    def test_find_all_games_of_one_team_between_two_dates(self):

        # expected result
        expected = ["2022020448", "2022020466"]

        # actual result
        game_ids = GameId(between_dates=("2022-12-12", "2022-12-14"), team=Team.MTL)
        game_ids.find_ids()

        actual = game_ids.ids

        assert isinstance(actual, list)
        assert all(isinstance(id, str) for id in actual)
        assert len(expected) == len(actual)
        assert expected == actual
