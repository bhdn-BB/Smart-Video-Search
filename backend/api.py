from pathlib import Path

from fastapi import FastAPI, UploadFile, File, BackgroundTasks
from pydantic import BaseModel
from typing import List
import aiohttp
import asyncio

app = FastAPI(title="Encoding Service API")

ENCODING_SERVICE_URL = "http://localhost:8001/encode"  # приклад сервісу енкодингу

# ------------------------------
# 1. Асинхронна передача промпту
# ------------------------------
class PromptRequest(BaseModel):
    prompt: str

@app.post("/send_prompt")
async def send_prompt(request: PromptRequest):
    async with aiohttp.ClientSession() as session:
        async with session.post(ENCODING_SERVICE_URL, json={"prompt": request.prompt}) as resp:
            data = await resp.json()
    return {"status": "ok", "response": data}


# ------------------------------
# 2. Передача списку фотографій
# ------------------------------
@app.post("/send_photos")
async def send_photos(files: List[UploadFile] = File(...)):
    responses = []
    async with aiohttp.ClientSession() as session:
        for file in files:
            content = await file.read()
            async with session.post(
                ENCODING_SERVICE_URL,
                data={"file": content},
                headers={"Content-Type": "application/octet-stream"}
            ) as resp:
                responses.append(await resp.json())
    return {"status": "ok", "results": responses}


# ---------------------------------------------
# 3. Асинхронна передача фото по одному + збір
# ---------------------------------------------
UPLOAD_QUEUE = []

async def send_file_to_encoding(file_bytes: bytes):
    async with aiohttp.ClientSession() as session:
        async with session.post(
            ENCODING_SERVICE_URL,
            data={"file": file_bytes},
            headers={"Content-Type": "application/octet-stream"}
        ) as resp:
            return await resp.json()

@app.post("/send_photo_async")
async def send_photo_async(file: UploadFile = File(...)):
    content = await file.read()
    task = asyncio.create_task(send_file_to_encoding(content))
    UPLOAD_QUEUE.append(task)
    return {"status": "queued", "filename": file.filename}

@app.get("/collect_results")
async def collect_results():
    results = await asyncio.gather(*UPLOAD_QUEUE)
    UPLOAD_QUEUE.clear()
    return {"status": "ok", "results": results}




