from sportswrangler.odds.the_odds_api.wranglers import TheOddsApiNFLWrangler
from sportswrangler.utils.enums import Sport


class TheOddsApiNCAAFWrangler(TheOddsApiNFLWrangler):
    sport: Sport = Sport.NCAAF
    _outrights_key: str = "americanfootball_ncaaf_championship_winner"
