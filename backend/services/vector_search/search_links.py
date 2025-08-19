import asyncio
import os
import torch
from torch import cosine_similarity
from backend.global_config import OUTPUT_FRAMES_DIR
from backend.logger import get_logger
from backend.services.video_processing.video_processor import VideoProcessor


class SearchLinks:

    def __init__(self, text_embedd, image_embedd):
        self.text_embedd = text_embedd
        self.image_embedd = image_embedd

    async def get_best_images_by_score_stream(self, k_frames=1):
        relevance_scores = cosine_similarity(self.image_embedd, self.text_embedd)
        top_indices = torch.argsort(relevance_scores, descending=True)[:k_frames]
        for current_dir in OUTPUT_FRAMES_DIR:
            if not current_dir:
                continue
            processor = VideoProcessor(
                output_dir=current_dir,
                logger_object=get_logger(__name__)
            )
            all_frames = await asyncio.to_thread(os.listdir, current_dir)
            for i in top_indices:
                link = await asyncio.to_thread(
                    processor.build_youtube_link_from_filename,
                    all_frames[i]
                )
                yield link