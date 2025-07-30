from pydantic import BaseModel, Field


class StartExtractionInput(BaseModel):
    agent_id: str = Field(..., description="add specific agent id related to your base")
    file_id: str = Field(..., description="provide the id of the file")
