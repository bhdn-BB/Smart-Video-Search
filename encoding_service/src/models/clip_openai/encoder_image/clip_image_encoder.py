from torch import nn

from encoding_service.src.models.clip_openai.config import MODEL_CLIP


class CLIPImageEncoder(nn.Module):
    def __init__(self, model=MODEL_CLIP):
        super().__init__()
        self.model = model

    def forward(self, pixel_values):
        return self.model.get_image_features(pixel_values=pixel_values)