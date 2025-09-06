from torch import nn

from encoding_service.src.models.clip_openai.config import MODEL_CLIP


class CLIPTextEncoder(nn.Module):
    def __init__(self, model=MODEL_CLIP):
        super().__init__()
        self.model = model

    def forward(self, input_ids, attention_mask):
        return self.model.get_text_features(input_ids=input_ids, attention_mask=attention_mask)