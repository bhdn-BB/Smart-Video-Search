from fastapi import APIRouter
import aiohttp
from backend.dto.query_request import QueryRequest
from backend.dto.query_response import QueryResponse
from backend.global_config import ENCODING_SERVICE_URL

router = APIRouter(
    prefix="/text_encoding",
    tags=["Text encoding"]
)

@router.post("/send_prompt", response_model=QueryResponse)
async def send_prompt(request: QueryRequest):
    async with aiohttp.ClientSession() as session:
        async with session.post(
            ENCODING_SERVICE_URL,
            json={"prompt": request.query}
        ) as resp:
            text_embedding = await resp.json()
    return {
        "status": "ok",
        "query_embedding": text_embedding
    }