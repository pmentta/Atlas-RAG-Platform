"""Answer domain entity."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass(frozen=True)
class Answer:
    """Represents an answer grounded on retrieved context."""

    text: str
    source_chunk_ids: list[str]
    created_at: datetime
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.text.strip():
            raise ValueError("Answer.text cannot be empty.")

        if self.created_at.tzinfo is None:
            raise ValueError("Answer.created_at must be timezone-aware.")

        normalized_sources = [chunk_id.strip() for chunk_id in self.source_chunk_ids if chunk_id.strip()]
        if not normalized_sources:
            raise ValueError("Answer.source_chunk_ids cannot be empty.")

        object.__setattr__(self, "source_chunk_ids", normalized_sources)
        object.__setattr__(self, "metadata", dict(self.metadata))

    @classmethod
    def create(
        cls,
        text: str,
        source_chunk_ids: list[str],
        metadata: dict[str, Any] | None = None,
    ) -> "Answer":
        """Factory helper with UTC timestamp."""
        return cls(
            text=text,
            source_chunk_ids=source_chunk_ids,
            created_at=datetime.now(timezone.utc),
            metadata=metadata or {},
        )
