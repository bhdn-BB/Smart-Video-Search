import os
import cv2
import yt_dlp as youtube_dl
from pydantic import HttpUrl
from backend.global_config import (
    TARGET_FORMAT_NOTE,
    MS_IN_SECOND,
    OUTPUT_FRAMES_DIR,

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

    def save_frames_from_video(
        self,
        video_url: HttpUrl,
        quality: int,
    ) -> None:

        self.logger_object.info(
            f"Start processing video: {video_url},"
            f" interval: {quality}s,"
            f" quality: {TARGET_FORMAT_NOTE}"
        )

        try:

            with youtube_dl.YoutubeDL({}) as ydl:
                video_info = ydl.extract_info(
                    video_url,
                    download=False
                )

            video_id = video_info.get('id', 'unknown')
            formats = video_info.get('formats', None)

            target_format = next(
                (f for f in formats
                 if f.get('format_note') == TARGET_FORMAT_NOTE),
                None
            )

            if not target_format:
                self.logger_object.warning(
                    f'Video format "{TARGET_FORMAT_NOTE}" not found.'
                )
                return None

            video_stream_url = target_format.get('url')

            video_capture = cv2.VideoCapture(video_stream_url)
            total_frames = video_capture.get(cv2.CAP_PROP_FRAME_COUNT)
            fps = int(video_capture.get(cv2.CAP_PROP_FPS))

            duration_ms = total_frames * MS_IN_SECOND / fps

            self.logger_object.info(
                f"Video info: id={video_id},"
                f" duration={duration_ms/1000:.2f}s, fps={fps}"
            )

            current_time_ms = 0
            frame_index = 0

            while (video_capture.isOpened() and
                   current_time_ms < duration_ms):

                video_capture.set(cv2.CAP_PROP_POS_MSEC, current_time_ms)
                read_success, current_frame = video_capture.read()

                if not read_success or not current_frame:
                    self.logger_object.warning(
                        f'Failed to read frame at'
                        f' {current_time_ms / MS_IN_SECOND:.3f}s.'
                    )
                    break

                frame_index += 1
                filename = f"frame_{frame_index}_{video_id}&t={round(current_time_ms / MS_IN_SECOND)}s.jpg"

                cv2.imwrite(self.output_dir, current_frame)
                self.logger_object.info(f'Saved frame: {filename}')
                current_time_ms += quality * MS_IN_SECOND

            video_capture.release()
            self.logger_object.info(
                f'Finished. Total frames saved: {frame_index}'
            )

        except Exception as e:
            self.logger_object.exception(
                f'Exception while processing video: {e}'
            )
        finally:
            self.logger_object.info(
                'Video processing attempt completed.'
            )


    def build_youtube_link_from_filename(
            self,
            filename: str
    ) -> str | None:
        try:
            # Example: "frame_3_n07rvqgxZfg&t=4s.jpeg"
            base = filename.split('.')[0]                # "frame_3_n07rvqgxZfg&t=4s"
            id_and_time = base.split('_', 2)[2]          # "n07rvqgxZfg&t=4s"
            link = f"https://www.youtube.com/watch?v={id_and_time}"
            self.logger_object.info(f'Generated link: {link}')
            return link
        except Exception as e:
            self.logger_object.error(
                f'Failed to build YouTube link from filename "{filename}": {e}'
            )
        finally:
            self.logger_object.debug(f'Attempted to parse filename: {filename}')
