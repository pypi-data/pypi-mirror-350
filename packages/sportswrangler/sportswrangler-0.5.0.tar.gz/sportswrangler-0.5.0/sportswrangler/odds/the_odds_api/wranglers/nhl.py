from typing import Literal

from sportswrangler.odds.the_odds_api.utils.classes import NHLKeyMapping
from sportswrangler.odds.the_odds_api.wranglers.base import TheOddsApiWrangler
from sportswrangler.utils.enums import Sport, StatCategory, BetCategory


class TheOddsApiNHLWrangler(TheOddsApiWrangler):
    sport: Sport = Sport.NHL
    _outrights_key: str = "icehockey_nhl_championship_winner"
    _player_prop_markets: list[
        Literal[
            "player_goal_scorer_anytime",
            "player_points",
            "player_assists",
            "player_shots_on_goal",
            "player_total_saves",
            "player_blocked_shots",
            "player_power_play_points",
            "player_goal_scorer_first",
            "player_goal_scorer_last",
            "player_points_alternate",
            "player_assists_alternate",
            "player_power_play_points_alternate",
            "player_goals_alternate",
            "player_shots_on_goal_alternate",
            "player_blocked_shots_alternate",
            "player_total_saves_alternate",
        ]
    ] = [
        "player_goal_scorer_anytime",
        "player_points",
        "player_assists",
        "player_shots_on_goal",
        "player_total_saves",
        "player_blocked_shots",
        "player_power_play_points",
        "player_goal_scorer_first",
        "player_goal_scorer_last",
        # alternates
        "player_points_alternate",
        "player_assists_alternate",
        "player_power_play_points_alternate",
        "player_goals_alternate",
        "player_shots_on_goal_alternate",
        "player_blocked_shots_alternate",
        "player_total_saves_alternate",
    ]
    _player_prop_key_mapping: NHLKeyMapping = {
        "player_goal_scorer_anytime": StatCategory.GOAL,
        "player_points": StatCategory.POINTS,
        "player_assists": StatCategory.ASSISTS,
        "player_shots_on_goal": StatCategory.SHOTS_ON_GOAL,
        "player_total_saves": StatCategory.SAVES,
        "player_blocked_shots": StatCategory.BLOCKS,
        "player_power_play_points": StatCategory.POWER_PLAY_POINTS,
        "player_goal_scorer_first": "F_" + StatCategory.GOAL,
        "player_goal_scorer_last": "L_" + StatCategory.GOAL,
        # alternates
        "player_points_alternate": "{} {}".format(
            BetCategory.ALTERNATE, StatCategory.POINTS
        ),
        "player_assists_alternate": "{} {}".format(
            BetCategory.ALTERNATE, StatCategory.ASSISTS
        ),
        "player_power_play_points_alternate": "{} {}".format(
            BetCategory.ALTERNATE, StatCategory.POWER_PLAY_POINTS
        ),
        "player_goals_alternate": "{} {}".format(
            BetCategory.ALTERNATE, StatCategory.GOAL
        ),
        "player_shots_on_goal_alternate": "{} {}".format(
            BetCategory.ALTERNATE, StatCategory.SHOTS_ON_GOAL
        ),
        "player_blocked_shots_alternate": "{} {}".format(
            BetCategory.ALTERNATE, StatCategory.BLOCKS
        ),
        "player_total_saves_alternate": "{} {}".format(
            BetCategory.ALTERNATE, StatCategory.SAVES
        ),
    }
