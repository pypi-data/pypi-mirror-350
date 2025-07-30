import pytest
from time import sleep
from unittest.mock import patch, MagicMock

# Import from the SDK module so that our patch targets are effective.
from splore_sdk.sdk import BaseSDK, SploreSDK, AgentSDK

# ----------------------
# Fixtures to patch dependencies in the SDK module
# ----------------------


@pytest.fixture
def mock_api_client():
    """
    Patch APIClient in splore_sdk.sdk so that any instantiation within BaseSDK uses the mock.
    """
    with patch("splore_sdk.sdk.APIClient") as MockAPIClient:
        instance = MagicMock()
        # Prevent real HTTP calls by having validate_api_key return True.
        instance.validate_api_key.return_value = True
        # Provide a dummy base_url.
        instance.base_url = "https://api.splore.ai"
        MockAPIClient.return_value = instance
        yield instance


@pytest.fixture
def mock_file_uploader():
    """
    Patch FileUploader in splore_sdk.sdk to prevent real file uploads.
    """
    with patch("splore_sdk.sdk.FileUploader") as MockFileUploader:
        instance = MagicMock()
        instance.upload_file.return_value = "file_123"
        MockFileUploader.return_value = instance
        yield instance


@pytest.fixture
def mock_agent_service():
    """
    Patch AgentService in splore_sdk.sdk (where it's imported) so that SploreSDK.agents is a mock.
    """
    with patch("splore_sdk.sdk.AgentService") as MockAgentService:
        instance = MagicMock()
        instance.get_agents.return_value = [{"id": "agent_123", "name": "Test Agent"}]
        MockAgentService.return_value = instance
        yield instance


@pytest.fixture
def mock_extraction_service():
    """
    Patch ExtractionService in splore_sdk.sdk (where it's imported) so that AgentSDK.extractions is a mock.
    """
    with patch("splore_sdk.sdk.ExtractionService") as MockExtractionService:
        instance = MagicMock()
        instance.set_agent.return_value = None
        instance.start.return_value = None
        instance.processing_status.return_value = {"fileProcessingStatus": "COMPLETED"}
        instance.extracted_response.return_value = {"data": "extracted_content"}
        MockExtractionService.return_value = instance
        yield instance


@pytest.fixture
def mock_search_service():
    """
    Patch SearchService in splore_sdk.sdk (where it's imported) so that AgentSDK.search is a mock.
    """
    with patch("splore_sdk.sdk.SearchService") as MockSearchService:
        instance = MagicMock()
        instance.set_agent.return_value = None
        instance.search.return_value = {
            "results": [
                {
                    "title": "Machine Learning - Wikipedia",
                    "link": "https://en.wikipedia.org/wiki/Machine_learning",
                    "snippet": "Machine learning is a branch of artificial intelligence...",
                }
            ]
        }
        instance.get_search_history.return_value = {
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
        MockSearchService.return_value = instance
        yield instance


@pytest.fixture
def mock_capabilities():
    """
    Patch capability classes in splore_sdk.sdk for AgentSDK initialization
    """
    with patch(
        "splore_sdk.sdk.ExtractionCapability"
    ) as MockExtractionCapability, patch(
        "splore_sdk.sdk.SearchCapability"
    ) as MockSearchCapability:

        extraction_instance = MagicMock()
        extraction_instance.extract.return_value = {"data": "extracted_content"}
        MockExtractionCapability.return_value = extraction_instance

        search_instance = MagicMock()
        search_instance.search.return_value = {
            "results": [
                {
                    "title": "Machine Learning - Wikipedia",
                    "link": "https://en.wikipedia.org/wiki/Machine_learning",
                    "snippet": "Machine learning is a branch of artificial intelligence...",
                }
            ]
        }
        search_instance.get_history.return_value = {
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
        MockSearchCapability.return_value = search_instance

        yield {"extraction": extraction_instance, "search": search_instance}


# ----------------------
# Tests for BaseSDK
# ----------------------


class TestBaseSDK:
    def test_missing_api_key_raises_error(self, mock_api_client, mock_file_uploader):
        with pytest.raises(ValueError, match="API Key is required to initialize SDK."):
            BaseSDK("", "base_1")

    def test_validate_api_key_called(self, mock_api_client, mock_file_uploader):
        sdk = BaseSDK("test_api_key", "base_1")
        # validate_api_key should be called during __init__
        mock_api_client.validate_api_key.assert_called_once()
        # The client attribute should be the patched instance.
        assert sdk.client == mock_api_client


# ----------------------
# Tests for SploreSDK
# ----------------------


class TestSploreSDK:
    @pytest.fixture
    def splore_sdk_instance(
        self, mock_api_client, mock_file_uploader, mock_agent_service
    ):
        return SploreSDK("test_api_key", "base_1", user_id="user_1")

    def test_initialization(self, splore_sdk_instance, mock_api_client):
        assert splore_sdk_instance.api_key == "test_api_key"
        assert splore_sdk_instance.base_id == "base_1"
        # validate_api_key is called in BaseSDK.__init__
        mock_api_client.validate_api_key.assert_called_once()
        # SploreSDK should have an 'agents' attribute.
        assert hasattr(splore_sdk_instance, "agents")

    def test_get_agents_no_filters(self, splore_sdk_instance, mock_agent_service):
        agents = splore_sdk_instance.get_agents()
        # Now the patched AgentService's get_agents should be called.
        mock_agent_service.get_agents.assert_called_once_with(
            agentId=None, agentName=None
        )
        assert agents == [{"id": "agent_123", "name": "Test Agent"}]

    def test_get_agents_with_filters(self, splore_sdk_instance, mock_agent_service):
        agents = splore_sdk_instance.get_agents(agentId="agent_123")
        mock_agent_service.get_agents.assert_called_once_with(
            agentId="agent_123", agentName=None
        )
        assert agents == [{"id": "agent_123", "name": "Test Agent"}]

    def test_init_agent_raises_error_when_empty(self, splore_sdk_instance):
        with pytest.raises(
            ValueError, match="Agent ID is required to initialize an agent."
        ):
            splore_sdk_instance.init_agent("")

    def test_init_agent_returns_agent_sdk(self, splore_sdk_instance):
        # Patch AgentSDK in splore_sdk.sdk so that init_agent returns a dummy.
        with patch("splore_sdk.sdk.AgentSDK") as MockAgentSDK:
            dummy_agent = MagicMock()
            MockAgentSDK.return_value = dummy_agent
            agent_instance = splore_sdk_instance.init_agent("agent_123")
            MockAgentSDK.assert_called_once_with(
                api_key="test_api_key", base_id="base_1", agent_id="agent_123"
            )
            assert agent_instance == dummy_agent


# ----------------------
# Tests for AgentSDK
# ----------------------


class TestAgentSDK:
    @pytest.fixture
    def agent_sdk_instance(
        self,
        mock_api_client,
        mock_file_uploader,
        mock_extraction_service,
        mock_search_service,
        mock_capabilities,
    ):
        return AgentSDK("test_api_key", "base_1", "agent_123")

    def test_initialization(
        self,
        agent_sdk_instance,
        mock_api_client,
        mock_extraction_service,
        mock_search_service,
        mock_capabilities,
    ):
        assert agent_sdk_instance.api_key == "test_api_key"
        assert agent_sdk_instance.base_id == "base_1"
        assert agent_sdk_instance.agent_id == "agent_123"
        mock_api_client.validate_api_key.assert_called_once()
        # ExtractionService should be attached for backwards compatibility
        assert hasattr(agent_sdk_instance, "extractions")
        # SearchService should be attached for backwards compatibility
        assert hasattr(agent_sdk_instance, "search")
        # Capabilities should be attached
        assert hasattr(agent_sdk_instance, "_extraction")
        assert hasattr(agent_sdk_instance, "_search")
        # Property accessors should work
        assert agent_sdk_instance.extraction == mock_capabilities["extraction"]
        assert agent_sdk_instance.search == mock_capabilities["search"]

    def test_extract_without_file_raises_error(self, agent_sdk_instance):
        with pytest.raises(
            ValueError,
            match="One of file_path or file_stream must be provided.",
        ):
            agent_sdk_instance.extract()

    def test_extract_with_file_path_success(
        self, agent_sdk_instance, mock_capabilities
    ):
        result = agent_sdk_instance.extract(file_path="dummy.txt")
        mock_capabilities["extraction"].extract.assert_called_once_with(
            file_path="dummy.txt", file_stream=None, max_poll_timeout=1200
        )
        assert result == {"data": "extracted_content"}

    def test_extract_with_file_stream_success(
        self, agent_sdk_instance, mock_capabilities
    ):
        fake_stream = MagicMock()
        result = agent_sdk_instance.extract(file_stream=fake_stream)
        mock_capabilities["extraction"].extract.assert_called_once_with(
            file_path=None, file_stream=fake_stream, max_poll_timeout=1200
        )
        assert result == {"data": "extracted_content"}

    # Since polling is now handled internally by the ExtractionCapability class,
    # we don't need to test it directly in the AgentSDK

    def test_search_query(self, agent_sdk_instance, mock_capabilities):
        result = agent_sdk_instance.search_query(
            query="What is machine learning?", count=5, engine="google"
        )
        mock_capabilities["search"].search.assert_called_once_with(
            query="What is machine learning?", count=5, engine="google"
        )
        assert result == {
            "results": [
                {
                    "title": "Machine Learning - Wikipedia",
                    "link": "https://en.wikipedia.org/wiki/Machine_learning",
                    "snippet": "Machine learning is a branch of artificial intelligence...",
                }
            ]
        }

    def test_search_query_without_agent_id(self, agent_sdk_instance):
        # Remove agent_id to test validation
        agent_sdk_instance.agent_id = None
        with pytest.raises(ValueError, match="Agent ID is required for search query."):
            agent_sdk_instance.search_query(query="What is machine learning?")

    def test_get_search_history(self, agent_sdk_instance, mock_capabilities):
        result = agent_sdk_instance.get_search_history(page=0, size=10)
        mock_capabilities["search"].get_history.assert_called_once_with(page=0, size=10)
        assert result == {
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

    def test_get_search_history_without_agent_id(self, agent_sdk_instance):
        # Remove agent_id to test validation
        agent_sdk_instance.agent_id = None
        with pytest.raises(
            ValueError, match="Agent ID is required for search history."
        ):
            agent_sdk_instance.get_search_history()
