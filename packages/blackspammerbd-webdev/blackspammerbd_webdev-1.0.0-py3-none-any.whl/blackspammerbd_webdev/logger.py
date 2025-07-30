import os
import logging
import json
from datetime import datetime

def setup_logger(name: str) -> logging.Logger:
    """
    Configure a logger that writes:
      - DEBUG logs to a timestamped JSON file under logs/
      - INFO+ logs to console with colorized formatting
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Ensure logs/ directory exists
    if not os.path.isdir("logs"):
        os.makedirs("logs")

    # File handler (DEBUG, JSON)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = f"logs/{name}_{timestamp}.json"
    fh = logging.FileHandler(log_filename, encoding="utf-8")
    fh.setLevel(logging.DEBUG)

    # Custom JSON formatter for file logs
    class JsonFormatter(logging.Formatter):
        def format(self, record):
            log_record = {
                "timestamp": datetime.fromtimestamp(record.created).isoformat(),
                "level": record.levelname,
                "message": record.getMessage(),
                "module": record.module,
                "funcName": record.funcName,
                "lineNo": record.lineno
            }
            return json.dumps(log_record)

    fh.setFormatter(JsonFormatter())

    # Console handler (INFO, human-readable)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    console_fmt = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    ch.setFormatter(console_fmt)

    # Attach handlers if not already attached
    if not logger.handlers:
        logger.addHandler(fh)
        logger.addHandler(ch)

    return logger

logger = setup_logger("BSBWebDev")
