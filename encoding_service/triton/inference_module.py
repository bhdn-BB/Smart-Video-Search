import os
import numpy as np
import grpc
import base64
from io import BytesIO
from PIL import Image
from transformers import CLIPProcessor
import tritonclient.grpc.aio as grpcclient
from tritonclient.grpc import service_pb2, service_pb2_grpc
from tritonclient.utils import triton_to_np_dtype
from encoding_service.src.models.clip_openai.config import MODEL_CLIP


class InferenceModule:

    def __init__(self, model_clip=MODEL_CLIP) -> None:
        self.url = os.environ.get("TRITON_SERVER_URL", "127.0.0.1:8001")
        self.triton_client = grpcclient.InferenceServerClient(url=self.url)
        self.processor = CLIPProcessor.from_pretrained(model_clip)

    async def infer_image(
            self,
            img: str,
            model_name: str = "encoder_image"
    ) -> np.ndarray:

        model_meta, _ = self.get_metadata(model_name)
        dtype = model_meta.inputs[0].datatype
        pil_img = self.decode_image(img)
        inputs = self.processor(images=pil_img, return_tensors="pt")
        pixel_values = inputs["pixel_values"].numpy()

        infer_inputs = [
            grpcclient.InferInput(model_meta.inputs[0].name, pixel_values.shape, dtype)
        ]
        infer_inputs[0].set_data_from_numpy(pixel_values.astype(triton_to_np_dtype(dtype)))

        outputs = [grpcclient.InferRequestedOutput(model_meta.outputs[0].name)]

        results = await self.triton_client.infer(
            model_name=model_name,
            inputs=infer_inputs,
            outputs=outputs,
        )
        return results.as_numpy(model_meta.outputs[0].name)

    async def infer_text(
            self,
            text: str,
            model_name: str = "encoder_text"
    ) -> np.ndarray:
        model_meta, _ = self.get_metadata(model_name)
        dtype_ids = model_meta.inputs[0].datatype
        dtype_mask = model_meta.inputs[1].datatype
        inputs = self.processor(text=[text], return_tensors="pt", padding=True)
        input_ids = inputs["input_ids"].numpy()
        attention_mask = inputs["attention_mask"].numpy()
        infer_inputs = []
        infer_inputs.append(
            grpcclient.InferInput(
                model_meta.inputs[0].name, input_ids.shape, dtype_ids)
        )
        infer_inputs[-1].set_data_from_numpy(
            input_ids.astype(triton_to_np_dtype(dtype_ids))
        )
        infer_inputs.append(
            grpcclient.InferInput(model_meta.inputs[1].name, attention_mask.shape, dtype_mask)
        )
        infer_inputs[-1].set_data_from_numpy(
            attention_mask.astype(triton_to_np_dtype(dtype_mask))
        )
        outputs = [grpcclient.InferRequestedOutput(model_meta.outputs[0].name)]
        results = await self.triton_client.infer(
            model_name=model_name,
            inputs=infer_inputs,
            outputs=outputs,
        )
        return results.as_numpy(model_meta.outputs[0].name)

    def decode_image(self, image_base64: str) -> Image.Image:
        if image_base64.startswith("data:image/"):
            _, encoded = image_base64.split(",", 1)
        else:
            encoded = image_base64
        img_bytes = base64.b64decode(encoded)
        img_buffer = BytesIO(img_bytes)
        return Image.open(img_buffer).convert("RGB")

    def get_metadata(self, model_name: str) -> object:
        channel = grpc.insecure_channel(self.url)
        grpc_stub = service_pb2_grpc.GRPCInferenceServiceStub(channel)
        metadata_request = service_pb2.ModelMetadataRequest(name=model_name)
        metadata_response = grpc_stub.ModelMetadata(metadata_request)
        config_request = service_pb2.ModelConfigRequest(name=model_name)
        config_response = grpc_stub.ModelConfig(config_request)
        return metadata_response, config_response