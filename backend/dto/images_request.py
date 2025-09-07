from typing import List
from pydantic import BaseModel, Field


class ImagesRequest(BaseModel):
    images: List[bytes] = Field(
        ...,
        description="Images bytes request",
    )
