import pytest
from unittest.mock import MagicMock
from splore_sdk.agents.agents_service import AgentService


# Dummy payload classes that mimic the interface expected by AgentService.
class DummyCreateAgentInput:
    def __init__(self, data):
        self.data = data

    def model_dump(self):
        return self.data


class DummyUpdateAgentInput:
    def __init__(self, data):
        self.data = data

    def model_dump(self):
        return self.data


@pytest.fixture
def dummy_api_client():
    """Create a dummy APIClient as a MagicMock."""
    client = MagicMock()
    # dummy base_url so that endpoint concatenation works
    client.base_url = "https://api.splore.ai"
    return client


@pytest.fixture
def agent_service(dummy_api_client):
    """Instantiate AgentService with the dummy APIClient."""
    return AgentService(dummy_api_client)


def test_create_agent(agent_service, dummy_api_client):
    payload = DummyCreateAgentInput({"dummy": "data"})
    dummy_response = {"id": "agent_123", "name": "New Agent"}
    dummy_api_client.request.return_value = dummy_response

    result = agent_service.create_agent(payload)
    expected_endpoint = "api/rest/v2/agents"
    dummy_api_client.request.assert_called_once_with(
        method="POST", endpoint=expected_endpoint, json={"dummy": "data"}
    )
    assert result == dummy_response


def test_update_agent(agent_service, dummy_api_client):
    payload = DummyUpdateAgentInput({"dummy": "update"})
    dummy_response = {"id": "agent_123", "name": "Updated Agent"}
    dummy_api_client.request.return_value = dummy_response

    result = agent_service.update_agent(payload)

    expected_endpoint = "api/rest/v2/agents"
    dummy_api_client.request.assert_called_once_with(
        method="PUT", endpoint=expected_endpoint, json={"dummy": "update"}
    )
    assert result == dummy_response


def test_get_agents_no_filters(agent_service, dummy_api_client):
    dummy_response = [{"id": "agent_123", "name": "Agent 1"}]
    dummy_api_client.request.return_value = dummy_response

    result = agent_service.get_agents()

    expected_endpoint = "api/rest/v2/agents"
    dummy_api_client.request.assert_called_once_with(
        method="GET", endpoint=expected_endpoint, params={}
    )
    assert result == dummy_response


def test_get_agents_with_filters(agent_service, dummy_api_client):
    dummy_response = [{"id": "agent_123", "name": "Agent 1"}]
    dummy_api_client.request.return_value = dummy_response

    result = agent_service.get_agents(agentId="agent_123", agentName="Test Agent")

    expected_endpoint = "api/rest/v2/agents"
    dummy_api_client.request.assert_called_once_with(
        method="GET",
        endpoint=expected_endpoint,
        params={"agentId": "agent_123", "agentName": "Test Agent"},
    )
    assert result == dummy_response


def test_delete_agent(agent_service, dummy_api_client):
    dummy_response = {"message": "Deleted"}
    dummy_api_client.request.return_value = dummy_response

    result = agent_service.delete_agents("agent_123")

    # Expected endpoint for deletion is 'api/rest/v2/agents/agent_123'
    expected_endpoint = "api/rest/v2/agents/agent_123"
    dummy_api_client.request.assert_called_once_with(
        method="DELETE", endpoint=expected_endpoint
    )
    assert result == dummy_response
