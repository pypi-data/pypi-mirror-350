from typing import Literal

from sportswrangler.odds.the_odds_api.utils.classes import NFLKeyMapping
from sportswrangler.odds.the_odds_api.wranglers.base import TheOddsApiWrangler
from sportswrangler.utils.enums import Sport, StatCategory, BetCategory


class TheOddsApiNFLWrangler(TheOddsApiWrangler):
    sport: Sport = Sport.NFL
    _outrights_key: str = "americanfootball_nfl_super_bowl_winner"
    _player_prop_markets: list[
        Literal[
            "player_pass_tds",
            "player_pass_yds",
            "player_pass_completions",
            "player_pass_attempts",
            "player_pass_interceptions",
            "player_pass_longest_completion",
            "player_rush_yds",
            "player_rush_attempts",
            "player_rush_longest",
            "player_receptions",
            "player_reception_yds",
            "player_reception_longest",
            "player_kicking_points",
            "player_field_goals",
            "player_tackles_assists",
            "player_1st_td",
            "player_last_td",
            "player_anytime_td",
            "player_pass_tds_alternate",
            "player_pass_yds_alternate",
            "player_rush_yds_alternate",
            "player_rush_reception_yds_alternate",
            "player_reception_yds_alternate",
            "player_receptions_alternate",
        ]
    ] = [
        "player_pass_tds",
        "player_pass_yds",
        "player_pass_completions",
        "player_pass_attempts",
        "player_pass_interceptions",
        "player_pass_longest_completion",
        "player_rush_yds",
        "player_rush_attempts",
        "player_rush_longest",
        "player_receptions",
        "player_reception_yds",
        "player_reception_longest",
        "player_kicking_points",
        "player_field_goals",
        "player_tackles_assists",
        "player_1st_td",
        "player_last_td",
        "player_anytime_td",
        # alternate
        "player_pass_tds_alternate",
        "player_pass_yds_alternate",
        "player_rush_yds_alternate",
        "player_rush_reception_yds_alternate",
        "player_reception_yds_alternate",
        "player_receptions_alternate",
    ]
    _player_prop_key_mapping: NFLKeyMapping = {
        "player_pass_tds": "P_".format(StatCategory.TOUCHDOWNS),
        "player_pass_yds": "P_".format(StatCategory.YARDS),
        "player_pass_completions": "P_".format(StatCategory.COMPLETIONS),
        "player_pass_attempts": "P_".format(StatCategory.ATTEMPTS),
        "player_pass_interceptions": "P_".format(StatCategory.INTERCEPTIONS),
        "player_pass_longest_completion": "P_".format(StatCategory.LONGEST),
        "player_rush_yds": "RU_".format(StatCategory.YARDS),
        "player_rush_attempts": "RU_".format(StatCategory.ATTEMPTS),
        "player_rush_longest": "RU_".format(StatCategory.LONGEST),
        "player_receptions": "RE_".format(StatCategory.RECEPTIONS),
        "player_reception_yds": "RE_".format(StatCategory.YARDS),
        "player_reception_longest": "RE_".format(StatCategory.LONGEST),
        "player_kicking_points": "K_".format(StatCategory.POINTS),
        "player_field_goals": "FG",
        "player_tackles_assists": "TOT",
        "player_1st_td": StatCategory.TOUCHDOWNS,
        "player_last_td": StatCategory.TOUCHDOWNS,
        "player_anytime_td": StatCategory.TOUCHDOWNS,
        # alternate
        "player_pass_tds_alternate": "P_{} {}".format(
            StatCategory.TOUCHDOWNS, BetCategory.ALTERNATE
        ),
        "player_pass_yds_alternate": "P_{} {}".format(
            StatCategory.YARDS, BetCategory.ALTERNATE
        ),
        "player_rush_yds_alternate": "RU_{} {}".format(
            StatCategory.YARDS, BetCategory.ALTERNATE
        ),
        "player_rush_reception_yds_alternate": "RU_RE_{} {}".format(
            StatCategory.YARDS, BetCategory.ALTERNATE
        ),
        "player_reception_yds_alternate": "RE_{} {}".format(
            StatCategory.YARDS, BetCategory.ALTERNATE
        ),
        "player_receptions_alternate": "{} {}".format(
            StatCategory.RECEPTIONS, BetCategory.ALTERNATE
        ),
    }
