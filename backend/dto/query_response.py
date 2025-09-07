from typing import List
from pydantic import BaseModel, Field


class QueryResponse(BaseModel):
    embedding: List[float] = Field(
        ...,
        description="Text embedding response"
    )