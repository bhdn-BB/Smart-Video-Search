from pydantic import BaseModel


class QueryResponse(BaseModel):
    embedding: list