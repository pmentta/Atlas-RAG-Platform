"""Application ports shared across use cases."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class VectorSearchResult:
    """Result item returned by vector similarity search."""

    chunk_id: str
    score: float
    payload: dict[str, object]


class VectorStorePort(ABC):
    """Port for vector-store operations used by the application layer."""

    @abstractmethod
    def ensure_collection(self) -> None:
        """Create or validate the target collection in the vector database."""

    @abstractmethod
    def upsert_embedding(
        self,
        chunk_id: str,
        embedding: list[float],
        payload: dict[str, object],
    ) -> None:
        """Insert or update one embedding record."""

    @abstractmethod
    def search_similar(
        self,
        query_embedding: list[float],
        limit: int,
        score_threshold: float | None = None,
    ) -> list[VectorSearchResult]:
        """Search for nearest neighbors by vector similarity."""
