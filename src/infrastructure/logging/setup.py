"""Structured logging configuration."""

from __future__ import annotations

from datetime import datetime, timezone
import json
import logging


class JsonFormatter(logging.Formatter):
    """Minimal JSON formatter for structured logs."""

    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        correlation_id = getattr(record, "correlation_id", None)
        if correlation_id:
            payload["correlation_id"] = correlation_id

        return json.dumps(payload, ensure_ascii=False)


def configure_logging(level: str, log_format: str = "json") -> None:
    """Configure root logger once for the process."""
    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    root_logger.setLevel(level)

    stream_handler = logging.StreamHandler()

    if log_format == "json":
        stream_handler.setFormatter(JsonFormatter())
    else:
        stream_handler.setFormatter(
            logging.Formatter(
                fmt="%(asctime)s %(levelname)s %(name)s - %(message)s",
            )
        )

    root_logger.addHandler(stream_handler)
