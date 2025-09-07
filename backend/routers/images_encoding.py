from fastapi import APIRouter, UploadFile, File
from typing import List
from backend.services.grpc.client import EncodingClient

router = APIRouter(prefix="/images_encoding", tags=["Images encoding"])
client = EncodingClient()

@router.post("/send_photos")
async def send_photos(files: List[UploadFile] = File(...)):
    images = [await f.read() for f in files]
    response = client.encode_images(images)
    return {"status": "ok", "results": [list(e.embedding) for e in response.embeddings]}
