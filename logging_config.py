"""Structured JSON logging configuration."""

import logging
import uuid

from pythonjsonlogger import jsonlogger


def generate_request_id() -> str:
    return uuid.uuid4().hex[:12]


def setup_logging(level: str = "INFO") -> None:
    handler = logging.StreamHandler()
    formatter = jsonlogger.JsonFormatter(
        fmt="%(asctime)s %(levelname)s %(name)s %(message)s",
        rename_fields={"asctime": "timestamp", "levelname": "level"},
    )
    handler.setFormatter(formatter)

    root = logging.getLogger()
    root.handlers.clear()
    root.addHandler(handler)
    root.setLevel(getattr(logging, level.upper(), logging.INFO))
