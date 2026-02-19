"""Query domain entity."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass(frozen=True)
class Query:
    """Represents a user question sent to the RAG pipeline."""

    text: str
    created_at: datetime
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.text.strip():
            raise ValueError("Query.text cannot be empty.")

        if self.created_at.tzinfo is None:
            raise ValueError("Query.created_at must be timezone-aware.")

        object.__setattr__(self, "metadata", dict(self.metadata))

    @classmethod
    def create(cls, text: str, metadata: dict[str, Any] | None = None) -> "Query":
        """Factory helper with UTC timestamp."""
        return cls(text=text, created_at=datetime.now(timezone.utc), metadata=metadata or {})
