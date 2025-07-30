from typing import Literal

from sportswrangler.odds.the_odds_api.utils.classes import EPLKeyMapping
from sportswrangler.odds.the_odds_api.wranglers.base import TheOddsApiWrangler
from sportswrangler.utils.enums import Sport, StatCategory, BetCategory


class TheOddsApiEPLWrangler(TheOddsApiWrangler):
    sport: Sport = Sport.EPL
    # no outrights yet
    _player_prop_markets: list[
        Literal[
            "player_goal_scorer_anytime",
            "player_first_goal_scorer",
            "player_last_goal_scorer",
            "player_to_receive_card",
            "player_to_receive_red_card",
            "player_shots_on_target",
            "player_shots",
            "player_assists",
            "alternate_spreads_corners",
            "alternate_totals_corners",
            "alternate_spreads_cards",
            "alternate_totals_cards",
            "double_chance",
        ]
    ] = [
        "player_goal_scorer_anytime",
        "player_first_goal_scorer",
        "player_last_goal_scorer",
        "player_to_receive_card",
        "player_to_receive_red_card",
        "player_shots_on_target",
        "player_shots",
        "player_assists",
        # alternates
        "alternate_spreads_corners",
        "alternate_totals_corners",
        "alternate_spreads_cards",
        "alternate_totals_cards",
        "double_chance",
    ]
    _player_prop_key_mapping: EPLKeyMapping = {
        "player_goal_scorer_anytime": StatCategory.GOAL,
        "player_first_goal_scorer": "F_" + StatCategory.GOAL,
        "player_last_goal_scorer": "L_" + StatCategory.GOAL,
        "player_to_receive_card": StatCategory.CARD,
        "player_to_receive_red_card": "R" + StatCategory.CARD,
        "player_shots_on_target": "{}G".format(StatCategory.SHOTS_ON_GOAL),
        "player_shots": StatCategory.SHOTS_ON_GOAL,
        "player_assists": StatCategory.ASSISTS,
        # alternates
        "alternate_spreads_corners": "{} {} {}".format(
            BetCategory.ALTERNATE, BetCategory.SPREAD, StatCategory.CORNER
        ),
        "alternate_totals_corners": "{} {} {}".format(
            BetCategory.ALTERNATE, BetCategory.TOTALS, StatCategory.CORNER
        ),
        "alternate_spreads_cards": "{} {} {}".format(
            BetCategory.ALTERNATE, BetCategory.SPREAD, StatCategory.CARD
        ),
        "alternate_totals_cards": "{} {} {}".format(
            BetCategory.ALTERNATE, BetCategory.TOTALS, StatCategory.CARD
        ),
        "double_chance": "DC",
    }
