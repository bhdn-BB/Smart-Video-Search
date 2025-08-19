from pathlib import Path

BASE_DIR = Path(__file__).parent

OUTPUT_FRAMES_DIR = BASE_DIR / 'frames'

TARGET_FORMAT_NOTE = '360p'
MS_IN_SECOND = 1000

QUALITY_INTERVAL_MAP = {
    10: 1.0,
    9: 1.5,
    8: 2.0,
    7: 2.5,
    6: 3.0,
    5: 4.0,
    4: 5.0,
    3: 6.0,
    2: 8.0,
    1: 10.0,
}

QUALITY_FRAMES = 15
