import logging
import os


def setup_logging():
    try:
        level = getattr(logging, os.environ.get("KEYMAER_LOG_LEVEL", "INFO").upper())
    except AttributeError:
        level = logging.INFO
    logging.basicConfig(encoding="utf-8", level=level)
