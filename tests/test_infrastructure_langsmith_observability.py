from __future__ import annotations

from types import SimpleNamespace
import unittest

import src.infrastructure.observability.langsmith_tracer as tracer_module
from src.infrastructure.observability import (
    LangSmithObservabilityAdapter,
    LangSmithSettings,
)


class FakeLangSmithClient:
    def __init__(self, api_key: str, api_url: str) -> None:
        self.api_key = api_key
        self.api_url = api_url
        self.runs: list[dict[str, object]] = []

    def create_run(self, **kwargs: object) -> None:
        self.runs.append(kwargs)


class LangSmithObservabilityTests(unittest.TestCase):
    def test_adapter_submits_run(self) -> None:
        tracer_module.Client = FakeLangSmithClient

        adapter = LangSmithObservabilityAdapter(
            LangSmithSettings(
                api_key="test-key",
                project="atlas-rag-platform",
                endpoint="https://api.smith.langchain.com",
            )
        )
        trace_id = adapter.start_trace(
            name="rag_pipeline.run",
            tags=["phase-6"],
            metadata={"prompt_version": "v1"},
        )
        adapter.log_event(trace_id=trace_id, name="retrieval.completed", payload={"count": 1})
        adapter.end_trace(trace_id=trace_id, status="success", payload={"sources": 1})

        client = adapter._client
        self.assertEqual(len(client.runs), 1)
        self.assertEqual(client.runs[0]["project_name"], "atlas-rag-platform")


if __name__ == "__main__":
    unittest.main()
