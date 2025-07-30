from datetime import datetime

from pydantic import BaseModel

from sportswrangler.utils.enums import ExtendedEnum


class TheOddsApiRegion(ExtendedEnum):
    US = "us"
    US2 = "us2"


class OddsFormat(str, ExtendedEnum):
    DECIMAL = "decimal"
    AMERICAN = "american"


class Bookmaker(BaseModel):
    odds_api_key: str
    url: str
    name: str
    region: TheOddsApiRegion


class BookmakerBet(BaseModel):
    bookmaker: Bookmaker
    odds: float
    lastUpdated: datetime


class TheOddsApiUsBookmaker(ExtendedEnum):
    BETONLINEAG = Bookmaker(
        odds_api_key="betonlineag",
        url="https://www.betonline.ag/",
        name="BetOnline.ag",
        region=TheOddsApiRegion.US,
    )
    BETMGM = Bookmaker(
        odds_api_key="betmgm",
        url="https://sports.nj.betmgm.com/en/sports",
        name="BetMGM",
        region=TheOddsApiRegion.US,
    )
    BETRIVERS = Bookmaker(
        odds_api_key="betrivers",
        url="https://www.betrivers.com/",
        name="BetRivers",
        region=TheOddsApiRegion.US,
    )
    BETUS = Bookmaker(
        odds_api_key="betus",
        url="https://www.betus.com.pa/",
        name="BetUS",
        region=TheOddsApiRegion.US,
    )
    BOVADA = Bookmaker(
        odds_api_key="bovada",
        url="https://www.bovada.lv/",
        name="Bovada",
        region=TheOddsApiRegion.US,
    )
    DRAFTKINGS = Bookmaker(
        odds_api_key="draftkings",
        url="https://draftkings.com/",
        name="DraftKings",
        region=TheOddsApiRegion.US,
    )
    FANDUEL = Bookmaker(
        odds_api_key="fanduel",
        url="https://sportsbook.fanduel.com/sports",
        name="FanDuel",
        region=TheOddsApiRegion.US,
    )
    LOWVIG = Bookmaker(
        odds_api_key="lowvig",
        url="https://www.lowvig.ag/",
        name="LowVig.ag",
        region=TheOddsApiRegion.US,
    )
    MYBOOKIEAG = Bookmaker(
        odds_api_key="mybookieag",
        url="https://mybookie.ag/",
        name="MyBookie.ag",
        region=TheOddsApiRegion.US,
    )
    POINTSBETUS = Bookmaker(
        odds_api_key="pointsbetus",
        url="https://nj.pointsbet.com/sports",
        name="PointsBet (US)",
        region=TheOddsApiRegion.US,
    )
    SUPERBOOK = Bookmaker(
        odds_api_key="superbook",
        url="https://co.superbook.com/sports",
        name="SuperBook",
        region=TheOddsApiRegion.US,
    )
    UNIBET_US = Bookmaker(
        odds_api_key="unibet_us",
        url="https://nj.unibet.com/",
        name="Unibet",
        region=TheOddsApiRegion.US,
    )
    WILLIAMHILL_US = Bookmaker(
        odds_api_key="williamhill_us",
        url="https://www.williamhill.com/us/nj/bet/",
        name="William Hill (Caesars)",
        region=TheOddsApiRegion.US,
    )
    WYNNBET = Bookmaker(
        odds_api_key="wynnbet",
        url="https://www.wynnbet.com/",
        name="WynnBET",
        region=TheOddsApiRegion.US,
    )
    BALLYBET = Bookmaker(
        odds_api_key="ballybet",
        url="https://play.ballybet.com/",
        name="Bally Bet",
        region=TheOddsApiRegion.US2,
    )
    BETPARX = Bookmaker(
        odds_api_key="betparx",
        url="https://betparx.com/#home",
        name="betPARX",
        region=TheOddsApiRegion.US2,
    )
    ESPNBET = Bookmaker(
        odds_api_key="espnbet",
        url="https://espnbet.com/",
        name="ESPN BET",
        region=TheOddsApiRegion.US2,
    )
    FLIFF = Bookmaker(
        odds_api_key="fliff",
        url="https://www.getfliff.com/",
        name="Fliff",
        region=TheOddsApiRegion.US2,
    )
    HARDROCKBET = Bookmaker(
        odds_api_key="hardrockbet",
        url="https://app.hardrock.bet/",
        name="Hard Rock Bet",
        region=TheOddsApiRegion.US2,
    )
    SISPORTSBOOK = Bookmaker(
        odds_api_key="sisportsbook",
        url="https://www.sisportsbook.com/",
        name="SI Sportsbook",
        region=TheOddsApiRegion.US2,
    )
    TIPICO_US = Bookmaker(
        odds_api_key="tipico_us",
        url="https://sportsbook-nj.tipico.us/home",
        name="Tipico",
        region=TheOddsApiRegion.US2,
    )
    WINDCREEK = Bookmaker(
        odds_api_key="windcreek",
        url="https://play.windcreekcasino.com/",
        name="Wind Creek (Betfred PA)",
        region=TheOddsApiRegion.US2,
    )

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))

    @classmethod
    def list_the_odds_api_keys(cls):
        return list(map(lambda c: c.value.odds_api_key, cls))

    @classmethod
    def list_bookmaker_urls(cls):
        return list(map(lambda c: c.value.url, cls))

    @classmethod
    def list_bookmaker_names(cls):
        return list(map(lambda c: c.value.name, cls))

    @classmethod
    def enum_from_key(cls, key: str):
        for e in cls:
            if e.value.odds_api_key == key:
                return e
        return None
