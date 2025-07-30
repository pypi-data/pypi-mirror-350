from pydantic import BaseModel, Field
from typing import Optional


class SearchQueryInput(BaseModel):
    """Input model for search query"""

    query: str = Field(..., description="Search query string")
    agent_id: str = Field(..., description="ID of the agent to use for search")
    count: Optional[int] = Field(10, description="Number of search results to return")
    engine: Optional[str] = Field("google", description="Search engine to use")
