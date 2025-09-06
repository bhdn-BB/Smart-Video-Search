from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    query: str = Field(..., max_length=150)