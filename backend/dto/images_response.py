from typing import List
from pydantic import BaseModel, Field


class ImagesResponse(BaseModel):
    embeddings: List[List[float]] = Field(
        ...,
        description="Images embeddings response",
    )