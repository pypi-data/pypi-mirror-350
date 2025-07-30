from enum import Enum


class ExtendedEnum(Enum):

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))


class Sport(str, ExtendedEnum):
    NBA = "NBA"
    NFL = "NFL"
    NHL = "NHL"
    MLB = "MLB"
    EPL = "EPL"
    NCAAF = "NCAAF"
    WNBA = "WNBA"


class StatCategory(str, ExtendedEnum):
    # General
    POINTS = "PTS"
    ASSISTS = "AST"
    BLOCKS = "BLK"
    STEALS = "STL"
    TURNOVERS = "TOV"
    REBOUNDS = "TRB"
    THREE_POINTERS = "3P"
    GOAL = "G"

    # Baseball
    STRIKEOUTS = "K"
    HITS = "H"
    WALKS = "BB"
    RUNS = "R"
    HOME_RUNS = "HR"
    RBI = "RBI"
    TOTAL_BASES = "TB"

    # Football
    YARDS = "YDS"
    TOUCHDOWNS = "TD"
    ATTEMPTS = "ATT"
    COMPLETIONS = "COM"
    INTERCEPTIONS = "INT"
    LONGEST = "LNG"
    RECEPTIONS = "REC"

    # Hockey
    SAVES = "SV"
    SHOTS_ON_GOAL = "S"
    POWER_PLAY_POINTS = "PPP"

    # Soccer
    CARD = "C"
    CORNER = "CRN"


class BetCategory(str, ExtendedEnum):
    ALTERNATE = "Alt"
    SPREAD = "Spread"
    TOTALS = "Total"
    H2H = "Moneyline"
