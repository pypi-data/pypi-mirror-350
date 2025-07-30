import logging
import os
from datetime import datetime
from typing import Literal, Callable

import numpy as np
import pandas as pd
import polars as pl
from dateutil import parser
from requests import Response, Session

from sportswrangler.generic.wrangler import Wrangler
from sportswrangler.odds.the_odds_api.utils.classes import (
    CommonParams,
    FeaturedKeyMapping,
    AdditionalKeyMapping,
    MarketKeyMapping,
    StandardizationConfig,
    OutrightsKeyMapping,
)
from sportswrangler.odds.the_odds_api.utils.constants import (
    SPORT_API_KEY_MAPPING,
)
from sportswrangler.odds.the_odds_api.utils.enums import (
    TheOddsApiRegion,
    TheOddsApiUsBookmaker,
    OddsFormat,
)
from sportswrangler.utils.helpers import flatten
from sportswrangler.utils.enums import BetCategory

logger = logging.getLogger(__name__)


class TheOddsApiWrangler(Wrangler):
    """
    Generic wrangler that sport specific wranglers inherit from. Currently, EPL, NBA, NFL, NHL, & MLB are supported.

    If you choose to use this generic wrangler, be aware of the following:

    - ``_player_prop_markets`` & ``_player_prop_key_mapping`` will both be empty
    - Not all sports support player props. See https://the-odds-api.com/sports-odds-data/betting-markets.html
    """

    _endpoint = "https://api.the-odds-api.com"
    api_key: str = os.environ.get("THE_ODDS_API_KEY")
    """
    https://the-odds-api.com/ API key
    """
    key_errors_threshold: int | None = None
    """While they are fairly uncommon, they still can occur. The number you set here will be the number of KeyErrors 
    to log and eat while parsing bookmaker data before throwing an exception. **Setting this to** ``None`` **means a 
    KeyError will never be thrown**"""
    log_number_of_calls_remaining: bool = False
    """
    Set this to True for the number of requests remaining until the quota resets to be logged
    """
    log_number_of_calls_used: bool = False
    """
    Set this to True for the number of requests used since the last quota reset to be logged
    """
    divider: str = "-"
    """
    Divider that will be used to build bet names (ex. points{divider}Over{divider}22.5), and replace spaces if desired
    via ``fill_spaces``
    """
    fill_spaces: bool = True
    """
    Boolean to specify whether or not spaces in game or entity strings should be replaced with the ``divider``
    """
    common_params: CommonParams = CommonParams(
        regions=",".join(TheOddsApiRegion.list()),
        bookmakers=",".join(TheOddsApiUsBookmaker.list_the_odds_api_keys()),
        odds_format=OddsFormat.DECIMAL,
    )
    """
    Common parameters that will be used across all applicable requests
    """
    standardization_config: StandardizationConfig = StandardizationConfig()
    _num_key_errors = 0
    # we will (intentionally) override these in the sport specific wranglers
    _player_prop_markets: list[str] = []
    _player_prop_key_mapping: MarketKeyMapping = {}
    _outrights_key: str = None
    # these are sport-agnostic
    _featured_markets: list[
        Literal["h2h", "spreads", "totals", "h2h_lay", "outrights_lay"]
    ] = [
        "h2h",
        "spreads",
        "totals",
    ]
    _featured_markets_key_mapping: FeaturedKeyMapping = {
        "h2h": BetCategory.H2H,
        "spreads": BetCategory.SPREAD,
        "totals": BetCategory.TOTALS,
    }
    _additional_markets: list[
        Literal[
            "alternate_spreads",
            "alternate_totals",
            "btts",
            "draw_no_bet",
            "h2h_3_way",
            "team_totals",
            "alternate_team_totals",
        ]
    ] = [
        "alternate_spreads",
        "alternate_totals",
        "btts",
        "draw_no_bet",
        "h2h_3_way",
        "team_totals",
        "alternate_team_totals",
    ]
    _additional_markets_key_mapping: AdditionalKeyMapping = {
        "alternate_spreads": "{} {}".format(BetCategory.ALTERNATE, BetCategory.SPREAD),
        "alternate_totals": "{} {}".format(BetCategory.ALTERNATE, BetCategory.TOTALS),
        "btts": "BTTS",
        "draw_no_bet": "DNB",
        "h2h_3_way": "3-Way {}".format(BetCategory.H2H),
        "team_totals": "Team " + BetCategory.TOTALS,
        "alternate_team_totals": "{} Team {}".format(
            BetCategory.ALTERNATE, BetCategory.TOTALS
        ),
    }

    @property
    def _filter_line(self):
        return (
            self.standardization_config.filter_odds_value or 1
            if self.common_params.oddsFormat == OddsFormat.DECIMAL
            else -10000
        )

    def request(self, url: str, additional_params=None) -> Response:
        """
        :param url: URL string to send a get query
        :param additional_params: dict of parameters to combine with api_key parameter
        """
        if additional_params is None:
            additional_params = {}
        logger.debug(
            "Sending a request to {} with the parameters {} \nNote: API key is intentionally left out of log message.".format(
                url, additional_params
            )
        )
        params = {"api_key": self.api_key, **additional_params}
        response = (
            self.session if isinstance(self.session, Session) else self.new_session()
        ).get(
            url=url,
            params=params,
        )
        if response.status_code != 200:
            raise Exception(
                f"Failed to get a response: status code {response.status_code}, response body {response.text}"
            )
        if self.log_number_of_calls_remaining:
            logger.info(
                "Number of calls remaining: {}".format(
                    response.headers.get("x-requests-remaining")
                )
            )
        if self.log_number_of_calls_used:
            logger.info(
                "Number of calls used: {}".format(
                    response.headers.get("x-requests-used")
                )
            )
        return response

    def base_request(
        self, api_path: str, sport_key: str = None, additional_params=None
    ) -> Response:
        """
        :param api_path: path that will be appended to https://api.the-odds-api.com/v4/sports/{sport_key}
        :param sport_key: sport key to make request for
        :param additional_params: dict of parameters to combine with api_key parameter
        """
        path = "https://api.the-odds-api.com/v4/sports/"
        response = self.request(
            url=path + (sport_key or SPORT_API_KEY_MAPPING[self.sport]) + api_path,
            additional_params=additional_params or {},
        )
        return response

    def historical_request(self, api_path: str, additional_params=None) -> Response:
        """
        :param api_path: path that will be appended to https://api.the-odds-api.com/v4/historical/sports/{sport_key}
        :param additional_params: dict of parameters to combine with api_key parameter
        """
        path = "https://api.the-odds-api.com/v4/historical/sports/"
        response = self.request(
            url=path + SPORT_API_KEY_MAPPING[self.sport] + api_path,
            additional_params=additional_params or {},
        )
        return response

    def get_events(
        self,
        ids_only: bool = True,
        starting_after: datetime = None,
    ) -> list[str | dict]:
        """
        Get a list of events for the specified sport (https://the-odds-api.com/liveapi/guides/v4/#get-events).

        :param ids_only: set this to False if you want the entire event object returned
        :param starting_after: optional datetime to filter out events that started before the datetime provided.
        """
        api_path = "/events"
        response: Response = self.base_request(api_path=api_path)

        data = response.json()
        return [
            event if not ids_only else event["id"]
            for event in data
            if not starting_after
            or starting_after < parser.parse(event["commence_time"])
        ]

    def parse_response(
        self, response: Response, market_key_mapping: MarketKeyMapping = None
    ):
        response_json = response.json()
        response_json = (
            response_json if isinstance(response_json, list) else [response_json]
        )

        data = [
            self.parse_event_data(response_data, market_key_mapping)
            for response_data in response_json
        ]
        # Flatten the list of lists
        data = list(flatten(data))
        if not self.preferred_dataframe:
            return data
        if self.preferred_dataframe == "polars":
            return pl.LazyFrame(data)
        return pd.DataFrame(data)

    def parse_event_data(
        self, response_data: dict, market_key_mapping: MarketKeyMapping = None
    ):
        event_id = response_data.get("id", "N/A")
        teams = (
            f'{response_data.get("away_team", "")}@{response_data.get("home_team", "")}'
        )
        if teams == "None@None":
            teams = "N/A"
        start_time = response_data.get("commence_time", "N/A")

        return [
            self.parse_bookmaker_data(
                bookmaker,
                event_id,
                teams,
                start_time,
                market_key_mapping,
            )
            for bookmaker in response_data.get("bookmakers", [])
        ]

    def parse_bookmaker_data(
        self,
        bookmaker: dict,
        event_id: str,
        teams: str,
        start_time: str,
        market_key_mapping: MarketKeyMapping = None,
    ):
        bookmaker_key = bookmaker["key"]
        market_data = []
        for market in bookmaker["markets"]:
            market_key = market["key"]
            last_updated = market["last_update"]
            for outcome in market["outcomes"]:
                try:
                    market_data.append(
                        self.build_market_dict(
                            outcome,
                            event_id,
                            teams,
                            start_time,
                            last_updated,
                            bookmaker_key,
                            market_key,
                            market_key_mapping,
                        )
                    )
                except KeyError as err:
                    if self.key_errors_threshold:
                        self._num_key_errors += 1
                        if self._num_key_errors >= self.key_errors_threshold:
                            logger.error("KeyErrors threshold met! Raising KeyError")
                            raise err
                    logger.info("Eating the following KeyError: {}".format(err))
                    continue
        return market_data

    def build_market_dict(
        self,
        outcome: dict,
        event_id: str,
        teams: str,
        start_time: str,
        last_updated: str,
        bookmaker_key: str,
        market_key: str,
        market_key_mapping: MarketKeyMapping = None,
    ):
        d = {
            "sport": self.sport.value,
            "gameStartTime": start_time,
            "lastUpdatedAt": last_updated,
            "game": (teams.replace(" ", self.divider) if self.fill_spaces else teams),
            "eventId": event_id,
            "bookmaker": bookmaker_key,
            "entity": (
                self.parse_entity(outcome, market_key).replace(" ", self.divider)
                if self.fill_spaces
                else self.parse_entity(outcome, market_key)
            ),
        }
        price = outcome["price"]
        # prop markets are fairly standardized, but traditional markets are not. Will have conditional chain to
        # account for the lack of standardization.
        if (
            "h2h" in market_key
            or "spreads" in market_key
            or market_key == "draw_no_bet"
            or market_key == "btts"
            or market_key == "outrights"
        ):
            if (
                "h2h" in market_key
                or market_key == "draw_no_bet"
                or market_key == "btts"
                or market_key == "outrights"
            ):
                d[self.parse_market_key(market_key, market_key_mapping)] = price
            else:
                d[
                    f"{self.parse_market_key(market_key, market_key_mapping)}{self.divider}({outcome['point']})"
                ] = price
        else:
            d[
                f"{self.parse_market_key(market_key, market_key_mapping)}{self.divider}{outcome['name']}{self.divider}{outcome['point']}"
            ] = price

        return d

    @staticmethod
    def parse_market_key(market_key: str, market_key_mapping: MarketKeyMapping = None):
        if market_key == "outrights":
            return "Champion"
        if not market_key_mapping:
            return market_key
        return market_key_mapping[market_key]  # type: ignore

    @staticmethod
    def parse_entity(outcome: dict, key: str):
        # These keys use the same entity format, group them
        if (
            "h2h" in key
            or "spreads" in key
            or key == "draw_no_bet"
            or key == "btts"
            or key == "outrights"
        ):
            return outcome["name"]
        elif "total" in key and "team" not in key:
            return "Game"
        else:
            return outcome["description"]

    def get_event_odds(
        self,
        event_id: str,
        markets: list[str],
        market_key_mapping: MarketKeyMapping = None,
    ):
        response = self.base_request(
            api_path="/events/{}/odds".format(event_id),
            additional_params={
                **self.common_params.model_dump(),
                "markets": ",".join(markets),
            },
        )
        return self.parse_response(response, market_key_mapping)

    def get_historic_event_odds(
        self,
        event_id: str,
        timestamp: datetime,
        markets: list[str],
        market_key_mapping: MarketKeyMapping = None,
    ):
        response = self.historical_request(
            api_path="/events/{}/odds".format(event_id),
            additional_params={
                **self.common_params.model_dump(),
                "markets": ",".join(markets),
                "date": timestamp.strftime("%Y-%m-%dT%H:%M:%S") + "Z",
            },
        )
        return self.parse_response(response, market_key_mapping)

    def get_additional_markets_event_odds(self, event_id: str):
        return self.get_event_odds(
            event_id,
            self._additional_markets,
            self._additional_markets_key_mapping,
        )

    def get_sport_odds(self):
        response = self.base_request(
            api_path="/odds",
            additional_params={
                **self.common_params.model_dump(),
                "markets": ",".join(self._featured_markets),
            },
        )
        return self.parse_response(response, self._featured_markets_key_mapping)

    def get_historical_sport_odds(self, timestamp: datetime):
        response = self.historical_request(
            api_path="/odds",
            additional_params={
                **self.common_params.model_dump(),
                "markets": ",".join(self._featured_markets),
                "date": timestamp.strftime("%Y-%m-%dT%H:%M:%S") + "Z",
            },
        )
        return self.parse_response(response, self._featured_markets_key_mapping)

    def get_player_prop_odds(self, event_id: str):
        return self.get_event_odds(
            event_id=event_id,
            markets=self._player_prop_markets,
            market_key_mapping=self._player_prop_key_mapping,
        )

    def standardize_odds(
        self, df: list | pd.DataFrame | pl.LazyFrame
    ) -> list | pd.DataFrame | pl.LazyFrame:
        # Only standardize DataFrames
        if isinstance(df, list):
            return df
        elif isinstance(df, pd.DataFrame):
            if df.empty:
                return df
            melted_df = pd.melt(
                df,
                id_vars=self.standardization_config.id_vars,
                var_name=self.standardization_config.variable_name,
                value_name=self.standardization_config.value_name,
            )
            return (
                melted_df[
                    (
                        melted_df[self.standardization_config.value_name].values
                        > self._filter_line
                    )
                    & (
                        ~np.isnan(
                            melted_df[self.standardization_config.value_name].values
                        )
                    )
                ]
                if self.standardization_config.filter_na_odds
                else melted_df
            )
        elif isinstance(df, pl.LazyFrame):
            if df.limit(1).collect().is_empty():
                return df
            melted_df = df.melt(
                id_vars=self.standardization_config.id_vars,
                variable_name=self.standardization_config.variable_name,
                value_name=self.standardization_config.value_name,
            )
            return (
                melted_df.filter(
                    (pl.col(self.standardization_config.value_name) > self._filter_line)
                    & (
                        pl.col(self.standardization_config.value_name)
                        .is_not_nan()
                        .is_not_null()
                    )
                )
                if self.standardization_config.filter_na_odds
                else melted_df
            )
        else:
            msg = f"did not expect type: {type(df).__name__!r} in `standardize_odds`"
            raise TypeError(msg)

    def merge_dfs(
        self,
        dfs: list[list] | list[pd.DataFrame] | list[pl.LazyFrame],
    ) -> list | pd.DataFrame | pl.DataFrame | pl.LazyFrame:
        first_item = next(iter(dfs), None)
        if isinstance(first_item, pd.DataFrame):
            return pd.concat(dfs)
        if isinstance(first_item, pl.LazyFrame):
            # If we give concat a LazyFrame, it will return a LazyFrame
            # https://github.com/pola-rs/polars/blob/main/py-polars/polars/functions/eager.py#L213
            merged_dfs: pl.LazyFrame = pl.concat(dfs)  # type: ignore
            if self.standardization_config.leave_lazy:
                return merged_dfs
            return merged_dfs.collect()
        return dfs

    def get_from_all_events(
        self,
        to_get: Callable[[str], list | pd.DataFrame | pl.LazyFrame],
        standardize: bool = True,
        starting_after: datetime = None,
    ):
        dfs = [
            (self.standardize_odds(to_get(e)) if standardize else to_get(e))
            for e in self.get_events(starting_after=starting_after)
        ]
        return self.merge_dfs(dfs)

    def get_all_player_prop_odds(
        self, standardize: bool = True, starting_after: datetime = None
    ):
        return self.get_from_all_events(
            self.get_player_prop_odds, standardize, starting_after
        )

    def get_all_additional_markets_odds(
        self, standardize: bool = True, starting_after: datetime = None
    ):
        return self.get_from_all_events(
            self.get_additional_markets_event_odds, standardize, starting_after
        )

    def get_traditional_odds(self, standardize: bool = True):
        return (
            self.standardize_odds(self.get_sport_odds())
            if standardize
            else self.get_sport_odds()
        )

    def get_all_event_odds(
        self,
        event_id: str = None,
        standardize: bool = True,
        starting_after: datetime = None,
    ):
        """
        Gets all odds available for an event using ``get_player_prop_odds`` & ``get_additional_markets_event_odds``

        - If ``event_id`` is provided, only odds for that event are returned
        - If ``starting_after`` is provided, odds for applicable events are returned
        NOTE: ``event_id`` takes precedence over ``starting_after``
        :param event_id: event id to get odds for
        :param standardize: if this is False, the results per event will not be sent to ``standardize_odds``
        :param starting_after: datetime that will be passed to ``get_events``
        """
        events = (
            [event_id] if event_id else self.get_events(starting_after=starting_after)
        )
        dfs = [
            df
            for event in events
            for df in (
                (
                    self.standardize_odds(self.get_player_prop_odds(event_id=event))
                    if standardize
                    else self.get_player_prop_odds(event_id=event)
                ),
                (
                    self.standardize_odds(
                        self.get_additional_markets_event_odds(event_id=event)
                    )
                    if standardize
                    else self.get_additional_markets_event_odds(event_id=event)
                ),
            )
        ]
        return self.merge_dfs(dfs)

    def get_futures_odds(self, standardize: bool = True):
        if not self._outrights_key:
            raise NotImplementedError("Futures odds are not available for this league")

        response = self.base_request(
            api_path="/odds",
            sport_key=self._outrights_key,
            additional_params={
                **self.common_params.model_dump(),
                "markets": "outrights",
            },
        )
        parsed_response = self.parse_response(response)

        return (
            self.standardize_odds(parsed_response) if standardize else parsed_response
        )
