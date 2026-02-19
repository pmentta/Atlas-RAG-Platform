"""Gemini generation adapter."""

from __future__ import annotations

from src.application import GenerationPort

try:
    import google.generativeai as genai
except ImportError:  # pragma: no cover
    genai = None


class GeminiGenerationError(Exception):
    """Raised when Gemini generation fails."""


class GeminiGenerationAdapter(GenerationPort):
    """Gemini implementation for text generation."""

    def __init__(self, api_key: str, model_name: str) -> None:
        if not api_key.strip():
            raise GeminiGenerationError("GEMINI_API_KEY cannot be empty.")
        if genai is None:
            raise GeminiGenerationError(
                "google-generativeai is not installed. Install dependencies before running Phase 5."
            )
        self._model_name = model_name
        genai.configure(api_key=api_key)
        self._model = genai.GenerativeModel(model_name)

    def generate_text(self, prompt: str) -> str:
        if not prompt.strip():
            raise GeminiGenerationError("Prompt cannot be empty.")
        try:
            response = self._model.generate_content(prompt)
        except Exception as error:  # noqa: BLE001
            raise GeminiGenerationError("Gemini generation request failed.") from error

        text = getattr(response, "text", "")
        if not str(text).strip():
            raise GeminiGenerationError("Gemini returned an empty response.")
        return str(text).strip()
