import logging
from pythonjsonlogger import jsonlogger

def get_logger(
        name: str = __name__,
        log_file: str = "log.json"
) -> logging.Logger:
    logger = logging.getLogger(name)
    file_handler = logging.FileHandler(log_file, mode="w")
    formatter = jsonlogger.JsonFormatter(
        '%(asctime)s %(levelname)s %(message)s'
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger