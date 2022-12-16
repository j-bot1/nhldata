"""
Module for finding ids that might be used as query paramaters in api calls
"""

from typing import Union, Optional, List, Tuple
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

    Examples
    -------
    Find the ids of all games played on December 12th, 2022

    >>> from nhldata.id import GameId
    >>> g_id = GameId('2022-12-12')
    >>> g_id.find_ids()
    >>> print(g_id.game_ids)
    ['2022020448', '2022020449', '2022020450', '2022020451', '2022020452', '2022020453']

    Find the ids of all games played by the Seattle Kraken between
    December 1st 2022 and December 14th 2022.

    >>> from nhldata.id import GameId
    >>> from nhldata.data import Team
    >>> g_id = GameId(('2022-12-01', '2022-12-14'), Team.SEA)
    >>> g_id.find_ids()
    >>> print(g_id.game_ids)
    ['2022020374', '2022020389', '2022020411', '2022020427', '2022020444', '2022020459']

    Find the ids of all games plays by the Seattle Kraken, the Montreal Canadians,
    or the Tampa Bay Lighting on October 26h, 2021.

    >>> from nhldata.id import GameId
    >>> from nhldata.data import Team
    >>> g_id = GameId('2021-10-26', [Team.SEA, Team.MTL, Team.TBL])
    >>> g_id.find_ids()
    >>> print(g_id.game_ids)
    ['2021020091', '2021020096']
    """

    def __init__(
        self,
        date: Union[str, Tuple[str, str]],
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
        """
        Find game ids that meet the given search critera and store them in the
        game_ids attribute.

        Return
        ------
        None

        Example
        -------
        Find the ids of all games plays by the Seattle Kraken, the Montreal Canadians,
        or the Tampa Bay Lighting on October 26h, 2021.

        >>> from nhldata.id import GameId
        >>> from nhldata.data import Team
        >>> g_id = GameId('2021-10-26', [Team.SEA, Team.MTL, Team.TBL])
        >>> g_id.find_ids()
        >>> print(g_id.game_ids)
        ['2021020091', '2021020096']
        """

        self._params = self._build_params_dict()
        self._requests_dict = self._make_request(self._params)

        game_ids = nested_lookup("gamePk", self._requests_dict)
        self.game_ids = [str(x) for x in game_ids]

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
