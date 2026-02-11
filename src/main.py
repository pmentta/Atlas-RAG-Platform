"""Entrypoint for Atlas RAG Platform."""

from __future__ import annotations

import logging
import sys

from src.infrastructure.config import SettingsError, load_settings
from src.infrastructure.logging import configure_logging


def main() -> int:
    """Bootstrap application and exit gracefully in Phase 1."""
    try:
        settings = load_settings()
        configure_logging(level=settings.log_level, log_format=settings.log_format)
    except SettingsError as settings_error:
        logging.basicConfig(level=logging.ERROR)
        logging.getLogger("atlas.bootstrap").error(
            "Invalid application settings: %s",
            settings_error,
        )
        return 1

    logger = logging.getLogger("atlas.bootstrap")
    logger.info(
        "Application bootstrap completed",
        extra={"correlation_id": "phase-1-bootstrap"},
    )
    logger.info(
        "Application terminated without runtime services (expected in Phase 1)",
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
