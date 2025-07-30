from typing import Literal

from pydantic import BaseModel, model_validator, ConfigDict
from requests import Session
from requests.adapters import HTTPAdapter
from typing_extensions import Self
from urllib3.util import Retry

from sportswrangler.global_configs import default_retry_config
from sportswrangler.utils.enums import Sport


class Wrangler(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    sport: Sport
    """
    Sport that you will be wranglin'
    """
    preferred_dataframe: Literal["pandas", "polars", None] = "polars"
    """Data frames engine that will be returned. If this is set to ``None``, you will not be able to use any methods 
    which manipulate (wrangle) the data and a list of dicts will always be returned"""
    session: Session | Literal["default", "always-new"] = "default"
    """`requests.Session` used for all requests made to the url prefix. This configuration is useful for configuring 
    timeout, retry, etc.
    
    ``"default"``: a session will be created using the `default_retry_config` & reused for the wrangler object's 
    lifetime
    
    ``"always-new"``: a new session will be created using the `default_retry_config` before every request
    
    ``requests.Session``: the provided session will be used for all of the wrangler's requests
    """
    retry_config: Retry = default_retry_config
    """`requests.Session` retry configuration. Safer than providing your own `request.Session` in the `session` field 
    as we will ensure the retry config is mounted to the best url prefix"""
    _endpoint: str
    """Endpoint requests will be sent to. Used for configuring & mounting `requests.Session`"""

    @model_validator(mode="after")
    def _create_session(self) -> Self:
        if isinstance(self.session, Session):
            return self
        if self.session == "default":
            self.session = self.new_session()

    def new_session(self) -> Session:
        s = Session()
        s.mount(self._endpoint, HTTPAdapter(max_retries=self.retry_config))
        return s
