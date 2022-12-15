"""A place to put enums that are used throughout the package"""

from enum import Enum


class Team(Enum):
    """Enumerate current NHL teams. The value is a string representation of the team's ID in the API"""

    ANA = "24"
    ARI = "53"
    BOS = "6"
    BUF = "7"
    CAR = "12"
    CBJ = "29"
    CGY = "20"
    CHI = "16"
    COL = "21"
    DAL = "25"
    DET = "17"
    EDM = "22"
    FLA = "13"
    LAK = "26"
    MIN = "30"
    MTL = "8"
    NJD = "1"
    NSH = "18"
    NYI = "2"
    NYR = "3"
    OTT = "9"
    PHI = "4"
    PIT = "5"
    SEA = "55"
    SJS = "28"
    STL = "19"
    TBL = "14"
    TOR = "10"
    VAN = "23"
    VGK = "54"
    WPG = "52"
    WSH = "15"


class Conference(Enum):
    """An enum representing a conference"""

    eastern = "6"
    western = "5"


class Division(Enum):
    """An enum representing a division"""

    atlantic = "17"
    metropolitan = "18"
    pacific = "15"
    central = "16"


class API_URL_root(Enum):
    """an enumeration of the NHL api URL root"""

    stats = "https://statsapi.web.nhl.com/api/v1"
    records = "https://records.nhl.com/site/api"


class API_URL(Enum):
    """base urls for api endpoints. Many of these take modifiers to refine the query."""

    play_by_play = f"{API_URL_root.stats.value}/game/ID/feed/live"
    schedule = f"{API_URL_root.stats.value}/schedule"
    standings = f"{API_URL_root.stats.value}/standings"
    franchise = f"{API_URL_root.stats.value}/franchises"
    teams = f"{API_URL_root.stats.value}/teams"
    division = f"{API_URL_root.stats.value}/divisions"
    conference = f"{API_URL_root.stats.value}/conferences"
    people = f"{API_URL_root.stats.value}/people"
    game_types = f"{API_URL_root.stats.value}/gameTypes"
    game_status = f"{API_URL_root.stats.value}/gameStatus"
    play_types = f"{API_URL_root.stats.value}/playTypes"
    tournament_types = f"{API_URL_root.stats.value}/tournamentTypes"
    playoffs = f"{API_URL_root.stats.value}/tournaments/playoffs"
    seasons = f"{API_URL_root.stats.value}/seasons"
    current_season = f"{API_URL_root.stats.value}/seasons/current"
    standing_types = f"{API_URL_root.stats.value}/standingsTypes"
    stats_types = f"{API_URL_root.stats.value}/statTypes"
    draft = f"{API_URL_root.stats.value}/draft"
    prospects = f"{API_URL_root.stats.value}/prospects"
    awards = f"{API_URL_root.stats.value}/awards"
    venues = f"{API_URL_root.stats.value}/venues"
    event_types = f"{API_URL_root.stats.value}/eventTypes"
    performer_types = f"{API_URL_root.stats.value}/performerTypes"
