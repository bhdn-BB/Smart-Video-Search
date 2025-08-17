from fastapi import FastAPI, File, UploadFile, Query, HTTPException
import base64
from triton.inference_module import InferenceModule
from encoding_service.src.models.clip_openai.config import MODEL_CLIP

app = FastAPI()
inference_module = InferenceModule()

@app.post("/encoding/image", description="Image encoding")
async def predict_image(file: UploadFile = File(..., description="Image input")):
    try:
        contents = await file.read()
        img_base64 = base64.b64encode(contents).decode("utf-8")
        features = await inference_module.infer_image(img_base64, model_name=MODEL_CLIP)
        return {"features": features.tolist()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@app.post("/encoding/text", description="Text encoding")
async def predict_text(text: str = Query(..., description="Text input")):
    try:
        features = await inference_module.infer_text(text=text, model_name=MODEL_CLIP)
        return {"features": features.tolist()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")