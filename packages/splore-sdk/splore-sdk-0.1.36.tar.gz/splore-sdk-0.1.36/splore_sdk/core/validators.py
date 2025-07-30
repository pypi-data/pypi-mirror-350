from pydantic import BaseModel, Field
from typing import Optional


class FilePathInput(BaseModel):
    file_path: str = Field(..., description="Local file path, S3 URI, or public URL")
    template_id: str = Field(..., description="Template ID for the extraction")
    agent_id: Optional[str] = Field(None, description="Optional Agent ID")
    base_id: str = Field(..., description="Base ID for the extraction")


class APIClientInput(BaseModel):
    api_key: str = Field(..., description="api_key generated from splore console")
    base_url: str = Field(..., description="base api url for splore app")
