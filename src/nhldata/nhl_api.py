"""
Get data from an NHL API endpoint

This module handles everything related to connecting to and requesting data
from an Nhl API endpoint.
"""

from typing import Optional, Dict
from enum import Enum
import requests


class _EndpointRoot(Enum):
    """an enumeration of the NHL api URL root"""

    stats = "https://statsapi.web.nhl.com/api/v1"
    records = "https://records.nhl.com/site/api"


class Endpoint(Enum):
    """
    A representation of an NHL API endpoint.

    This class represents all of the possible NHL API endpoints we're able to
    connect to. This class is passed as the first argument to the NhlApi class
    on its initialization and defines the endpoint it will connect to.

    Currently, only endpoints of the stats api are avalible.

    Notes
    ------
    While there's no official documentation for these endpoints, Drew Hynes has
    done a tremendous job creating an unofficial refference, which you can find
    here: https://gitlab.com/dword4/nhlapi/-/blob/master/stats-api.md

    Examples
    --------
    represent the schedule endpoint.
    >>> Endpoint.schedule
    <Endpoint.schedule: 'https://statsapi.web.nhl.com/api/v1/schedule'>


    """

    play_by_play = f"{_EndpointRoot.stats.value}/game/ID/feed/live"
    schedule = f"{_EndpointRoot.stats.value}/schedule"
    standings = f"{_EndpointRoot.stats.value}/standings"
    franchise = f"{_EndpointRoot.stats.value}/franchises"
    teams = f"{_EndpointRoot.stats.value}/teams"
    division = f"{_EndpointRoot.stats.value}/divisions"
    conference = f"{_EndpointRoot.stats.value}/conferences"
    people = f"{_EndpointRoot.stats.value}/people"
    game_types = f"{_EndpointRoot.stats.value}/gameTypes"
    game_status = f"{_EndpointRoot.stats.value}/gameStatus"
    play_types = f"{_EndpointRoot.stats.value}/playTypes"
    tournament_types = f"{_EndpointRoot.stats.value}/tournamentTypes"
    playoffs = f"{_EndpointRoot.stats.value}/tournaments/playoffs"
    seasons = f"{_EndpointRoot.stats.value}/seasons"
    current_season = f"{_EndpointRoot.stats.value}/seasons/current"
    standing_types = f"{_EndpointRoot.stats.value}/standingsTypes"
    stats_types = f"{_EndpointRoot.stats.value}/statTypes"
    draft = f"{_EndpointRoot.stats.value}/draft"
    prospects = f"{_EndpointRoot.stats.value}/prospects"
    awards = f"{_EndpointRoot.stats.value}/awards"
    venues = f"{_EndpointRoot.stats.value}/venues"
    event_types = f"{_EndpointRoot.stats.value}/eventTypes"
    performer_types = f"{_EndpointRoot.stats.value}/performerTypes"


class NhlApi:
    """
    A class used to represent the NHL API

    This class is our entrypoint into the NHL API. It handles all get requests
    to all NHL API endpoints and stores the response. It also contains methods
    to transform that response in to various useful data structures that can be
    served up for consumption by other processes.

    The class takes an Endpoint enum to define the endpoint url. This can be
    imported from nhldata.nhl_api.

    Attributes
    ----------
    endpoint_url : Endpoint
        A Endpoint enum defining an API endpoint

    params: dict(key : str(value))
        A dictionary of params used to modify the request from the endpoint.
        Keys corrispond to endpoint modifiers and values corrispond to their
        value.

    response: requests.response
        The response from the API. Avalible after successful executing the
        `.request()` method.

    Methods
    -------
        request : None
            calls the api and if successfull, stores the response to the
            response attribute.

        to_dict : dict
            returns the response conent as a dictionary

    Example
    -------
    Get the current season shcedule as a dict

    >>> from nhldata.nhl_api import NhlApi, Endpoint
    >>> api_request = NhlApi(Endpoint.shcedule)
    >>> api_request.request()
    >>> api_request.to_dict()
    """

    def __init__(self, endpoint: Endpoint, params: Optional[Dict] = None):
        """
        Paramaters
        ----------
        endpoint : Endpoint
            A Endpoint enum defining an API endpoint

        params: dict(key : str(value)), optional
            A dictionary of params used to modify the request from the
            endpoint. Defualts to None.
        """
        self.endpoint = endpoint.value
        self.params = params

    def request(self) -> None:
        """
        Submits the get request to the specified API endpoint and stores the
        result in the response attribute.

        Raises
        ------
        ConnectionError
            if the connection to the endpoint fails. this is usually because an
            invalid endpoint url was given to the class

        HTTPError
            if the endpoint responded with an error status

        """
        if self.params is not None:
            response = requests.get(self.endpoint, params=self.params)
        else:
            response = requests.get(self.endpoint, params=self.params)

        response.raise_for_status()
        self.response = response

    def to_dict(self) -> Dict:
        """
        Returns the API response content as a dictionary

        The `.request()` method must be executed successfully before this can
        return any content.

        Returns
        -------
        dict
            the body of the api response
        """
        return self.response.json()
