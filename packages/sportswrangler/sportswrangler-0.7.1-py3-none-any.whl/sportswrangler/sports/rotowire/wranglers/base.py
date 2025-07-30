import logging
import os

from requests import Response, Session

from sportswrangler.sports.rotowire.utils.constants import SPORT_API_PATH_MAPPING
from sportswrangler.generic.wrangler import Wrangler

logger = logging.getLogger(__name__)
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


class RotoWireWrangler(Wrangler):
    _endpoint = "https://api.rotowire.com/"
    api_key: str = os.environ.get("ROTOWIRE_API_KEY")
    """
    API Key assigned to make calls to RotoWire API
    """

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
        params = {"key": self.api_key, "format": "json", **additional_params}
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

    def base_request(self, api_path: str, additional_params=None) -> Response:
        """
        :param api_path: path that will be appended to https://api.rotowire.com/{sport_path}
        :param additional_params: dict of parameters to combine with API Key parameter
        """
        return self.request(
            url=self._endpoint + SPORT_API_PATH_MAPPING[self.sport] + api_path,
            additional_params=additional_params or {},
        )
