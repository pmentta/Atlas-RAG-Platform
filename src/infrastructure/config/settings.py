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


_ALLOWED_LOG_LEVELS = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
_ALLOWED_LOG_FORMATS = {"json", "text"}


def _read_env(name: str, default: str) -> str:
    value = os.getenv(name, default).strip()
    return value or default


def load_settings() -> AppSettings:
    """Load settings from environment with explicit validation."""
    app_env = _read_env("APP_ENV", "development")
    app_name = _read_env("APP_NAME", "atlas-rag-platform")
    log_level = _read_env("LOG_LEVEL", "INFO").upper()
    log_format = _read_env("LOG_FORMAT", "json").lower()

    if log_level not in _ALLOWED_LOG_LEVELS:
        raise SettingsError(
            f"Invalid LOG_LEVEL='{log_level}'. Allowed values: {sorted(_ALLOWED_LOG_LEVELS)}"
        )

    if log_format not in _ALLOWED_LOG_FORMATS:
        raise SettingsError(
            f"Invalid LOG_FORMAT='{log_format}'. Allowed values: {sorted(_ALLOWED_LOG_FORMATS)}"
        )

    return AppSettings(
        app_env=app_env,
        app_name=app_name,
        log_level=log_level,
        log_format=log_format,
    )
