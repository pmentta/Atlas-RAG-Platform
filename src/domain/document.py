"""Document domain entity."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass(frozen=True)
class Document:
    """Represents a source document in the knowledge base."""

    id: str
    source_path: str
    created_at: datetime
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.id.strip():
            raise ValueError("Document.id cannot be empty.")

        if not self.source_path.strip():
            raise ValueError("Document.source_path cannot be empty.")

        if self.created_at.tzinfo is None:
            raise ValueError("Document.created_at must be timezone-aware.")

        object.__setattr__(self, "metadata", dict(self.metadata))

    @classmethod
    def create(cls, id: str, source_path: str, metadata: dict[str, Any] | None = None) -> "Document":
        """Factory helper with UTC timestamp."""
        return cls(
            id=id,
            source_path=source_path,
            created_at=datetime.now(timezone.utc),
            metadata=metadata or {},
        )
