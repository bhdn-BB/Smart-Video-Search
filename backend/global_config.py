from pathlib import Path

BASE_DIR = Path(__file__).parent

OUTPUT_FRAMES_DIR = BASE_DIR / 'frames'

TARGET_FORMAT_NOTE = '360p'
MS_IN_SECOND = 1000

QUALITY_INTERVAL_MAP = {
    10: "fps=1/1.0",
    9:  "fps=1/1.5",
    8:  "fps=1/2.0",
    7:  "fps=1/2.5",
    6:  "fps=1/3.0",
    5:  "fps=1/4.0",
    4:  "fps=1/5.0",
    3:  "fps=1/6.0",
    2:  "fps=1/8.0",
    1:  "fps=1/10.0",
}

QUALITY_FRAMES = 31

ENCODING_SERVICE_URL = "http://localhost:8001/encode"

MAX_LENGTH_QUERY = 150
