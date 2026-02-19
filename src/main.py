"""Entrypoint for Atlas RAG Platform."""

from __future__ import annotations

import logging
import sys

from src.infrastructure.config import SettingsError, load_settings
from src.infrastructure.logging import configure_logging
from src.infrastructure.observability import (
    LangSmithObservabilityAdapter,
    LangSmithObservabilityError,
    LangSmithSettings,
)
from src.infrastructure.vector_store import QdrantVectorStore, VectorStoreInfrastructureError
from src.infrastructure.vector_store.qdrant_adapter import QdrantSettings


def main() -> int:
    """Bootstrap application and validate Phase 6 observability wiring."""
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

    try:
        vector_store = QdrantVectorStore.from_url(
            QdrantSettings(
                url=settings.qdrant_url,
                collection_name=settings.qdrant_collection_name,
                embedding_size=settings.embedding_size,
            )
        )
        vector_store.ensure_collection()
    except VectorStoreInfrastructureError as infrastructure_error:
        logger.error(
            "Vector store initialization failed: %s",
            infrastructure_error,
            extra={"correlation_id": "phase-6-bootstrap"},
        )
        return 1

    if settings.langchain_tracing_v2:
        try:
            LangSmithObservabilityAdapter(
                LangSmithSettings(
                    api_key=settings.langchain_api_key,
                    project=settings.langchain_project,
                    endpoint=settings.langchain_endpoint,
                )
            )
        except LangSmithObservabilityError as observability_error:
            logger.error(
                "Observability initialization failed: %s",
                observability_error,
                extra={"correlation_id": "phase-6-bootstrap"},
            )
            return 1

    logger.info(
        "Application bootstrap completed with vector store and observability readiness",
        extra={"correlation_id": "phase-6-bootstrap"},
    )
    logger.info(
        "Application terminated without API runtime services (expected in current phase)",
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
