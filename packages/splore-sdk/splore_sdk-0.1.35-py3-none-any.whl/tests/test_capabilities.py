# import pytest
# from unittest.mock import patch, MagicMock

# from splore_sdk.sdk import (
#     AgentCapability,
#     ExtractionCapability,
#     SearchCapability,
#     AgentSDK
# )
# from splore_sdk.core.api_client import APIClient
# from splore_sdk.utils.file_uploader import FileUploader


# @pytest.fixture
# def mock_api_client():
#     mock = MagicMock(spec=APIClient)
#     mock.agent_id = "test_agent_id"
#     return mock


# @pytest.fixture
# def mock_file_uploader():
#     mock = MagicMock(spec=FileUploader)
#     mock.upload_file.return_value = "file_123"
#     return mock


# @pytest.fixture
# def mock_logger():
#     return MagicMock()


# class TestAgentCapability:
#     def test_initialization(self, mock_api_client, mock_logger):
#         capability = AgentCapability(
#             client=mock_api_client,
#             agent_id="test_agent_id",
#             logger=mock_logger
#         )

#         assert capability.client == mock_api_client
#         assert capability.agent_id == "test_agent_id"
#         assert capability.logger == mock_logger


# class TestExtractionCapability:
#     @pytest.fixture
#     def mock_extraction_service(self):
#         with patch("splore_sdk.sdk.ExtractionService") as mock_service:
#             instance = MagicMock()
#             instance.set_agent.return_value = None
#             instance.start.return_value = None
#             instance.processing_status.return_value = {"fileProcessingStatus": "COMPLETED"}
#             instance.extracted_response.return_value = {"data": "extracted_content"}
#             mock_service.return_value = instance
#             yield instance

#     @pytest.fixture
#     def extraction_capability(self, mock_api_client, mock_file_uploader, mock_logger, mock_extraction_service):
#         with patch("splore_sdk.sdk.ExtractionService", return_value=mock_extraction_service):
#             return ExtractionCapability(
#                 client=mock_api_client,
#                 agent_id="test_agent_id",
#                 file_uploader=mock_file_uploader,
#                 logger=mock_logger
#             )

#     def test_initialization(self, extraction_capability, mock_api_client, mock_file_uploader, mock_logger):
#         assert extraction_capability.client == mock_api_client
#         assert extraction_capability.agent_id == "test_agent_id"
#         assert extraction_capability.file_uploader == mock_file_uploader
#         assert extraction_capability.logger == mock_logger
#         assert hasattr(extraction_capability, "service")

#     def test_extract_success(self, extraction_capability, mock_file_uploader, mock_extraction_service):
#         result = extraction_capability.extract(file_path="test.pdf")

#         # Check file upload was called
#         mock_file_uploader.upload_file.assert_called_once_with(
#             file_path="test.pdf", file_stream=None
#         )

#         # Check extraction service methods were called
#         mock_extraction_service.set_agent.assert_called_once_with(agent_id="test_agent_id")
#         mock_extraction_service.start.assert_called_once_with(file_id="file_123")
#         mock_extraction_service.processing_status.assert_called_once_with(file_id="file_123")
#         mock_extraction_service.extracted_response.assert_called_once_with(file_id="file_123")

#         # Check correct result was returned
#         assert result == {"data": "extracted_content"}

#     def test_extract_polling(self, extraction_capability, mock_extraction_service):
#         # Setup mock to return "IN_PROGRESS" first, then "COMPLETED"
#         mock_extraction_service.processing_status.side_effect = [
#             {"fileProcessingStatus": "IN_PROGRESS"},
#             {"fileProcessingStatus": "COMPLETED"}
#         ]

#         with patch("splore_sdk.sdk.sleep") as mock_sleep:
#             result = extraction_capability.extract(file_path="test.pdf")

#         # Verify polling behavior
#         assert mock_extraction_service.processing_status.call_count == 2
#         mock_sleep.assert_called_once_with(10)
#         assert result == {"data": "extracted_content"}

#     def test_extract_validation_error(self, extraction_capability):
#         # Test error when no file path or stream provided
#         with pytest.raises(ValueError, match="One of file_path or file_stream must be provided."):
#             extraction_capability.extract()

#         # Test error when agent_id is None
#         extraction_capability.agent_id = None
#         with pytest.raises(ValueError, match="Agent ID is required for extraction flow."):
#             extraction_capability.extract(file_path="test.pdf")


# class TestSearchCapability:
#     @pytest.fixture
#     def mock_search_service(self):
#         with patch("splore_sdk.sdk.SearchService") as mock_service:
#             instance = MagicMock()
#             instance.set_agent.return_value = None
#             instance.search.return_value = {
#                 "results": [
#                     {
#                         "title": "Test Result",
#                         "link": "https://example.com",
#                         "snippet": "This is a test result"
#                     }
#                 ]
#             }
#             instance.get_search_history.return_value = {
#                 "items": [{"query": "test query"}],
#                 "total": 1
#             }
#             mock_service.return_value = instance
#             yield instance

#     @pytest.fixture
#     def search_capability(self, mock_api_client, mock_logger, mock_search_service):
#         with patch("splore_sdk.sdk.SearchService", return_value=mock_search_service):
#             return SearchCapability(
#                 client=mock_api_client,
#                 agent_id="test_agent_id",
#                 logger=mock_logger
#             )

#     def test_initialization(self, search_capability, mock_api_client, mock_logger):
#         assert search_capability.client == mock_api_client
#         assert search_capability.agent_id == "test_agent_id"
#         assert search_capability.logger == mock_logger
#         assert hasattr(search_capability, "service")

#     def test_search(self, search_capability, mock_search_service):
#         result = search_capability.search(
#             query="test query",
#             count=5,
#             engine="google"
#         )

#         # Check search service was called correctly
#         mock_search_service.set_agent.assert_called_once_with(agent_id="test_agent_id")
#         mock_search_service.search.assert_called_once_with(
#             query="test query",
#             count=5,
#             engine="google"
#         )

#         # Check expected result
#         assert result["results"][0]["title"] == "Test Result"

#     def test_search_validation_error(self, search_capability):
#         # Test error when agent_id is None
#         search_capability.agent_id = None
#         with pytest.raises(ValueError, match="Agent ID is required for search query."):
#             search_capability.search(query="test query")

#     def test_get_history(self, search_capability, mock_search_service):
#         result = search_capability.get_history(page=0, size=10)

#         # Check search service was called correctly
#         mock_search_service.set_agent.assert_called_once_with(agent_id="test_agent_id")
#         mock_search_service.get_search_history.assert_called_once_with(page=0, size=10)

#         # Check expected result
#         assert result["items"][0]["query"] == "test query"
#         assert result["total"] == 1

#     def test_get_history_validation_error(self, search_capability):
#         # Test error when agent_id is None
#         search_capability.agent_id = None
#         with pytest.raises(ValueError, match="Agent ID is required for search history."):
#             search_capability.get_history()


# class TestRefactoredAgentSDK:
#     @pytest.fixture
#     def mock_backend_services(self):
#         """Patch all backend services used by the AgentSDK"""
#         with patch("splore_sdk.sdk.APIClient") as mock_api_client, \
#              patch("splore_sdk.sdk.FileUploader") as mock_file_uploader, \
#              patch("splore_sdk.sdk.ExtractionService") as mock_extraction_service, \
#              patch("splore_sdk.sdk.SearchService") as mock_search_service, \
#              patch("splore_sdk.sdk.ExtractionCapability") as mock_extraction_capability, \
#              patch("splore_sdk.sdk.SearchCapability") as mock_search_capability:

#             # Configure mocks
#             api_client_instance = MagicMock()
#             api_client_instance.validate_api_key.return_value = True
#             mock_api_client.return_value = api_client_instance

#             file_uploader_instance = MagicMock()
#             mock_file_uploader.return_value = file_uploader_instance

#             extraction_service_instance = MagicMock()
#             mock_extraction_service.return_value = extraction_service_instance

#             search_service_instance = MagicMock()
#             mock_search_service.return_value = search_service_instance

#             extraction_capability_instance = MagicMock()
#             extraction_capability_instance.extract.return_value = {"data": "extracted_content"}
#             mock_extraction_capability.return_value = extraction_capability_instance

#             search_capability_instance = MagicMock()
#             search_capability_instance.search.return_value = {"results": [{"title": "Test Result"}]}
#             search_capability_instance.get_history.return_value = {"items": [{"query": "test query"}]}
#             mock_search_capability.return_value = search_capability_instance

#             yield {
#                 "api_client": api_client_instance,
#                 "file_uploader": file_uploader_instance,
#                 "extraction_service": extraction_service_instance,
#                 "search_service": search_service_instance,
#                 "extraction_capability": extraction_capability_instance,
#                 "search_capability": search_capability_instance
#             }

#     @pytest.fixture
#     def agent_sdk(self, mock_backend_services):
#         return AgentSDK(
#             api_key="test_api_key",
#             base_id="test_base_id",
#             agent_id="test_agent_id"
#         )

#     def test_initialization(self, agent_sdk, mock_backend_services):
#         # Test that APIClient and FileUploader were initialized correctly
#         assert hasattr(agent_sdk, "client")
#         assert hasattr(agent_sdk, "file_uploader")

#         # Test that capabilities were initialized correctly
#         assert hasattr(agent_sdk, "_extraction")
#         assert hasattr(agent_sdk, "_search")

#         # Test that backward compatibility service references were set
#         assert hasattr(agent_sdk, "extractions")
#         assert hasattr(agent_sdk, "search")

#     def test_capability_properties(self, agent_sdk, mock_backend_services):
#         # Test extraction property
#         extraction = agent_sdk.extraction
#         assert extraction == mock_backend_services["extraction_capability"]

#         # Test search property
#         search = agent_sdk.search
#         assert search == mock_backend_services["search_capability"]

#     def test_backward_compatibility_methods(self, agent_sdk, mock_backend_services):
#         # Test extract method forwards to capability
#         result = agent_sdk.extract(file_path="test.pdf")
#         mock_backend_services["extraction_capability"].extract.assert_called_once_with(
#             file_path="test.pdf", file_stream=None
#         )
#         assert result == {"data": "extracted_content"}

#         # Test search_query method forwards to capability
#         result = agent_sdk.search_query(query="test query", count=5, engine="google")
#         mock_backend_services["search_capability"].search.assert_called_once_with(
#             query="test query", count=5, engine="google"
#         )
#         assert result["results"][0]["title"] == "Test Result"

#         # Test get_search_history method forwards to capability
#         result = agent_sdk.get_search_history(page=0, size=10)
#         mock_backend_services["search_capability"].get_history.assert_called_once_with(
#             page=0, size=10
#         )
#         assert result["items"][0]["query"] == "test query"
