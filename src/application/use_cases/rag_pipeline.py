"""Minimal RAG pipeline use case."""

from __future__ import annotations

from dataclasses import dataclass

from src.application.ports import EmbeddingPort, GenerationPort, VectorStorePort
from src.domain import Answer, Query


class RAGPipelineError(Exception):
    """Raised when RAG pipeline execution fails."""


@dataclass(frozen=True)
class RAGRequest:
    """Input contract for minimal RAG pipeline."""

    query_text: str
    top_k: int = 3
    score_threshold: float | None = None


class RAGPipelineService:
    """Use case for retrieval, prompt construction and answer generation."""

    def __init__(
        self,
        vector_store: VectorStorePort,
        embedding_service: EmbeddingPort,
        generation_service: GenerationPort,
    ) -> None:
        self._vector_store = vector_store
        self._embedding_service = embedding_service
        self._generation_service = generation_service

    def run(self, request: RAGRequest) -> Answer:
        """Execute minimal RAG flow and return answer with source chunk IDs."""
        query = Query.create(text=request.query_text)
        query_embedding = self._embedding_service.embed_text(query.text)
        retrieved_chunks = self._vector_store.search_similar(
            query_embedding=query_embedding,
            limit=request.top_k,
            score_threshold=request.score_threshold,
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
        generated_text = self._generation_service.generate_text(prompt)

        return Answer.create(
            text=generated_text,
            source_chunk_ids=source_chunk_ids,
            metadata={
                "query_text": query.text,
                "top_k": request.top_k,
            },
        )

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
