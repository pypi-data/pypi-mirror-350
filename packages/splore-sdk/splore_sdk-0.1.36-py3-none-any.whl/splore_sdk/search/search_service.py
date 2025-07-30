from typing import Optional
from .validations import SearchQueryInput
from splore_sdk.core.api_client import APIClient
from splore_sdk.core.compat import model_dump_or_dict


class SearchService:
    def __init__(self, api_client: APIClient, agent_id: str):
        self.api_client = api_client
        self.search_prefix = "api/rest/v2/search"
        self.api_client.agent_id = agent_id

    def set_agent(self, agent_id):
        self.api_client.agent_id = agent_id

    def endpoint(self, endpoint):
        return self.search_prefix + endpoint

    def search(
        self, query: str, count: Optional[int] = 10, engine: Optional[str] = "google"
    ):
        """
        Perform a search query using the specified parameters.

        Args:
            query: The search query string
            count: Number of results to return (default: 10)
            engine: Search engine to use (default: "google")

        Returns:
            The search results from the API
        """
        if self.api_client.agent_id is None:
            raise ValueError(
                "For search, agent_id is required. Initialize the SDK with agent_id or call function `search.set_agent(agent_id)`"
            )

        payload = SearchQueryInput(
            query=query, agent_id=self.api_client.agent_id, count=count, engine=engine
        )

        return self.api_client.request(
            method="POST",
            endpoint=self.endpoint(""),
            json=model_dump_or_dict(payload),
        )

    def get_search_history(
        self,
        page: Optional[int] = 0,
        size: Optional[int] = 10,
    ):
        """
        Get search history for the current agent.

        Args:
            page: Page number for pagination (default: 0)
            size: Number of results per page (default: 10)

        Returns:
            The search history from the API
        """
        if self.api_client.agent_id is None:
            raise ValueError(
                "For search history, agent_id is required. Initialize the SDK with agent_id or call function `search.set_agent(agent_id)`"
            )

        params = {"agentId": self.api_client.agent_id, "page": page, "size": size}
        return self.api_client.request(
            method="GET",
            endpoint=self.endpoint("/history"),
            params=params,
        )
