from urllib3.util import Retry

default_retry_config: Retry = Retry(
    total=50, backoff_factor=0.25, status_forcelist=[429]
)
