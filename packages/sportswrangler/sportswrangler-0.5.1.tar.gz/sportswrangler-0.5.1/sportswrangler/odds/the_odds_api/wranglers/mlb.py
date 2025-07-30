from typing import Literal

from sportswrangler.odds.the_odds_api.utils.classes import MLBKeyMapping
from sportswrangler.odds.the_odds_api.wranglers.base import TheOddsApiWrangler
from sportswrangler.utils.enums import Sport, StatCategory, BetCategory


class TheOddsApiMLBWrangler(TheOddsApiWrangler):
    sport: Sport = Sport.MLB
    _outrights_key: str = "baseball_mlb_world_series_winner"
    _player_prop_markets: list[
        Literal[
            "batter_home_runs",
            "batter_hits",
            "batter_total_bases",
            "batter_rbis",
            "batter_runs_scored",
            "batter_hits_runs_rbis",
            "batter_singles",
            "batter_doubles",
            "batter_triples",
            "batter_walks",
            "batter_strikeouts",
            "batter_stolen_bases",
            "pitcher_strikeouts",
            "pitcher_record_a_win",
            "pitcher_hits_allowed",
            "pitcher_walks",
            "pitcher_earned_runs",
            "pitcher_outs",
            "batter_total_bases_alternate",
            "batter_home_runs_alternate",
            "batter_hits_alternate",
            "batter_rbis_alternate",
            "pitcher_hits_allowed_alternate",
            "pitcher_walks_alternate",
            "pitcher_strikeouts_alternate",
        ]
    ] = [
        "batter_home_runs",
        "batter_hits",
        "batter_total_bases",
        "batter_rbis",
        "batter_runs_scored",
        "batter_hits_runs_rbis",
        "batter_singles",
        "batter_doubles",
        "batter_triples",
        "batter_walks",
        "batter_strikeouts",
        "batter_stolen_bases",
        "pitcher_strikeouts",
        "pitcher_record_a_win",
        "pitcher_hits_allowed",
        "pitcher_walks",
        "pitcher_earned_runs",
        "pitcher_outs",
        # alternate
        "batter_total_bases_alternate",
        "batter_home_runs_alternate",
        "batter_hits_alternate",
        "batter_rbis_alternate",
        "pitcher_hits_allowed_alternate",
        "pitcher_walks_alternate",
        "pitcher_strikeouts_alternate",
    ]
    _player_prop_key_mapping: MLBKeyMapping = {
        "batter_home_runs": StatCategory.HOME_RUNS,
        "batter_hits": StatCategory.HITS,
        "batter_total_bases": StatCategory.TOTAL_BASES,
        "batter_rbis": StatCategory.RBI,
        "batter_runs_scored": StatCategory.RUNS,
        "batter_hits_runs_rbis": "{}+{}+{}".format(
            StatCategory.HITS, StatCategory.RUNS, StatCategory.RBI
        ),
        "batter_singles": "1B",
        "batter_doubles": "2B",
        "batter_triples": "3B",
        "batter_walks": StatCategory.WALKS,
        "batter_strikeouts": StatCategory.STRIKEOUTS,
        "batter_stolen_bases": "SB",
        "pitcher_strikeouts": StatCategory.STRIKEOUTS,
        "pitcher_record_a_win": "W",
        "pitcher_hits_allowed": StatCategory.HITS,
        "pitcher_walks": StatCategory.WALKS,
        "pitcher_earned_runs": "ERA",
        "pitcher_outs": "O",
        # alternate
        "batter_total_bases_alternate": "{} {}".format(
            BetCategory.ALTERNATE, StatCategory.TOTAL_BASES
        ),
        "batter_home_runs_alternate": "{} {}".format(
            BetCategory.ALTERNATE, StatCategory.HOME_RUNS
        ),
        "batter_hits_alternate": "{} {}".format(
            BetCategory.ALTERNATE, StatCategory.HITS
        ),
        "batter_rbis_alternate": "{} {}".format(
            BetCategory.ALTERNATE, StatCategory.RBI
        ),
        "pitcher_hits_allowed_alternate": "{} {}".format(
            BetCategory.ALTERNATE, StatCategory.HITS
        ),
        "pitcher_walks_alternate": "{} {}".format(
            BetCategory.ALTERNATE, StatCategory.WALKS
        ),
        "pitcher_strikeouts_alternate": "{} {}".format(
            BetCategory.ALTERNATE, StatCategory.STRIKEOUTS
        ),
    }
