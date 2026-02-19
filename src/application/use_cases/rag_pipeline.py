"""Minimal RAG pipeline use case."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from src.application.ports import EmbeddingPort, GenerationPort, ObservabilityPort, VectorStorePort
from src.domain import Answer, Query


class RAGPipelineError(Exception):
    """Raised when RAG pipeline execution fails."""


@dataclass(frozen=True)
class RAGRequest:
    """Input contract for minimal RAG pipeline."""

    query_text: str
    top_k: int = 3
    score_threshold: float | None = None
    prompt_version: str = "v1"
    model_version: str = "gemini-1.5-flash"
    dataset_version: str = "unversioned"


class RAGPipelineService:
    """Use case for retrieval, prompt construction and answer generation."""

    def __init__(
        self,
        vector_store: VectorStorePort,
        embedding_service: EmbeddingPort,
        generation_service: GenerationPort,
        observability_service: ObservabilityPort | None = None,
    ) -> None:
        self._vector_store = vector_store
        self._embedding_service = embedding_service
        self._generation_service = generation_service
        self._observability_service = observability_service

    def run(self, request: RAGRequest) -> Answer:
        """Execute minimal RAG flow and return answer with source chunk IDs."""
        trace_id = self._start_trace(request)

        try:
            query = Query.create(text=request.query_text)
            query_embedding = self._embedding_service.embed_text(query.text)
            self._log_event(
                trace_id,
                "embedding.generated",
                {"embedding_dimensions": len(query_embedding)},
            )

            retrieved_chunks = self._vector_store.search_similar(
                query_embedding=query_embedding,
                limit=request.top_k,
                score_threshold=request.score_threshold,
            )
            self._log_event(
                trace_id,
                "retrieval.completed",
                {
                    "retrieved_count": len(retrieved_chunks),
                    "top_k": request.top_k,
                    "score_threshold": request.score_threshold,
                },
            )

            if not retrieved_chunks:
                raise RAGPipelineError(
                    "No relevant context found for query. Ingest TXT files before querying."
                )

            context_blocks = []
            source_chunk_ids: list[str] = []
            for item in retrieved_chunks:
                source_text = str(item.payload.get("text", "")).strip()
                if not source_text:
                    continue
                source_chunk_ids.append(item.chunk_id)
                context_blocks.append(f"[chunk_id={item.chunk_id}] {source_text}")

            if not context_blocks:
                raise RAGPipelineError(
                    "Retrieved chunks did not contain 'text' payload required for prompt context."
                )

            prompt = self._build_prompt(query.text, context_blocks)
            self._log_event(
                trace_id,
                "prompt.built",
                {
                    "prompt_version": request.prompt_version,
                    "context_chunks_used": len(context_blocks),
                    "prompt_length": len(prompt),
                },
            )

            generated_text = self._generation_service.generate_text(prompt)

            answer = Answer.create(
                text=generated_text,
                source_chunk_ids=source_chunk_ids,
                metadata={
                    "query_text": query.text,
                    "top_k": request.top_k,
                    "prompt_version": request.prompt_version,
                    "model_version": request.model_version,
                    "dataset_version": request.dataset_version,
                },
            )

            self._end_trace(
                trace_id,
                status="success",
                payload={
                    "answer_length": len(answer.text),
                    "sources_count": len(answer.source_chunk_ids),
                },
            )
            return answer

        except Exception as error:
            self._end_trace(
                trace_id,
                status="error",
                payload={"error_type": error.__class__.__name__, "error_message": str(error)},
            )
            raise

    @staticmethod
    def _build_prompt(query_text: str, context_blocks: list[str]) -> str:
        context = "\n\n".join(context_blocks)
        return (
            "You are a factual assistant. Use only the provided context. "
            "If the answer is not in context, say you do not know.\n\n"
            f"Context:\n{context}\n\n"
            f"Question: {query_text}\n"
            "Answer with concise factual statements and no hallucinations."
        )

    def _start_trace(self, request: RAGRequest) -> str | None:
        if self._observability_service is None:
            return None

        return self._observability_service.start_trace(
            name="rag_pipeline.run",
            tags=["phase-5", "phase-6-observability"],
            metadata={
                "prompt_version": request.prompt_version,
                "model_version": request.model_version,
                "dataset_version": request.dataset_version,
                "top_k": request.top_k,
            },
        )

    def _log_event(self, trace_id: str | None, name: str, payload: dict[str, Any]) -> None:
        if self._observability_service is None or trace_id is None:
            return
        self._observability_service.log_event(trace_id=trace_id, name=name, payload=payload)

    def _end_trace(self, trace_id: str | None, status: str, payload: dict[str, Any]) -> None:
        if self._observability_service is None or trace_id is None:
            return
        self._observability_service.end_trace(trace_id=trace_id, status=status, payload=payload)
