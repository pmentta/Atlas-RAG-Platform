from __future__ import annotations

import unittest

from src.application import (
    EmbeddingPort,
    GenerationPort,
    ObservabilityPort,
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


class FakeObservabilityService(ObservabilityPort):
    def __init__(self) -> None:
        self.events: list[tuple[str, str, dict[str, object]]] = []

    def start_trace(self, name: str, tags: list[str], metadata: dict[str, object]) -> str:
        self.events.append(("start", name, metadata))
        return "trace-1"

    def log_event(self, trace_id: str, name: str, payload: dict[str, object]) -> None:
        self.events.append(("event", name, payload))

    def end_trace(self, trace_id: str, status: str, payload: dict[str, object]) -> None:
        self.events.append(("end", status, payload))


class RAGPipelineServiceTests(unittest.TestCase):
    def test_rag_pipeline_returns_answer_with_sources(self) -> None:
        observability = FakeObservabilityService()
        service = RAGPipelineService(
            vector_store=FakeVectorStore(),
            embedding_service=FakeEmbeddingService(),
            generation_service=FakeGenerationService(),
            observability_service=observability,
        )

        answer = service.run(
            RAGRequest(
                query_text="What is Atlas?",
                top_k=3,
                prompt_version="v2",
                model_version="gemini-1.5-flash",
                dataset_version="kb-2026-02",
            )
        )

        self.assertEqual(answer.text, "Atlas is a RAG platform.")
        self.assertEqual(answer.source_chunk_ids, ["chunk-1"])
        self.assertEqual(answer.metadata["top_k"], 3)
        self.assertEqual(answer.metadata["prompt_version"], "v2")
        self.assertEqual(answer.metadata["dataset_version"], "kb-2026-02")

        event_names = [event[1] for event in observability.events]
        self.assertIn("embedding.generated", event_names)
        self.assertIn("retrieval.completed", event_names)
        self.assertIn("prompt.built", event_names)
        self.assertIn("success", event_names)

    def test_rag_pipeline_fails_without_retrieved_context(self) -> None:
        observability = FakeObservabilityService()
        service = RAGPipelineService(
            vector_store=EmptyVectorStore(),
            embedding_service=FakeEmbeddingService(),
            generation_service=FakeGenerationService(),
            observability_service=observability,
        )

        with self.assertRaises(RAGPipelineError):
            service.run(RAGRequest(query_text="What is Atlas?"))

        self.assertEqual(observability.events[-1][1], "error")


if __name__ == "__main__":
    unittest.main()
