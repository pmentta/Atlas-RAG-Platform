"""Application settings loaded from environment variables."""

from __future__ import annotations

from dataclasses import dataclass
import os


class SettingsError(Exception):
    """Raised when environment settings are invalid."""


@dataclass(frozen=True)
class AppSettings:
    """Runtime settings for Atlas RAG Platform."""

    app_env: str
    app_name: str
    log_level: str
    log_format: str
    qdrant_url: str
    qdrant_collection_name: str
    embedding_size: int
    gemini_api_key: str
    gemini_generation_model: str
    gemini_embedding_model: str


_ALLOWED_LOG_LEVELS = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
_ALLOWED_LOG_FORMATS = {"json", "text"}


def _read_env(name: str, default: str | None = None) -> str:
    raw_value = os.getenv(name, default)
    if raw_value is None:
        return ""
    return raw_value.strip()


def _read_required_env(name: str, stage: str, remediation: str) -> str:
    value = _read_env(name)
    if value:
        return value
    raise SettingsError(
        f"Missing required environment variable '{name}' in stage '{stage}'. {remediation}"
    )


def load_settings() -> AppSettings:
    """Load settings from environment with explicit validation."""
    app_env = _read_env("APP_ENV", "development") or "development"
    app_name = _read_env("APP_NAME", "atlas-rag-platform") or "atlas-rag-platform"
    log_level = (_read_env("LOG_LEVEL", "INFO") or "INFO").upper()
    log_format = (_read_env("LOG_FORMAT", "json") or "json").lower()

    qdrant_url = _read_required_env(
        name="QDRANT_URL",
        stage="phase-3-vector-store",
        remediation="Set QDRANT_URL (example: http://localhost:6333).",
    )
    qdrant_collection_name = _read_env("QDRANT_COLLECTION_NAME", "atlas_chunks") or "atlas_chunks"
    embedding_size_raw = _read_env("EMBEDDING_SIZE", "768") or "768"

    gemini_api_key = _read_required_env(
        name="GEMINI_API_KEY",
        stage="phase-5-rag-pipeline",
        remediation="Set GEMINI_API_KEY with a valid API key from Google AI Studio.",
    )
    gemini_generation_model = _read_env("GEMINI_GENERATION_MODEL", "gemini-1.5-flash") or "gemini-1.5-flash"
    gemini_embedding_model = _read_env("GEMINI_EMBEDDING_MODEL", "models/text-embedding-004") or "models/text-embedding-004"

    if log_level not in _ALLOWED_LOG_LEVELS:
        raise SettingsError(
            f"Invalid LOG_LEVEL='{log_level}'. Allowed values: {sorted(_ALLOWED_LOG_LEVELS)}"
        )
    if log_format not in _ALLOWED_LOG_FORMATS:
        raise SettingsError(
            f"Invalid LOG_FORMAT='{log_format}'. Allowed values: {sorted(_ALLOWED_LOG_FORMATS)}"
        )

    try:
        embedding_size = int(embedding_size_raw)
    except ValueError as error:
        raise SettingsError(
            f"Invalid EMBEDDING_SIZE='{embedding_size_raw}'. Expected integer greater than zero."
        ) from error
    if embedding_size <= 0:
        raise SettingsError("Invalid EMBEDDING_SIZE. Expected integer greater than zero.")

    return AppSettings(
        app_env=app_env,
        app_name=app_name,
        log_level=log_level,
        log_format=log_format,
        qdrant_url=qdrant_url,
        qdrant_collection_name=qdrant_collection_name,
        embedding_size=embedding_size,
        gemini_api_key=gemini_api_key,
        gemini_generation_model=gemini_generation_model,
        gemini_embedding_model=gemini_embedding_model,
    )
