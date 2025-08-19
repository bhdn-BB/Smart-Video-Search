import os
import cv2
import subprocess
import yt_dlp as youtube_dl
from pydantic import HttpUrl
from backend.global_config import (
    TARGET_FORMAT_NOTE,
    MS_IN_SECOND,
    OUTPUT_FRAMES_DIR,
    QUALITY_INTERVAL_MAP,
    QUALITY_FRAMES,

)
from backend.logger import get_logger


class VideoProcessor:

    def __init__(
        self,
        output_dir=OUTPUT_FRAMES_DIR,
        logger_object=get_logger(__name__)
    ) -> None:
        self.output_dir = output_dir
        self.logger_object = logger_object

    def save_frames_with_ffmpeg(
        self,
        video_url: HttpUrl,
        quality: int,
    ) -> None:

        self.logger_object.info(
            f"Start FFmpeg processing: {video_url}, step={quality}s"
        )

        try:
            with youtube_dl.YoutubeDL({}) as ydl:
                video_info = ydl.extract_info(video_url, download=False)

            video_id = video_info.get("id", "unknown")
            formats = video_info.get("formats", [])
            target_format = next(
                (f for f in formats if f.get("format_note") == TARGET_FORMAT_NOTE),
                None
            )
            if not target_format:
                self.logger_object.warning(f'Format "{TARGET_FORMAT_NOTE}" not found.')
                return None

            video_stream_url = target_format.get("url")
            os.makedirs(self.output_dir, exist_ok=True)
            output_pattern = os.path.join(self.output_dir, f"frame_%03d_{video_id}.jpg")
            item_interval = QUALITY_INTERVAL_MAP.get(quality)

            command = [
                "ffmpeg",
                "-i", video_stream_url,
                "-vf", item_interval,
                "-q:v", QUALITY_FRAMES,
                output_pattern,
                "-y"
            ]
            subprocess.run(command, check=True)
            self.logger_object.info(f"Frames saved to {output_pattern}")
        except Exception as e:
            self.logger_object.exception(f"FFmpeg error: {e}")
        finally:
            self.logger_object.info("FFmpeg processing attempt completed.")

    def build_youtube_link_from_filename(
        self,
        filename: str
    ) -> str | None:
        try:
            # Example: "frame_3_n07rvqgxZfg&t=4s.jpeg"
            base = filename.split(".")[0]           # "frame_3_n07rvqgxZfg&t=4s"
            id_and_time = base.split("_", 2)[2]     # "n07rvqgxZfg&t=4s"
            link = f"https://www.youtube.com/watch?v={id_and_time}"
            self.logger_object.info(f"Generated link: {link}")
            return link
        except Exception as e:
            self.logger_object.error(
                f'Failed to build YouTube link from filename "{filename}": {e}'
            )
        finally:
            self.logger_object.debug(f"Attempted to parse filename: {filename}")
