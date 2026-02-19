from __future__ import annotations

from types import SimpleNamespace
import unittest

import src.infrastructure.vector_store.qdrant_adapter as adapter
from src.infrastructure.vector_store.qdrant_adapter import (
    QdrantSettings,
    QdrantVectorStore,
    VectorStoreInfrastructureError,
)


class FakeQdrantClient:
    def __init__(self) -> None:
        self.exists = False
        self.created = False
        self.upsert_called = False

    def collection_exists(self, collection_name: str) -> bool:
        return self.exists

    def create_collection(self, **kwargs: object) -> None:
        self.created = True

    def upsert(self, **kwargs: object) -> None:
        self.upsert_called = True

    def search(self, **kwargs: object) -> list[SimpleNamespace]:
        return [SimpleNamespace(id="chunk-1", score=0.99, payload={"document_id": "doc-1"})]


class QdrantAdapterTests(unittest.TestCase):
    def setUp(self) -> None:
        adapter.qdrant_models = adapter.qdrant_models or SimpleNamespace(
            VectorParams=lambda **kwargs: kwargs,
            Distance=SimpleNamespace(COSINE="cosine"),
            PointStruct=lambda **kwargs: kwargs,
        )
        self.settings = QdrantSettings(
            url="http://localhost:6333",
            collection_name="atlas_chunks",
            embedding_size=3,
        )
        self.client = FakeQdrantClient()
        self.store = QdrantVectorStore(settings=self.settings, client=self.client)

    def test_ensure_collection_creates_when_absent(self) -> None:
        self.store.ensure_collection()
        self.assertTrue(self.client.created)

    def test_upsert_validates_embedding_size(self) -> None:
        with self.assertRaises(VectorStoreInfrastructureError):
            self.store.upsert_embedding(
                chunk_id="chunk-1",
                embedding=[0.1],
                payload={},
            )

    def test_search_returns_port_result_type(self) -> None:
        results = self.store.search_similar(query_embedding=[0.1, 0.2, 0.3], limit=1)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].chunk_id, "chunk-1")
        self.assertEqual(results[0].payload["document_id"], "doc-1")


if __name__ == "__main__":
    unittest.main()
