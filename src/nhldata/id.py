"""
Module for finding ids that might be used as query paramaters in api calls
"""

from typing import Union, Optional, List, LiteralString, Tuple
from nhldata.data import Team
from nhldata.nhl_api import NhlApi, Endpoint
from nested_lookup import nested_lookup


class GameId:
    """
    A representation of a set of GameIds.

    Each NHL game is uniquly identified by a game id. These game ids are used
    in the construction of some NHL API endpoints and are needed to retrieve
    data from them. This class uses a set of search critera to find and store
    game ids.

    Attributes
    ----------
        game_ids : List[str]
            list of game ids as strings. created after `.find_ids()` method is
            executed.

    Methods
    -------
        find_ids() : None
            Queries the shcedule API and finds the game Ids given the arguments.
            Stores the ids as a list of strings in the `ids` attribute.
    """

    def __init__(
        self,
        date: Union[LiteralString, Tuple[LiteralString, LiteralString]],
        team: Optional[Union[Team, List[Team]]] = None,
    ):
        """
        Arguments
        ---------
        date : str | tuple(start_date: str, end_date: str)
           The time window in which the games occured.

        team : Team | List[Team], optional
            The team or teams that played in the games you want the ids of
        """
        self._url = Endpoint.schedule
        self._date = date
        self._team = team
        self.game_ids = None

    def find_ids(self) -> None:

        self.params = self._build_params_dict()
        self.requests_dict = self._make_request(self.params)

        # TODO: replace `nested_lookup()` import with code I control
        game_ids = nested_lookup("gamePk", self.requests_dict)
        self.game_ids = [str(x) for x in game_ids]

    def to_list(self) -> list:
        return self.game_ids

    def _make_request(self, params: dict) -> dict:
        """make an api request and return the payload as dict"""
        if params is None:
            nhl_api = NhlApi(self._url)
        else:
            nhl_api = NhlApi(self._url, params)

        nhl_api.request()

        return nhl_api.to_dict()

    def _build_params_dict(self) -> dict:

        params = dict()
        params = self._add_date_params(params)
        params = self._add_team_param(params)

        return params

    def _add_date_params(self, params: dict) -> dict:
        """if `date` is defined, add it to the params dict"""
        if self._date is None:
            return params

        if isinstance(self._date, tuple):
            startDate, endDate = self._date
            params.update({"startDate": startDate, "endDate": endDate})
            return params

        params.update({"date": self._date})
        return params

    def _add_team_param(self, params: dict) -> dict:
        """if `team` is defined, add it to the params dict"""
        if self._team is None:
            return params

        if isinstance(self._team, list):
            params.update({"teamId": ",".join([x.value for x in self._team])})
            return params

        params.update({"teamId": self._team.value})
        return params


# class PlayerId:
#   class to find player ids
