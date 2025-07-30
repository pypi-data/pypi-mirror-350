from typing import Literal

from sportswrangler.odds.the_odds_api.utils.classes import NBAKeyMapping
from sportswrangler.odds.the_odds_api.wranglers.base import TheOddsApiWrangler
from sportswrangler.utils.enums import Sport, StatCategory, BetCategory


class TheOddsApiNBAWrangler(TheOddsApiWrangler):
    sport: Sport = Sport.NBA
    _outrights_key: str = "basketball_nba_championship_winner"
    _player_prop_markets: list[
        Literal[
            "player_points",
            "player_rebounds",
            "player_assists",
            "player_threes",
            "player_blocks",
            "player_steals",
            "player_turnovers",
            "player_blocks_steals",
            "player_points_rebounds_assists",
            "player_points_rebounds",
            "player_points_assists",
            "player_rebounds_assists",
            "player_first_basket",
            "player_double_double",
            "player_triple_double",
            "player_points_alternate",
            "player_rebounds_alternate",
            "player_assists_alternate",
            "player_blocks_alternate",
            "player_steals_alternate",
            "player_threes_alternate",
            "player_points_assists_alternate",
            "player_points_rebounds_alternate",
            "player_rebounds_assists_alternate",
            "player_points_rebounds_assists_alternate",
        ]
    ] = [
        "player_points",
        "player_rebounds",
        "player_assists",
        "player_threes",
        "player_blocks",
        "player_steals",
        "player_turnovers",
        "player_blocks_steals",
        "player_points_rebounds_assists",
        "player_points_rebounds",
        "player_points_assists",
        "player_rebounds_assists",
        "player_first_basket",
        "player_double_double",
        "player_triple_double",
        # alternate
        "player_points_alternate",
        "player_rebounds_alternate",
        "player_assists_alternate",
        "player_blocks_alternate",
        "player_steals_alternate",
        "player_threes_alternate",
        "player_points_assists_alternate",
        "player_points_rebounds_alternate",
        "player_rebounds_assists_alternate",
        "player_points_rebounds_assists_alternate",
    ]
    _player_prop_key_mapping: NBAKeyMapping = {
        "player_points": StatCategory.POINTS,
        "player_rebounds": StatCategory.REBOUNDS,
        "player_assists": StatCategory.ASSISTS,
        "player_threes": StatCategory.THREE_POINTERS,
        "player_blocks": StatCategory.BLOCKS,
        "player_steals": StatCategory.STEALS,
        "player_turnovers": StatCategory.TURNOVERS,
        "player_blocks_steals": "{}_{}".format(
            StatCategory.BLOCKS, StatCategory.STEALS
        ),
        "player_points_rebounds_assists": "{}_{}_{}".format(
            StatCategory.POINTS, StatCategory.REBOUNDS, StatCategory.ASSISTS
        ),
        "player_points_rebounds": "{}_{}".format(
            StatCategory.POINTS, StatCategory.REBOUNDS
        ),
        "player_points_assists": "{}_{}".format(
            StatCategory.POINTS, StatCategory.ASSISTS
        ),
        "player_rebounds_assists": "{}_{}".format(
            StatCategory.REBOUNDS, StatCategory.ASSISTS
        ),
        "player_first_basket": "FB",
        "player_double_double": "DD",
        "player_triple_double": "TD",
        # alternate
        "player_points_alternate": "{} {}".format(
            BetCategory.ALTERNATE, StatCategory.POINTS
        ),
        "player_rebounds_alternate": "{} {}".format(
            BetCategory.ALTERNATE, StatCategory.REBOUNDS
        ),
        "player_assists_alternate": "{} {}".format(
            BetCategory.ALTERNATE, StatCategory.ASSISTS
        ),
        "player_blocks_alternate": "{} {}".format(
            BetCategory.ALTERNATE, StatCategory.BLOCKS
        ),
        "player_steals_alternate": "{} {}".format(
            BetCategory.ALTERNATE, StatCategory.STEALS
        ),
        "player_threes_alternate": "{} {}".format(
            BetCategory.ALTERNATE, StatCategory.THREE_POINTERS
        ),
        "player_points_assists_alternate": "{} {}_{}".format(
            BetCategory.ALTERNATE, StatCategory.POINTS, StatCategory.ASSISTS
        ),
        "player_points_rebounds_alternate": "{} {}_{}".format(
            BetCategory.ALTERNATE, StatCategory.POINTS, StatCategory.REBOUNDS
        ),
        "player_rebounds_assists_alternate": "{} {}_{}".format(
            BetCategory.ALTERNATE, StatCategory.REBOUNDS, StatCategory.ASSISTS
        ),
        "player_points_rebounds_assists_alternate": "{} {}_{}_{}".format(
            BetCategory.ALTERNATE,
            StatCategory.POINTS,
            StatCategory.REBOUNDS,
            StatCategory.ASSISTS,
        ),
    }
