"""Chunk domain entity."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class Chunk:
    """Represents a chunk generated from a source document."""

    id: str
    document_id: str
    content: str
    sequence_number: int
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.id.strip():
            raise ValueError("Chunk.id cannot be empty.")

        if not self.document_id.strip():
            raise ValueError("Chunk.document_id cannot be empty.")

        if not self.content.strip():
            raise ValueError("Chunk.content cannot be empty.")

        if self.sequence_number < 0:
            raise ValueError("Chunk.sequence_number must be non-negative.")

        object.__setattr__(self, "metadata", dict(self.metadata))
