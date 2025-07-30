from typing import Optional, List, Dict
from pydantic import BaseModel, Field


class CreateAgentInput(BaseModel):
    agentName: str = Field(..., description="provide an agent name as identifier")
    description: Optional[str] = Field(
        ..., description="provide description related to the agent"
    )
    enableWebSearch: Optional[bool] = Field(
        ..., description="want to enable search for agent"
    )


class RetrievalWeights(BaseModel):
    docType: Optional[Dict[str, float]] = Field(
        ..., description="provide the weight configurations"
    )
    recencyDay: Optional[float] = Field(..., description="")


class RankProfileConfig(BaseModel):
    ratio: Optional[float]
    matchFactor: Optional[Dict[str, float]]


class UpdateAgentInput(CreateAgentInput):
    agentName: Optional[str] = Field(
        ..., description="provide an agent name as identifier"
    )
    id: str = Field(..., description="provide the agent id you want to update")
    topk: Optional[int] = Field(
        ...,
        description="specify the number of documents (between 1 and 10) to be considered when generating responses",
    )
    useInternalData: Optional[bool] = Field(..., description="")
    model: Optional[str] = Field(..., description="LLM model for your agent")
    temprature: Optional[float] = Field(
        ...,
        description="This setting controls the creativity and variability of the responses (0-1)",
    )
    responseGeneration: Optional[bool] = Field(
        ..., description="check the documentation"
    )
    inlineCitation: Optional[bool] = Field(..., description="check the documentation")
    retrievalWeights: Optional[RetrievalWeights]
    returnRelatedQuestions: Optional[bool]
    defaultRelatedQuestions: Optional[List[str]]
    numberOfRelatedQuestions: Optional[int]
    rankProfiles: Optional[RankProfileConfig]
