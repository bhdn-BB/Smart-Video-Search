from pydantic import BaseModel, Field
from backend.global_config import MAX_LENGTH_QUERY


class QueryRequest(BaseModel):
    query: str = Field(..., max_length=MAX_LENGTH_QUERY)