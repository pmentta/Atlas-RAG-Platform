from __future__ import annotations

import os
import unittest

from src.infrastructure.config import SettingsError, load_settings


class SettingsTests(unittest.TestCase):
    def setUp(self) -> None:
        self._old_env = dict(os.environ)

    def tearDown(self) -> None:
        os.environ.clear()
        os.environ.update(self._old_env)

    def test_load_settings_requires_qdrant_url(self) -> None:
        os.environ.pop("QDRANT_URL", None)
        os.environ["GEMINI_API_KEY"] = "dummy-key"
        with self.assertRaises(SettingsError):
            load_settings()

    def test_load_settings_requires_gemini_api_key(self) -> None:
        os.environ["QDRANT_URL"] = "http://localhost:6333"
        os.environ.pop("GEMINI_API_KEY", None)
        with self.assertRaises(SettingsError):
            load_settings()

    def test_load_settings_requires_langsmith_key_when_tracing_enabled(self) -> None:
        os.environ["QDRANT_URL"] = "http://localhost:6333"
        os.environ["GEMINI_API_KEY"] = "dummy-key"
        os.environ["LANGCHAIN_TRACING_V2"] = "true"
        os.environ.pop("LANGCHAIN_API_KEY", None)
        with self.assertRaises(SettingsError):
            load_settings()

    def test_load_settings_accepts_required_fields(self) -> None:
        os.environ["QDRANT_URL"] = "http://localhost:6333"
        os.environ["EMBEDDING_SIZE"] = "384"
        os.environ["GEMINI_API_KEY"] = "dummy-key"
        os.environ["LANGCHAIN_TRACING_V2"] = "false"
        settings = load_settings()
        self.assertEqual(settings.qdrant_url, "http://localhost:6333")
        self.assertEqual(settings.embedding_size, 384)
        self.assertEqual(settings.gemini_api_key, "dummy-key")


if __name__ == "__main__":
    unittest.main()
