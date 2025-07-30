from typing import Optional
import pytest
from unittest.mock import MagicMock, patch
from splore_sdk.search.search_service import SearchService
from splore_sdk.core.compat import model_dump_or_dict
from splore_sdk.core.api_client import APIClient
from splore_sdk.search.validations import SearchQueryInput


@pytest.fixture
def mock_api_client():
    return MagicMock(spec=APIClient)


@pytest.fixture
def search_service(mock_api_client):
    return SearchService(api_client=mock_api_client, agent_id="test_agent")


def test_search(search_service, mock_api_client):
    # Setup mock response
    mock_api_client.request.return_value = {
        "results": [
            {
                "title": "Machine Learning - Wikipedia",
                "link": "https://en.wikipedia.org/wiki/Machine_learning",
                "snippet": "Machine learning is a branch of artificial intelligence...",
            }
        ]
    }

    # Test parameters
    query = "What is machine learning?"
    count = 5
    engine = "google"

    # Call the search method
    response = search_service.search(query=query, count=count, engine=engine)

    # Assert the response
    assert response == {
        "results": [
            {
                "title": "Machine Learning - Wikipedia",
                "link": "https://en.wikipedia.org/wiki/Machine_learning",
                "snippet": "Machine learning is a branch of artificial intelligence...",
            }
        ]
    }

    # Verify correct API call
    payload = model_dump_or_dict(
        SearchQueryInput(query=query, agent_id="test_agent", count=count, engine=engine)
    )

    mock_api_client.request.assert_called_once_with(
        method="POST",
        endpoint="api/rest/v2/search",
        json=payload,
    )


def test_get_search_history(search_service, mock_api_client):
    # Setup mock response
    mock_api_client.request.return_value = {
        "items": [
            {
                "id": "search1",
                "query": "What is machine learning?",
                "createdAt": "2025-04-08T12:00:00Z",
                "results": 5,
            }
        ],
        "total": 1,
        "page": 0,
        "size": 10,
    }

    # Test parameters
    page = 0
    size = 10

    # Call the get_search_history method
    response = search_service.get_search_history(page=page, size=size)

    # Assert the response
    assert response == {
        "items": [
            {
                "id": "search1",
                "query": "What is machine learning?",
                "createdAt": "2025-04-08T12:00:00Z",
                "results": 5,
            }
        ],
        "total": 1,
        "page": 0,
        "size": 10,
    }

    # Verify correct API call
    mock_api_client.request.assert_called_once_with(
        method="GET",
        endpoint="api/rest/v2/search/history",
        params={"agentId": "test_agent", "page": page, "size": size},
    )


def test_set_agent(search_service):
    # Test setting a new agent ID
    new_agent_id = "new_test_agent"
    search_service.set_agent(new_agent_id)

    # Verify the agent ID was updated
    assert search_service.api_client.agent_id == new_agent_id


def test_search_with_missing_agent_id(search_service, mock_api_client):
    # Set agent_id to None to test error handling
    search_service.api_client.agent_id = None

    # Test parameters
    query = "What is machine learning?"

    # Verify that a ValueError is raised when agent_id is missing
    with pytest.raises(ValueError) as excinfo:
        search_service.search(query=query)

    assert "agent_id is required" in str(excinfo.value)

    # Verify that no API request was made
    mock_api_client.request.assert_not_called()


def test_get_search_history_with_missing_agent_id(search_service, mock_api_client):
    # Set agent_id to None to test error handling
    search_service.api_client.agent_id = None

    # Verify that a ValueError is raised when agent_id is missing
    with pytest.raises(ValueError) as excinfo:
        search_service.get_search_history()

    assert "agent_id is required" in str(excinfo.value)

    # Verify that no API request was made
    mock_api_client.request.assert_not_called()
