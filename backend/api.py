from fastapi import FastAPI
from backend.routers import text_encoding, images_encoding

app = FastAPI(title="Encoding Service API")
app.include_router(text_encoding.router)
app.include_router(images_encoding.router)
