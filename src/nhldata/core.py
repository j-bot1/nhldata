from typing import Union, Optional, List
from nhldata.data import Team, API_URL
import requests
from nested_lookup import nested_lookup


class Api:
    """Class that handles Api request and converts payload to dict

    ...
    Arguments
    =========
        endpoint_utl : API_URL
            the API_URL enum associated with the endpoint we'd like to query

        params: Optional[dict]
            A dictionary of modifiers to apply to the query

    Methods
    =======
        request : None
            calls the api and gets the response

        to_dict : dict
            returns the response as a dictionary

    """

    def __init__(self, endpoint_url: API_URL, params: Optional[dict] = None) -> None:
        self.endpoint_url = endpoint_url.value
        self.params = params

    def request(self) -> None:
        """
        Submits the get request to the Api.

        ...

        Returns
        =======
        None

        """
        if self.params is not None:
            response = requests.get(self.endpoint_url, params=self.params)

        else:
            response = requests.get(self.endpoint_url, params=self.params)

        response.raise_for_status()

        self.response = response

    def to_dict(self) -> dict:
        """
        if request was successful, returns the request payload as a dict

        ...

        Returns
        =======
        dict

        """
        return self.response.json()


class GameId:
    """Given a set of critera, find a set of game ids.

    Uses the shcedule endpoint of the API to find game ids. Game Ids are used
    in the URLs of some endpoints to retrive more detailed information related to
    a specific game. GameId can be helpful in finding them.

    ...
    Arguments
    =========
        on_date : str
            look for game ids on a specific date. One of `on_date` or
            `between_dates` is required.

        between_dates : tuple(str, str)
            a tuple of strings representing the start date and end date of a
            range of days. Look for game Ids between these dates, inclusive.
            One of `on_date` or `between_dates` is required.

        team : Team
            look for games in that time window played by a specific team.

    Methods
    =======
        find_ids() : None
            Queries the shcedule API and finds the game Ids given the arguments.
            Stores the ids as a list of strings in the `ids` attribute.

    Attributes
    ==========
        ids : List[str]
            list of game ids as strings. created after `find_ids()` method is executed.

    """

    def __init__(
        self,
        on_date: Optional[str] = None,
        between_dates: Optional[tuple[str]] = None,
        team: Optional[Union[Team, List[Team]]] = None,
    ) -> None:
        self.url = API_URL.schedule
        self.on_date = on_date
        self.between_dates = between_dates
        self.team = team

    def find_ids(self) -> None:

        self.params = self._build_params_dict()
        self.requests_dict = self._make_request(self.params)
        game_ids = nested_lookup("gamePk", self.requests_dict)
        self.game_ids = [str(x) for x in game_ids]

    def to_list(self) -> list:
        return self.game_ids

    def _make_request(self, params: dict) -> dict:
        """make an api request and return the payload as dict"""
        if params is None:
            nhl_api = Api(self.url)
        else:
            nhl_api = Api(self.url, params)

        nhl_api.request()

        return nhl_api.to_dict()

    def _build_params_dict(self) -> dict:

        params = dict()
        params = self._on_date(params)
        params = self._between_dates(params)
        params = self._team(params)

        return params

    def _on_date(self, params: dict) -> dict:
        """if `on_date` is defined, add it to the params dict"""
        if self.on_date is None:
            return params

        params.update({"date": self.on_date})

        return params

    def _between_dates(self, params: dict) -> dict:
        """if `between_dates` is defined, add it to the params dict"""
        if self.between_dates is None:
            return params

        startDate, endDate = self.between_dates
        params.update({"startDate": startDate, "endDate": endDate})
        return params

    def _team(self, params: dict) -> dict:
        """if `team` is defined, add it to the params dict"""
        if self.team is None:
            return params

        if isinstance(self.team, list):
            params.update({"teamId": ",".join([x.value for x in self.team])})
            return params

        params.update({"teamId": self.team.value})
        return params
