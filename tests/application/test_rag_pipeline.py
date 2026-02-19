from __future__ import annotations

import unittest

from src.application import (
    EmbeddingPort,
    GenerationPort,
    RAGPipelineError,
    RAGPipelineService,
    RAGRequest,
    VectorSearchResult,
    VectorStorePort,
)


class FakeEmbeddingService(EmbeddingPort):
    def embed_text(self, text: str) -> list[float]:
        return [0.1, 0.2, 0.3]


class FakeGenerationService(GenerationPort):
    def generate_text(self, prompt: str) -> str:
        return "Atlas is a RAG platform."


class FakeVectorStore(VectorStorePort):
    def ensure_collection(self) -> None:
        return None

    def upsert_embedding(self, chunk_id: str, embedding: list[float], payload: dict[str, object]) -> None:
        return None

    def search_similar(
        self,
        query_embedding: list[float],
        limit: int,
        score_threshold: float | None = None,
    ) -> list[VectorSearchResult]:
        return [
            VectorSearchResult(
                chunk_id="chunk-1",
                score=0.94,
                payload={"text": "Atlas is a Retrieval-Augmented Generation platform."},
            )
        ]


class EmptyVectorStore(FakeVectorStore):
    def search_similar(
        self,
        query_embedding: list[float],
        limit: int,
        score_threshold: float | None = None,
    ) -> list[VectorSearchResult]:
        return []


class RAGPipelineServiceTests(unittest.TestCase):
    def test_rag_pipeline_returns_answer_with_sources(self) -> None:
        service = RAGPipelineService(
            vector_store=FakeVectorStore(),
            embedding_service=FakeEmbeddingService(),
            generation_service=FakeGenerationService(),
        )

        answer = service.run(RAGRequest(query_text="What is Atlas?", top_k=3))

        self.assertEqual(answer.text, "Atlas is a RAG platform.")
        self.assertEqual(answer.source_chunk_ids, ["chunk-1"])
        self.assertEqual(answer.metadata["top_k"], 3)

    def test_rag_pipeline_fails_without_retrieved_context(self) -> None:
        service = RAGPipelineService(
            vector_store=EmptyVectorStore(),
            embedding_service=FakeEmbeddingService(),
            generation_service=FakeGenerationService(),
        )

        with self.assertRaises(RAGPipelineError):
            service.run(RAGRequest(query_text="What is Atlas?"))


if __name__ == "__main__":
    unittest.main()
