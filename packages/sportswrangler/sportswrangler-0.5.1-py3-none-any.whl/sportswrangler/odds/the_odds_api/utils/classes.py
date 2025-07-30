from pydantic import BaseModel, Field
from typing_extensions import TypedDict

from sportswrangler.odds.the_odds_api.utils.enums import OddsFormat


class StandardizationConfig(BaseModel):
    """
    Configurations to be used when standardizing the data post-parsing. Only applicable if using a data frames engine.
    """

    id_vars: list[str] = [
        "sport",
        "gameStartTime",
        "lastUpdatedAt",
        "game",
        "eventId",
        "bookmaker",
        "entity",
    ]
    """Columns to use as identifier variables when melting the data frames"""
    variable_name: str = "bet"
    """Column name of the variable column when melting the data frames"""
    value_name: str = "odds"
    """Column name of the value column when melting the data frames"""
    filter_na_odds: bool = True
    """Only applicable if using a data frames engine. If this is True, any rows with NaN/0 in the post-melted odds 
    column (`StandardizationConfig.value_name`) will be filtered out"""
    leave_lazy: bool = False
    """Only applicable if using polars data frames engine. If this is True, will return a LazyFrame and not a 
    DataFrame, and you will need to call ``.collect()``"""
    filter_odds_value: int | float = None
    """The value that the odds must be greater than when going through the standardization process to be returned. 
    Default is 1 for decimal odds & -10000 for American odds"""


class CommonParams(BaseModel):
    regions: str
    bookmakers: str
    oddsFormat: OddsFormat = Field(alias="odds_format")


class MarketKeyMapping(TypedDict):
    pass


class FeaturedKeyMapping(MarketKeyMapping):
    h2h: str
    spreads: str
    totals: str


class OutrightsKeyMapping(MarketKeyMapping):
    outrights: str


class AdditionalKeyMapping(MarketKeyMapping):
    alternate_spreads: str
    alternate_totals: str
    btts: str
    draw_no_bet: str
    h2h_3_way: str
    team_totals: str
    alternate_team_totals: str


class NBAKeyMapping(MarketKeyMapping):
    player_points: str
    player_rebounds: str
    player_assists: str
    player_threes: str
    player_blocks: str
    player_steals: str
    player_turnovers: str
    player_blocks_steals: str
    player_points_rebounds_assists: str
    player_points_rebounds: str
    player_points_assists: str
    player_rebounds_assists: str
    player_first_basket: str
    player_double_double: str
    player_triple_double: str
    player_points_alternate: str
    player_rebounds_alternate: str
    player_assists_alternate: str
    player_blocks_alternate: str
    player_steals_alternate: str
    player_threes_alternate: str
    player_points_assists_alternate: str
    player_points_rebounds_alternate: str
    player_rebounds_assists_alternate: str
    player_points_rebounds_assists_alternate: str


class NFLKeyMapping(MarketKeyMapping):
    player_pass_tds: str
    player_pass_yds: str
    player_pass_completions: str
    player_pass_attempts: str
    player_pass_interceptions: str
    player_pass_longest_completion: str
    player_rush_yds: str
    player_rush_attempts: str
    player_rush_longest: str
    player_receptions: str
    player_reception_yds: str
    player_reception_longest: str
    player_kicking_points: str
    player_field_goals: str
    player_tackles_assists: str
    player_1st_td: str
    player_last_td: str
    player_anytime_td: str
    player_pass_tds_alternate: str
    player_pass_yds_alternate: str
    player_rush_yds_alternate: str
    player_rush_reception_yds_alternate: str
    player_reception_yds_alternate: str
    player_receptions_alternate: str


class NHLKeyMapping(MarketKeyMapping):
    player_goal_scorer_anytime: str
    player_points: str
    player_assists: str
    player_shots_on_goal: str
    player_total_saves: str
    player_blocked_shots: str
    player_power_play_points: str
    player_goal_scorer_first: str
    player_goal_scorer_last: str
    player_points_alternate: str
    player_assists_alternate: str
    player_power_play_points_alternate: str
    player_goals_alternate: str
    player_shots_on_goal_alternate: str
    player_blocked_shots_alternate: str
    player_total_saves_alternate: str


class MLBKeyMapping(MarketKeyMapping):
    batter_home_runs: str
    batter_hits: str
    batter_total_bases: str
    batter_rbis: str
    batter_runs_scored: str
    batter_hits_runs_rbis: str
    batter_singles: str
    batter_doubles: str
    batter_triples: str
    batter_walks: str
    batter_strikeouts: str
    batter_stolen_bases: str
    pitcher_strikeouts: str
    pitcher_record_a_win: str
    pitcher_hits_allowed: str
    pitcher_walks: str
    pitcher_earned_runs: str
    pitcher_outs: str
    batter_total_bases_alternate: str
    batter_home_runs_alternate: str
    batter_hits_alternate: str
    batter_rbis_alternate: str
    pitcher_hits_allowed_alternate: str
    pitcher_walks_alternate: str
    pitcher_strikeouts_alternate: str


class EPLKeyMapping(MarketKeyMapping):
    player_goal_scorer_anytime: str
    player_first_goal_scorer: str
    player_last_goal_scorer: str
    player_to_receive_card: str
    player_to_receive_red_card: str
    player_shots_on_target: str
    player_shots: str
    player_assists: str
    alternate_spreads_corners: str
    alternate_totals_corners: str
    alternate_spreads_cards: str
    alternate_totals_cards: str
    double_chance: str
