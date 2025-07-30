from typing import Optional
from .validations import StartExtractionInput
from splore_sdk.core.api_client import APIClient
from splore_sdk.core.compat import model_dump_or_dict


class ExtractionService:
    def __init__(self, api_client: APIClient, agent_id: str):
        self.api_client = api_client
        self.extraction_prefix = "api/rest/v2/extractions"
        self.api_client.agent_id = agent_id

    def set_agent(self, agent_id):
        self.api_client.agent_id = agent_id

    def endpoint(self, endpoint):
        return self.extraction_prefix + endpoint

    def upload_file(self, fileObj):
        return self.api_client.request(
            method="POST", endpoint=self.endpoint("/files"), files=fileObj
        )

    def start(self, file_id: str):
        if self.api_client.agent_id is None:
            raise ValueError(
                "for extraction agent_id is required, intialise the sdk with agent_id or call function `extractions.set_agent(agent_id)`"
            )

        payload = StartExtractionInput(
            agent_id=self.api_client.agent_id,
            file_id=file_id,
        )
        return self.api_client.request(
            method="POST",
            endpoint=self.endpoint("/start"),
            json=model_dump_or_dict(payload),
        )

    def processing_status(self, file_id: str):
        if self.api_client.agent_id is None:
            raise ValueError(
                "for extraction agent_id is required, intialise the sdk with agent_id or call function `extractions.set_agent(agent_id)`"
            )

        params = {"agentId": self.api_client.agent_id, "fileId": file_id}
        return self.api_client.request(
            method="GET", endpoint=self.endpoint("/status"), params=params
        )

    def extracted_response(self, file_id: str):
        if self.api_client.agent_id is None:
            raise ValueError(
                "for extraction agent_id is required, intialise the sdk with agent_id or call function `extractions.set_agent(agent_id)`"
            )

        params = {"agentId": self.api_client.agent_id, "fileId": file_id}
        return self.api_client.request(
            method="GET", endpoint=self.endpoint(""), params=params
        )

    def all_extracted_response(
        self,
        page: Optional[int] = 0,
        size: Optional[int] = 10,
        compact: Optional[bool] = True,
    ):
        params = {"page": page, "size": size, "compact": compact}
        return self.api_client.request(
            method="GET", endpoint=self.endpoint(""), params=params
        )

    def extracted_response_by_extraction_id(
        self, extraction_id: str, version: Optional[int] = 1
    ):
        params = {"version": version}
        return self.api_client.request(
            method="GET", endpoint=self.endpoint(f"/{extraction_id}"), params=params
        )

    def start_extraction_by_extraction_id(self, extraction_id: str):
        return self.api_client.request(
            method="POST", endpoint=self.endpoint(f"/{extraction_id}"), json={}
        )
