from typing import Optional
from splore_sdk.core.api_client import APIClient
from .validations import CreateAgentInput, UpdateAgentInput
from splore_sdk.core.compat import model_dump_or_dict


class AgentService:
    def __init__(self, api_client: APIClient):
        self.api_client = api_client
        self.agent_prefix = "api/rest/v2/"

    def endpoint(self, endpoint):
        return self.agent_prefix + endpoint

    def create_agent(self, agent_payload: CreateAgentInput):
        return self.api_client.request(
            method="POST",
            endpoint=self.endpoint("agents"),
            json=model_dump_or_dict(agent_payload),
        )

    def update_agent(self, agent_payload: UpdateAgentInput):
        return self.api_client.request(
            method="PUT",
            endpoint=self.endpoint("agents"),
            json=model_dump_or_dict(agent_payload),
        )

    def get_agents(
        self, agentId: Optional[str] = None, agentName: Optional[str] = None
    ):
        params = {}
        if agentId:
            params["agentId"] = agentId
        if agentName:
            params["agentName"] = agentName
        return self.api_client.request(
            method="GET", endpoint=self.endpoint("agents"), params=params
        )

    def delete_agents(self, agentId: str):
        endpoint = self.endpoint("agents") + "/" + agentId
        return self.api_client.request(method="DELETE", endpoint=endpoint)
