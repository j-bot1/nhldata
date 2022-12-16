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
