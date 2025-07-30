import logging
import os

import pandas as pd
import polars as pl
from requests import Response, Session
from datetime import datetime

from sportswrangler.generic.wrangler import Wrangler
from sportswrangler.utils.enums import Sport

logger = logging.getLogger(__name__)
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


class DataFeedsWrangler(Wrangler):
    _endpoint = "http://rest.datafeeds.rolling-insights.com/api/v1"
    sport: Sport = None
    rsc_token: str = os.environ.get("DATA_FEEDS_RSC_TOKEN")
    """
    Token assigned to your account to make calls to DataFeeds
    """

    @staticmethod
    def _clean_df(raw_df):
        metadata_columns = [
            "round",
            "sport",
            "season",
            "status",
            "game_ID",
            "game_time",
            "event_name",
            "game_status",
            "season_type",
            "game_location",
            "away_team_name",
            "home_team_name",
        ]
        if isinstance(raw_df, pd.DataFrame):
            metadata = raw_df[metadata_columns]
        elif isinstance(raw_df, pl.DataFrame):
            metadata = raw_df.select(metadata_columns).to_pandas()
        else:
            raise TypeError("Input should be a pandas DataFrame or polars DataFrame")

        teams_data = []
        players_data = []

        # Helper function to flatten a dictionary with parent keys, excluding specific parent keys
        def flatten_dict(d, parent_key="", sep=".", exclude_keys=None):
            if exclude_keys is None:
                exclude_keys = []
            items = []
            for k, v in d.items():
                new_key = f"{parent_key}{sep}{k}" if parent_key else k
                if isinstance(v, dict) and k not in exclude_keys:
                    items.extend(
                        flatten_dict(
                            v, new_key, sep=sep, exclude_keys=exclude_keys
                        ).items()
                    )
                else:
                    items.append((new_key, v))
            return dict(items)

        # Combined processing for team and player data
        for index, row in raw_df.iterrows():
            game_metadata = metadata.loc[index].to_dict()
            if game_metadata["status"] != "completed":
                continue

            # Extract year, month, day from game_time
            game_time = datetime.strptime(
                game_metadata["game_time"], "%a, %d %b %Y %H:%M:%S %Z"
            )
            game_metadata["year"] = game_time.year
            game_metadata["month"] = game_time.month
            game_metadata["day"] = game_time.day

            for team_type in ["away_team", "home_team"]:
                # Process team data
                team_data = {**game_metadata, **row["full_box"][team_type]}
                team_data.update(row["full_box"][team_type]["team_stats"])
                team_data = flatten_dict(team_data, exclude_keys=["team_stats"])
                team_data.pop("team_stats")
                team_data["teamId"] = row["full_box"][team_type]["team_id"]
                team_data.pop("team_id")
                team_data["type"] = "team"
                teams_data.append(team_data)

                # Process player data
                for category, players in row["player_box"][team_type].items():
                    for player_id, stats in players.items():
                        player_data = flatten_dict({**game_metadata, **stats})
                        player_data["type"] = "player"
                        player_data["teamId"] = row["full_box"][team_type]["team_id"]
                        player_data["playerId"] = player_id
                        players_data.append(player_data)

        teams_df = pd.DataFrame(teams_data)
        players_df = pd.DataFrame(players_data)

        # Convert numeric columns to double and replace None with 'None'
        for df in [teams_df, players_df]:
            for col in df.columns:
                if df[col].dtype == "object":
                    df[col] = df[col].apply(lambda x: "None" if x is None else x)
                elif pd.api.types.is_numeric_dtype(df[col]):
                    df[col] = df[col].astype(float)

        if isinstance(raw_df, pd.DataFrame):
            return teams_df, players_df
        elif isinstance(raw_df, pl.DataFrame):
            return pl.from_pandas(teams_df), pl.from_pandas(players_df)

    def request(self, url: str, additional_params=None) -> Response:
        """
        :param url: URL string to send a get query
        :param additional_params: dict of parameters to combine with RSC_token parameter
        """
        if additional_params is None:
            additional_params = {}
        logger.debug(
            "Sending a request to {} with the parameters {} \nNote: RSC token is intentionally left out of log message.".format(
                url, additional_params
            )
        )
        params = {"RSC_token": self.rsc_token, **additional_params}
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
        return response

    def base_request(
        self,
        api_path: str,
        additional_params=None,
        sports: list[Sport] = None,
        clean: bool = False,
    ) -> (
        dict[str, list]
        | dict[str, pd.DataFrame]
        | dict[str, pl.LazyFrame]
        | dict[str, dict[str, pd.DataFrame]]
        | dict[str, dict[str, pl.LazyFrame]]
    ):
        """
        :param sports: list of sports to parse into preferred dataframe
        :param api_path: path that will be appended to http://rest.datafeeds.rolling-insights.com/api/v1
        :param additional_params: dict of parameters to combine with RSC_token parameter
        :param clean: whether to clean and flatten the data
        """
        response = self.request(
            url=self._endpoint + api_path,
            additional_params=additional_params or {},
        )
        data = response.json()["data"]
        if sports and self.preferred_dataframe:
            for sport in sports:
                df = (
                    pd.DataFrame(data[sport])
                    if self.preferred_dataframe == "pandas"
                    else pl.LazyFrame(data[sport])
                )
                if clean:
                    teams_df, players_df = self._clean_df(df)
                    data[sport] = {"team": teams_df, "player": players_df}
                    continue
                data[sport] = df
        return data

    def get_season_schedule(
        self, date: str = None, sports: list[Sport] = None, team_id: str = None
    ):
        api_path = "/schedule-season"
        additional_params = None
        if date:
            api_path += f"/{date}"
        if sports or self.sport:
            self_sport = [self.sport] if self.sport else []
            sports = sports + self_sport if sports else self_sport
            api_path += "/{}".format("-".join(sports))
        if team_id:
            if len(sports) > 1:
                raise Exception(
                    "One single sport MUST be specified if using `team_id` parameter."
                )
            additional_params = {"team_id": team_id}
        return self.base_request(api_path, additional_params, sports)

    def get_weekly_schedule(
        self, date: str = "now", sports: list[Sport] = None, team_id: str = None
    ):
        api_path = "/schedule-week"
        additional_params = None
        if date:
            api_path += f"/{date}"
        if sports or self.sport:
            self_sport = [self.sport] if self.sport else []
            sports = sports + self_sport if sports else self_sport
            api_path += "/{}".format("-".join(sports))
        if team_id:
            if len(sports) > 1:
                raise Exception(
                    "One single sport MUST be specified if using `team_id` parameter."
                )
            additional_params = {"team_id": team_id}
        return self.base_request(api_path, additional_params, sports)

    def get_daily_schedule(
        self,
        date: str = "now",
        sports: list[Sport] = None,
        team_id: str = None,
        game_id: str = None,
    ):
        api_path = "/schedule"
        additional_params = {}
        if date:
            api_path += f"/{date}"
        if sports or self.sport:
            self_sport = [self.sport] if self.sport else []
            sports = sports + self_sport if sports else self_sport
            api_path += "/{}".format("-".join(sports))
        if team_id:
            if len(sports) > 1:
                raise Exception(
                    "One single sport MUST be specified if using `team_id` parameter."
                )
            additional_params["team_id"] = team_id
        if game_id:
            if len(sports) > 1:
                raise Exception(
                    "One single sport MUST be specified if using `game_id` parameter."
                )
            additional_params["game_id"] = game_id

        return self.base_request(api_path, additional_params, sports)

    def get_live(
        self,
        date: str = "now",
        sports: list[Sport] = None,
        team_id: str = None,
        game_id: str = None,
        clean: bool = True,
    ):
        """

        :param date:  "now" or YYYY-MM-DD
        :param sports:
        :param team_id:
        :param game_id:
        :param clean:
        :return:
        """
        api_path = "/live"
        additional_params = {}
        if date:
            api_path += f"/{date}"
        if sports or self.sport:
            self_sport = [self.sport] if self.sport else []
            sports = sports + self_sport if sports else self_sport
            api_path += "/{}".format("-".join(sports))
        if team_id:
            if len(sports) > 1:
                raise Exception(
                    "One single sport MUST be specified if using `team_id` parameter."
                )
            additional_params["team_id"] = team_id
        if game_id:
            if len(sports) > 1:
                raise Exception(
                    "One single sport MUST be specified if using `game_id` parameter."
                )
            additional_params["game_id"] = game_id

        return self.base_request(
            api_path=api_path,
            additional_params=additional_params,
            sports=sports,
            clean=clean,
        )

    def get_team_info(
        self,
        sports: list[Sport] = None,
        team_id: str = None,
        from_assets: bool = True,
    ):
        if from_assets:
            data = {}
            for sport in sports or Sport.list():
                loaded = pd.read_csv(
                    os.path.join(__location__, "assets/{}/teams.csv".format(sport))
                )
                if team_id:
                    loaded = loaded[loaded["team_id" == team_id]]
                if self.preferred_dataframe != "pandas":
                    loaded = (
                        loaded.to_dict("records")
                        if not self.preferred_dataframe
                        else pl.LazyFrame(loaded)
                    )
                data[sport] = loaded
            return data
        api_path = "/team-info"
        additional_params = {}
        if sports or self.sport:
            self_sport = [self.sport] if self.sport else []
            sports = sports + self_sport if sports else self_sport
            api_path += "/{}".format("-".join(sports))
        if team_id:
            if len(sports) > 1:
                raise Exception(
                    "One single sport MUST be specified if using `team_id` parameter."
                )
            additional_params["team_id"] = team_id
        return self.base_request(api_path, additional_params, sports)

    def get_team_season_stats(
        self,
        date: str = None,
        sports: list[Sport] = None,
        team_id: str = None,
    ):
        api_path = "/team-stats"
        additional_params = {}
        if date:
            api_path += f"/{date}"
        if sports or self.sport:
            self_sport = [self.sport] if self.sport else []
            sports = sports + self_sport if sports else self_sport
            api_path += "/{}".format("-".join(sports))
        if team_id:
            if len(sports) > 1:
                raise Exception(
                    "One single sport MUST be specified if using `team_id` parameter."
                )
            additional_params["team_id"] = team_id

        return self.base_request(api_path, additional_params, sports)

    def get_player_info(
        self,
        sports: list[Sport] = None,
        team_id: str = None,
        from_assets: bool = True,
    ):
        if from_assets:
            data = {}
            for sport in sports:
                loaded = pd.read_csv(
                    os.path.join(__location__, "assets/{}/players.csv".format(sport))
                )
                if team_id:
                    loaded = loaded[loaded["team_id" == team_id]]
                if self.preferred_dataframe != "pandas":
                    loaded = (
                        loaded.to_dict("records")
                        if not self.preferred_dataframe
                        else pl.LazyFrame(loaded)
                    )
                data[sport] = loaded
            return data
        api_path = "/player-info"
        additional_params = {}
        if sports or self.sport:
            self_sport = [self.sport] if self.sport else []
            sports = sports + self_sport if sports else self_sport
            api_path += "/{}".format("-".join(sports))
        if team_id:
            if len(sports) > 1:
                raise Exception(
                    "One single sport MUST be specified if using `team_id` parameter."
                )
            additional_params["team_id"] = team_id

        return self.base_request(api_path, additional_params, sports)

    def get_player_stats(
        self,
        date: str = None,
        sports: list[Sport] = None,
        team_id: str = None,
        player_id: str = None,
    ):
        api_path = "/player-stats"
        additional_params = {}
        if date:
            api_path += f"/{date}"
        if sports or self.sport:
            self_sport = [self.sport] if self.sport else []
            sports = sports + self_sport if sports else self_sport
            api_path += "/{}".format("-".join(sports))
        if team_id:
            if len(sports) > 1:
                raise Exception(
                    "One single sport MUST be specified if using `team_id` parameter."
                )
            additional_params["team_id"] = team_id
        if player_id:
            if len(sports) > 1:
                raise Exception(
                    "One single sport MUST be specified if using `player_id` parameter."
                )
            additional_params["player_id"] = player_id

        return self.base_request(api_path, additional_params, sports)

    def get_player_injuries(
        self,
        sports: list[Sport] = None,
        team_id: str = None,
    ):
        api_path = "/injuries"
        additional_params = {}
        if sports or self.sport:
            self_sport = [self.sport] if self.sport else []
            sports = sports + self_sport if sports else self_sport
            api_path += "/{}".format("-".join(sports))
        if team_id:
            if len(sports) > 1:
                raise Exception(
                    "One single sport MUST be specified if using `team_id` parameter."
                )
            additional_params["team_id"] = team_id

        return self.base_request(api_path, additional_params, sports)

    def get_team_depth_chart(
        self,
        sports: list[Sport] = None,
        team_id: str = None,
    ):
        api_path = "/depth-charts"
        additional_params = {}
        if sports or self.sport:
            self_sport = [self.sport] if self.sport else []
            sports = sports + self_sport if sports else self_sport
            api_path += "/{}".format("-".join(sports))
        if team_id:
            if len(sports) > 1:
                raise Exception(
                    "One single sport MUST be specified if using `team_id` parameter."
                )
            additional_params["team_id"] = team_id

        return self.base_request(api_path, additional_params, sports)
