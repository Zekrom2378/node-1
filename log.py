# Updated log.py
import json
import logging
import sys
from datetime import datetime, timezone


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "msg": record.getMessage(),
            "logger": record.name,
        }
        return json.dumps(payload)


def setup_logger() -> logging.Logger:
    logger = logging.getLogger("node1")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()

    # 1. File Handler - Logs EVERYTHING
    file_handler = logging.FileHandler("robot_debug.log")
    file_handler.setFormatter(JsonFormatter())
    logger.addHandler(file_handler)

    # 2. Console Handler - Still logs, but we will be picky about calling it
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging.Formatter('%(message)s')) # Cleaner console view
    logger.addHandler(console_handler)

    return logger