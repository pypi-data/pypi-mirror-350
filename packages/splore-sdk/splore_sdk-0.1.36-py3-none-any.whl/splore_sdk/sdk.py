from abc import ABC
from typing import IO, Optional, Dict
from splore_sdk.core.api_client import APIClient
from splore_sdk.core.logger import sdk_logger, with_logging_context
from splore_sdk.extractions.extractions_service import ExtractionService
from splore_sdk.search.search_service import SearchService
from splore_sdk.agents.agents_service import AgentService
from splore_sdk.utils.file_uploader import FileUploader
from splore_sdk.utils.decorators import poll_with_timeout


class BaseSDK:
    @with_logging_context(new_context=True)
    def __init__(
        self,
        api_key: str,
        base_id: str,
        user_id: Optional[str] = None,
        agent_id: Optional[str] = None,
    ):
        self.logger = sdk_logger

        if not api_key:
            raise ValueError("API Key is required to initialize SDK.")
        self.base_id = base_id
        self.api_key = api_key
        self.user_id = user_id
        self.agent_id = agent_id
        self.client = APIClient(
            api_key=self.api_key, base_id=base_id, agent_id=agent_id
        )
        self.file_uploader = FileUploader(
            api_key=self.api_key, base_id=self.base_id, user_id=self.user_id
        )
        self.validate_api_key()
        self.logger.info(
            f"SDK initialized with base_id: {self.base_id} and agent_id: {self.agent_id}"
        )

    @with_logging_context()
    def validate_api_key(self):
        try:
            self.client.validate_api_key()
        except Exception as e:
            self.logger.debug(f"API Key validation failed: {e}")
            raise ValueError("API Key validation failed")


class SploreSDK(BaseSDK):
    def __init__(self, api_key: str, base_id: str, user_id: Optional[str] = None):
        super().__init__(api_key, base_id, user_id)
        self.agents = AgentService(self.client)

    def get_agents(
        self, agentId: Optional[str] = None, agentName: Optional[str] = None
    ):
        """Fetch the list of agents related to the base."""
        return self.agents.get_agents(agentId=agentId, agentName=agentName)

    @with_logging_context()
    def init_agent(self, agent_id: str) -> "AgentSDK":
        """
        Initialize and return an agent-specific instance.

        Args:
            agent_id (str): The ID of the agent to initialize.

        Returns:
            AgentSDK: An instance of AgentSDK specific to the given agent ID.
        """
        if not agent_id:
            raise ValueError("Agent ID is required to initialize an agent.")
        self.logger.info(f"Initializing agent with ID: {agent_id}")
        return AgentSDK(api_key=self.api_key, base_id=self.base_id, agent_id=agent_id)


# Agent capabilities as separate modules
class AgentCapability(ABC):
    """Base class for all agent capabilities like extraction, search, chat, etc."""

    def __init__(self, client: APIClient, agent_id: str, logger=None):
        self.client = client
        self.agent_id = agent_id
        self.logger = logger or sdk_logger


class ExtractionCapability(AgentCapability):
    """Extraction capability for agents"""

    def __init__(
        self, client: APIClient, agent_id: str, file_uploader: FileUploader, logger=None
    ):
        super().__init__(client, agent_id, logger)
        self.service = ExtractionService(client, agent_id=agent_id)
        self.file_uploader = file_uploader

    @with_logging_context(new_context=True)
    def extract(
        self,
        file_path: Optional[str] = None,
        file_stream: Optional[IO] = None,
        max_poll_timeout: Optional[float] = 1200,  # 20 minutes
    ) -> Dict:
        """
        Run the extraction pipeline for the agent by uploading a file.

        Args:
            file_path (Optional[str], optional): Local file path.
            file_stream (Optional[IO], optional): File object/blob.

        Raises:
            ValueError: If neither file_path nor file_stream is provided.

        Returns:
            Dict: Extracted response data from the file.
        """
        if not (file_path or file_stream):
            raise ValueError("One of file_path or file_stream must be provided.")
        if not self.agent_id:
            raise ValueError("Agent ID is required for extraction flow.")

        # Creating a new context for this extraction operation
        # The decorator already generated a new UUID, so no need to call generate_new_uuid() explicitly
        self.logger.info(f"Starting extraction task for file: {file_path or 'stream'}")

        self.service.set_agent(agent_id=self.agent_id)
        self.logger.info(
            f"Starting file upload for agent {self.agent_id}, file: {file_path}"
        )
        upload_res = self.file_uploader.upload_file(
            file_path=file_path, file_stream=file_stream
        )
        self.logger.info(f"File upload completed with file_id: {upload_res}")

        # Define the polling function for indexing status
        @poll_with_timeout(
            condition=lambda resp: resp.get("fileProcessingStatus") == "INDEXED",
            max_timeout=max_poll_timeout,
            min_poll_interval=30,
            max_poll_interval=300,
        )
        def check_indexing_status():
            resp = self.service.processing_status(file_id=upload_res)
            if resp.get("fileProcessingStatus") != "INDEXED":
                self.logger.info("File indexing not completed, waiting...")
            return resp

        # Wait for indexing to complete with timeout
        check_indexing_status()

        extraction_resp = self.service.start(file_id=upload_res)
        if extraction_resp is None:
            raise Exception("Extraction Failed")
        extraction_id = extraction_resp.get("extractionId", None)
        self.logger.info(f"File extraction started with extractionId: {extraction_id}")

        # Define the polling function for extraction status
        @poll_with_timeout(
            condition=lambda resp: resp.get("file", {}).get("status") == "COMPLETED",
            max_timeout=max_poll_timeout,
            min_poll_interval=30,
            max_poll_interval=300,
        )
        def check_and_get_extracted_response():
            resp = self.service.extracted_response_by_extraction_id(
                extraction_id=extraction_id
            )
            if resp.get("file", {}).get("status") != "COMPLETED":
                self.logger.info(
                    f"File extraction not completed, status: {resp.get('file', {}).get('status')}, waiting..."
                )
            return resp

        # Wait for extraction to complete with timeout
        extracted_resp = check_and_get_extracted_response()
        self.logger.info("File extraction completed")
        return extracted_resp

    @with_logging_context(new_context=True)
    def retry_extraction(
        self, extraction_id: str, max_poll_timeout: Optional[float] = 1200
    ):
        # The decorator already generated a new UUID, so no need to call generate_new_uuid() explicitly
        self.logger.info(
            f"Starting extraction retry task for extraction ID: {extraction_id}"
        )

        extraction_resp = self.service.start_extraction_by_extraction_id(
            extraction_id=extraction_id
        )
        if extraction_resp is None:
            raise Exception("Extraction Failed")
        version = extraction_resp.get("version", 1)

        # Define the polling function for extraction status
        @poll_with_timeout(
            condition=lambda resp: resp.get("file", {}).get("status") == "COMPLETED",
            max_timeout=max_poll_timeout,
            min_poll_interval=30,
            max_poll_interval=300,
        )
        def check_and_get_extracted_response():
            resp = self.service.extracted_response_by_extraction_id(
                extraction_id=extraction_id, version=version
            )
            if resp.get("file", {}).get("status") != "COMPLETED":
                self.logger.info(
                    f"File extraction not completed, status: {resp.get('file', {}).get('status')}, waiting..."
                )
            return resp

        # Wait for extraction to complete with timeout
        extracted_resp = check_and_get_extracted_response()
        self.logger.info("File extraction completed")
        return extracted_resp


class SearchCapability(AgentCapability):
    """Search capability for agents"""

    def __init__(self, client: APIClient, agent_id: str, logger=None):
        super().__init__(client, agent_id, logger)
        self.service = SearchService(client, agent_id=agent_id)

    def search(
        self, query: str, count: Optional[int] = 10, engine: Optional[str] = "google"
    ) -> Dict:
        """
        Perform a search query using the specified parameters.

        Args:
            query (str): The search query string.
            count (Optional[int], optional): Number of results to return. Defaults to 10.
            engine (Optional[str], optional): Search engine to use. Defaults to "google".

        Returns:
            Dict: The search results from the API.
        """
        if not self.agent_id:
            raise ValueError("Agent ID is required for search query.")

        self.service.set_agent(agent_id=self.agent_id)
        self.logger.info(
            f"Starting search query for agent {self.agent_id}, query: {query}"
        )

        search_results = self.service.search(query=query, count=count, engine=engine)
        self.logger.info("Search query completed")
        return search_results

    def get_history(self, page: Optional[int] = 0, size: Optional[int] = 10) -> Dict:
        """
        Get search history for the current agent.

        Args:
            page (Optional[int], optional): Page number for pagination. Defaults to 0.
            size (Optional[int], optional): Number of results per page. Defaults to 10.

        Returns:
            Dict: The search history from the API.
        """
        if not self.agent_id:
            raise ValueError("Agent ID is required for search history.")

        self.service.set_agent(agent_id=self.agent_id)
        self.logger.info(f"Getting search history for agent {self.agent_id}")

        history = self.service.get_search_history(page=page, size=size)
        self.logger.info("Search history retrieved")
        return history


# Main Agent SDK with capabilities
class AgentSDK(BaseSDK):
    def __init__(self, api_key: str, base_id: str, agent_id: str):
        super().__init__(api_key, base_id, agent_id=agent_id)

        # Initialize capabilities
        self._extraction = ExtractionCapability(
            self.client, agent_id, self.file_uploader, self.logger
        )
        self._search = SearchCapability(self.client, agent_id, self.logger)

        # For backward compatibility
        self.extractions = ExtractionService(self.client, agent_id=agent_id)
        self._search_service = SearchService(self.client, agent_id=agent_id)

    @property
    def extraction(self) -> ExtractionCapability:
        """Access to extraction capabilities"""
        return self._extraction

    @property
    def search(self) -> SearchCapability:
        """Access to search capabilities"""
        return self._search

    @property
    def search_service(self) -> SearchService:
        """Backward compatibility access to search service"""
        return self._search_service

    # Backward compatibility methods
    def extract(
        self,
        file_path: Optional[str] = None,
        file_stream: Optional[IO] = None,
        max_poll_timeout: Optional[float] = 1200,
    ) -> Dict:
        """Backward compatibility method for extraction"""
        if file_path is None and file_stream is None:
            raise ValueError("One of file_path or file_stream must be provided.")
        return self.extraction.extract(
            file_path=file_path,
            file_stream=file_stream,
            max_poll_timeout=max_poll_timeout,
        )

    def search_query(
        self, query: str, count: Optional[int] = 10, engine: Optional[str] = "google"
    ) -> Dict:
        """Backward compatibility method for search"""
        if self.agent_id is None:
            raise ValueError("Agent ID is required for search query.")
        return self.search.search(query=query, count=count, engine=engine)

    def get_search_history(
        self, page: Optional[int] = 0, size: Optional[int] = 10
    ) -> Dict:
        """Backward compatibility method for search history"""
        if self.agent_id is None:
            raise ValueError("Agent ID is required for search history.")
        return self.search.get_history(page=page, size=size)
