import json
import logging

import pandas as pd
import polars as pl
import re
from requests import Response, Session

from sportswrangler.generic.wrangler import Wrangler
from sportswrangler.utils.enums import Sport
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class KeepTradeCutWrangler(Wrangler):
    _endpoint = "https://keeptradecut.com"
    sport: Sport = Sport.NFL
    delimiter: str = "_"
    """
    Delimiter used for flattening values 
    """

    def request(self, url: str) -> Response:
        """
        :param url: URL string to send a get query
        """
        logger.debug("Sending a request to {}.".format(url))

        response = (
            self.session if isinstance(self.session, Session) else self.new_session()
        ).get(
            url=url,
        )
        if response.status_code != 200:
            raise Exception(
                f"Failed to get a response: status code {response.status_code}, response body {response.text}"
            )
        return response

    def base_request(self, api_path: str) -> list[dict] | pd.DataFrame | pl.LazyFrame:
        """
        :param api_path: path that will be appended to https://keeptradecut.com
        """
        response = self.request(
            url=self._endpoint + api_path,
        )
        data = []
        request_content = response.content
        soup = BeautifulSoup(request_content, features="html.parser")
        for script in soup.find_all("script"):
            script_text = script.text
            if re.search(r"\bvar\splayersArray\b", script_text):
                # get javascript object inside the script
                match = re.search(
                    r"var playersArray = (\[.*?\]);", script_text, re.DOTALL
                )
                if match:
                    # Extract the array of objects as a string
                    array_string = match.group(1)
                    data = json.loads(array_string)
                    # Convert the string to a Python list of dicts
                    # data = ast.literal_eval(array_string)
                    break
        if data:
            data = self._parse_data(data)
        return data

    def _parse_data(self, data: list[dict]) -> list[dict] | pd.DataFrame | pl.LazyFrame:
        df = pd.json_normalize(data, sep=self.delimiter)
        match self.preferred_dataframe:
            case "pandas":
                return df
            case "polars":
                return pl.LazyFrame(df)
            case _:
                return df.to_dict("records")

    def get_player_rankings(self):
        api_path = "/dynasty-rankings"
        return self.base_request(api_path)

    def get_prospect_rankings(self):
        api_path = "/devy-rankings"
        return self.base_request(api_path)
