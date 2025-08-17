from pathlib import Path

import torch

BASE_PATH = Path(__file__).parent

CLIP_IMAGE1_ONNX_PATH = BASE_PATH / 'clip_openai_image_encoder.onnx'
CLIP_TEXT1_ONNX_PATH = BASE_PATH / 'clip_openai_text_encoder.onnx'

CLIP_IMAGE1_ONNX_PATH_FP16 = BASE_PATH / 'clip_openai_image_encoder_fp16.onnx'
CLIP_TEXT1_ONNX_PATH_FP16 = BASE_PATH / 'clip_openai_text_encoder_fp16.onnx'

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"