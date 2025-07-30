import threading
from typing import Optional
import requests
from .exceptions import APIError
from .logger import sdk_logger
from .constants import BASE_URL
from splore_sdk.utils.decorators.retry_with_backoff import retry_with_backoff


class APIClient:
    def __init__(
        self,
        api_key: str,
        base_id: str,
        agent_id: Optional[str] = None,
        base_url: Optional[str] = None,
        session: Optional[requests.Session] = None,
    ):
        self.api_key = api_key
        self.agent_id = agent_id
        self.base_id = base_id
        self.base_url = base_url if base_url else BASE_URL
        self.logger = sdk_logger
        self._thread_local = threading.local()
        if session is not None:
            self._thread_local.session = session
        self.logger.debug(
            f"api client initialised with api_key: ${self.api_key}, base_url: ${base_url}"
        )

    def set_session(self, session: requests.Session):
        """Set a thread-local session for this client."""
        self._thread_local.session = session

    def get_session(self) -> requests.Session:
        """Get the thread-local session, or create one if not set."""
        if not hasattr(self._thread_local, "session"):
            self._thread_local.session = requests.Session()
        return self._thread_local.session

    @retry_with_backoff(max_retries=3, backoff_factor=0.5)
    def validate_api_key(self):
        """Validate the API key."""
        return self.request(method="GET", endpoint="api/rest/v2/authenticate")

    @retry_with_backoff(max_retries=3, backoff_factor=0.5)
    def request(self, method: str, endpoint: str, **kwargs):
        headers = kwargs.pop("headers", {})
        headers["X-API-KEY"] = self.api_key
        url = f"{self.base_url}/{endpoint}"
        try:
            self.logger.debug(
                f"api with url: {url}, method: {method} \n headers: {headers} \n started"
            )
            session = self.get_session()
            response = session.request(method, url, headers=headers, **kwargs)
            response.raise_for_status()
            self.logger.info(
                f"api with endpoint: {endpoint}, {method.upper()} succeeded"
            )
            try:
                return response.json()
            except ValueError:
                self.logger.warning(
                    f"Response is not JSON, returning raw content. URL: {url}"
                )
                return response.text
        except requests.exceptions.RequestException as e:
            self.logger.error(
                f"api with endpoint: {endpoint}, {method.upper()} failed", str(e)
            )
            raise APIError(f"API Request {url}, method: {method} failed")
