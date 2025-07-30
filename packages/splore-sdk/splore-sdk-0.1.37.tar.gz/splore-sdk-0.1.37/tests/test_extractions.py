from typing import Optional
from io import StringIO
import pytest
from unittest.mock import MagicMock, patch
from splore_sdk.extractions.extractions_service import ExtractionService
from splore_sdk.extractions.validations import StartExtractionInput
from splore_sdk.core.compat import model_dump_or_dict
from splore_sdk.core.api_client import APIClient


@pytest.fixture
def mock_api_client():
    return MagicMock(spec=APIClient)


@pytest.fixture
def extraction_service(mock_api_client):
    return ExtractionService(api_client=mock_api_client, agent_id="test_agent")


def test_upload_file(extraction_service, mock_api_client):
    mock_api_client.request.return_value = {"fileId": "12345"}
    file_obj = {"file": ("test.pdf", b"dummy content")}
    response = extraction_service.upload_file(file_obj)
    assert response == {"fileId": "12345"}
    mock_api_client.request.assert_called_once_with(
        method="POST", endpoint="api/rest/v2/extractions/files", files=file_obj
    )


def test_start_extraction(extraction_service, mock_api_client):
    mock_api_client.request.return_value = {"status": "started"}
    file_id = "12345"
    response = extraction_service.start(file_id)
    assert response == {"status": "started"}
    payload = model_dump_or_dict(
        StartExtractionInput(agent_id="test_agent", file_id=file_id)
    )
    mock_api_client.request.assert_called_once_with(
        method="POST", endpoint="api/rest/v2/extractions/start", json=payload
    )


def test_processing_status(extraction_service, mock_api_client):
    mock_api_client.request.return_value = {"status": "processing"}
    file_id = "12345"
    response = extraction_service.processing_status(file_id)
    assert response == {"status": "processing"}
    mock_api_client.request.assert_called_once_with(
        method="GET",
        endpoint="api/rest/v2/extractions/status",
        params={"agentId": "test_agent", "fileId": file_id},
    )


def test_extracted_response(extraction_service, mock_api_client):
    mock_api_client.request.return_value = {"data": "extracted content"}
    file_id = "12345"
    response = extraction_service.extracted_response(file_id)
    assert response == {"data": "extracted content"}
    mock_api_client.request.assert_called_once_with(
        method="GET",
        endpoint="api/rest/v2/extractions",
        params={"agentId": "test_agent", "fileId": file_id},
    )


def test_all_extracted_response(extraction_service, mock_api_client):
    mock_api_client.request.return_value = {"items": []}
    response = extraction_service.all_extracted_response()
    assert response == {"items": []}
    mock_api_client.request.assert_called_once_with(
        method="GET",
        endpoint="api/rest/v2/extractions",
        params={"page": 0, "size": 10, "compact": True},
    )
