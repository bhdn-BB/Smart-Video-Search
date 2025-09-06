import os
import subprocess
import yt_dlp as youtube_dl
from pydantic import HttpUrl
from backend.global_config import (
    TARGET_FORMAT_NOTE,
    OUTPUT_FRAMES_DIR,
    QUALITY_INTERVAL_MAP,
    QUALITY_FRAMES,
)


class VideoProcessor:

    def __init__(
        self,
        output_dir=OUTPUT_FRAMES_DIR,
    ) -> None:
        self.output_dir = output_dir

    def save_frames_with_ffmpeg(
        self,
        video_url: HttpUrl,
        quality: int,
    ) -> None:
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
                raise ValueError(f'Format "{TARGET_FORMAT_NOTE}" not found.')

            video_stream_url = target_format.get("url")
            os.makedirs(self.output_dir, exist_ok=True)
            output_pattern = os.path.join(self.output_dir, f"frame_%03d_{video_id}.jpg")
            command = [
                "ffmpeg",
                "-i", video_stream_url,
                "-vf", QUALITY_INTERVAL_MAP[quality],
                "-q:v", str(QUALITY_FRAMES),
                output_pattern,
                "-y",
            ]
            subprocess.run(command, check=True)
        except Exception as e:
            raise RuntimeError(f"FFmpeg processing failed: {e}")

    def build_youtube_link_from_filename(
        self,
        filename: str
    ) -> str | None:
        try:
            # Example: "frame_3_n07rvqgxZfg&t=4s.jpeg"
            base = filename.split(".")[0]           # "frame_3_n07rvqgxZfg&t=4s"
            id_and_time = base.split("_", 2)[2]     # "n07rvqgxZfg&t=4s"
            link = f"https://www.youtube.com/watch?v={id_and_time}"
            return link
        except Exception as e:
            raise ValueError(
                f'Failed to build YouTube link from filename "{filename}": {e}'
            )