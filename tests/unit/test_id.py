"""unit tests for finding game ids"""

from nhldata.id import GameId
from nhldata.data import Team


class TestGameId:
    def test_find_all_games_on_single_day(self):

        # expected result
        expected = ["2022020466", "2022020467", "2022020468"]

        # actual result
        g_id = GameId(date="2022-12-14")
        g_id.find_ids()

        actual = g_id.game_ids
        assert isinstance(actual, list)
        assert all(isinstance(id, str) for id in actual)
        assert len(expected) == len(actual)
        assert expected.sort() == actual.sort()

    def test_find_all_games_between_two_dates(self):

        # expected result
        expected = [str(x) for x in range(2022020448, 2022020469)]

        # actual result
        g_id = GameId(date=("2022-12-12", "2022-12-14"))
        g_id.find_ids()

        actual = g_id.game_ids

        assert isinstance(actual, list)
        assert all(isinstance(id, str) for id in actual)
        assert len(expected) == len(actual)
        assert expected.sort() == actual.sort()

    def test_find_all_games_of_one_team_between_two_dates(self):

        # expected result
        expected = ["2022020448", "2022020466"]

        # actual result
        g_id = GameId(date=("2022-12-12", "2022-12-14"), team=Team.MTL)
        g_id.find_ids()

        actual = g_id.game_ids

        assert isinstance(actual, list)
        assert all(isinstance(id, str) for id in actual)
        assert len(expected) == len(actual)
        assert expected.sort() == actual.sort()

    def test_find_all_games_of_multiple_teams_between_two_dates(self):

        # expected result
        expected = [
            "2022020448",
            "2022020466",
            "2022020459",
            "2022020460",
            "2022020467",
        ]

        # actual result
        g_id = GameId(
            date=("2022-12-12", "2022-12-14"),
            team=[Team.MTL, Team.SEA, Team.DET],
        )
        g_id.find_ids()

        actual = g_id.game_ids

        assert isinstance(actual, list)
        assert all(isinstance(id, str) for id in actual)
        assert len(expected) == len(actual)
        assert expected.sort() == actual.sort()
