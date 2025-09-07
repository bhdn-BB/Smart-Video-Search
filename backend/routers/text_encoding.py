from fastapi import APIRouter
from backend.dto.query_request import QueryRequest
from backend.dto.query_response import QueryResponse
from backend.services.grpc.client import EncodingClient

router = APIRouter(prefix="/text_encoding", tags=["Text encoding"])
client = EncodingClient()

@router.post("/send_prompt", response_model=QueryResponse)
async def send_prompt(request: QueryRequest):
    response = client.encode_text(request.query)
    return QueryResponse(embedding=list(response.embedding))
