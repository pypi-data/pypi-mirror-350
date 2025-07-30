from sportswrangler.odds.the_odds_api.wranglers import TheOddsApiNBAWrangler
from sportswrangler.utils.enums import Sport


class TheOddsApiWNBAWrangler(TheOddsApiNBAWrangler):
    sport: Sport = Sport.WNBA
