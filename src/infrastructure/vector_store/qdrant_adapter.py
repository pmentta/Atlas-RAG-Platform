"""Qdrant adapter implementing the vector-store port."""

from __future__ import annotations

from dataclasses import dataclass

from src.application import VectorSearchResult, VectorStorePort

try:
    from qdrant_client import QdrantClient
    from qdrant_client.http import models as qdrant_models
except ImportError:  # pragma: no cover - covered by runtime guard
    QdrantClient = None
    qdrant_models = None


class VectorStoreInfrastructureError(Exception):
    """Raised when vector-store operations fail in infrastructure."""


@dataclass(frozen=True)
class QdrantSettings:
    """Qdrant-specific runtime settings."""

    url: str
    collection_name: str
    embedding_size: int


class QdrantVectorStore(VectorStorePort):
    """Qdrant implementation of vector store operations."""

    def __init__(self, settings: QdrantSettings, client: object) -> None:
        self._settings = settings
        self._client = client

    @classmethod
    def from_url(cls, settings: QdrantSettings) -> "QdrantVectorStore":
        """Build adapter from URL using qdrant-client."""
        if QdrantClient is None:
            raise VectorStoreInfrastructureError(
                "qdrant-client is not installed. Install project dependencies before running Phase 3."
            )
        client = QdrantClient(url=settings.url)
        return cls(settings=settings, client=client)

    def ensure_collection(self) -> None:
        """Create collection if absent, otherwise keep existing collection."""
        try:
            if self._client.collection_exists(collection_name=self._settings.collection_name):
                return

            self._client.create_collection(
                collection_name=self._settings.collection_name,
                vectors_config=qdrant_models.VectorParams(
                    size=self._settings.embedding_size,
                    distance=qdrant_models.Distance.COSINE,
                ),
            )
        except Exception as error:  # noqa: BLE001
            raise VectorStoreInfrastructureError(
                f"Failed to ensure Qdrant collection '{self._settings.collection_name}'."
            ) from error

    def upsert_embedding(
        self,
        chunk_id: str,
        embedding: list[float],
        payload: dict[str, object],
    ) -> None:
        """Upsert one embedding record into Qdrant."""
        if not chunk_id.strip():
            raise VectorStoreInfrastructureError("chunk_id cannot be empty.")

        if len(embedding) != self._settings.embedding_size:
            raise VectorStoreInfrastructureError(
                "Embedding size mismatch. "
                f"Expected {self._settings.embedding_size}, got {len(embedding)}."
            )

        try:
            self._client.upsert(
                collection_name=self._settings.collection_name,
                points=[
                    qdrant_models.PointStruct(
                        id=chunk_id,
                        vector=embedding,
                        payload=payload,
                    )
                ],
            )
        except Exception as error:  # noqa: BLE001
            raise VectorStoreInfrastructureError(f"Failed to upsert chunk '{chunk_id}' into Qdrant.") from error

    def search_similar(
        self,
        query_embedding: list[float],
        limit: int,
        score_threshold: float | None = None,
    ) -> list[VectorSearchResult]:
        """Return nearest vectors from Qdrant collection."""
        if len(query_embedding) != self._settings.embedding_size:
            raise VectorStoreInfrastructureError(
                "Query embedding size mismatch. "
                f"Expected {self._settings.embedding_size}, got {len(query_embedding)}."
            )

        if limit <= 0:
            raise VectorStoreInfrastructureError("limit must be greater than zero.")

        try:
            results = self._client.search(
                collection_name=self._settings.collection_name,
                query_vector=query_embedding,
                limit=limit,
                score_threshold=score_threshold,
            )
        except Exception as error:  # noqa: BLE001
            raise VectorStoreInfrastructureError("Failed to query Qdrant similarity search.") from error

        return [
            VectorSearchResult(
                chunk_id=str(point.id),
                score=float(point.score),
                payload=point.payload or {},
            )
            for point in results
        ]
