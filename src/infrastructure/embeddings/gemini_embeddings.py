"""Gemini embeddings adapter."""

from __future__ import annotations

from src.application import EmbeddingPort

try:
    import google.generativeai as genai
except ImportError:  # pragma: no cover
    genai = None


class GeminiEmbeddingError(Exception):
    """Raised when Gemini embedding requests fail."""


class GeminiEmbeddingAdapter(EmbeddingPort):
    """Gemini implementation for embeddings."""

    def __init__(self, api_key: str, model_name: str = "models/text-embedding-004") -> None:
        if not api_key.strip():
            raise GeminiEmbeddingError("GEMINI_API_KEY cannot be empty.")
        if genai is None:
            raise GeminiEmbeddingError(
                "google-generativeai is not installed. Install dependencies before running Phase 5."
            )
        self._model_name = model_name
        genai.configure(api_key=api_key)

    def embed_text(self, text: str) -> list[float]:
        if not text.strip():
            raise GeminiEmbeddingError("Embedding text cannot be empty.")
        try:
            response = genai.embed_content(model=self._model_name, content=text)
        except Exception as error:  # noqa: BLE001
            raise GeminiEmbeddingError("Gemini embedding request failed.") from error

        embedding = response.get("embedding")
        if not isinstance(embedding, list) or not embedding:
            raise GeminiEmbeddingError("Gemini embedding response is invalid.")
        return [float(value) for value in embedding]
