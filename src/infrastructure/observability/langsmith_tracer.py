"""LangSmith tracer adapter."""

from __future__ import annotations

from dataclasses import dataclass
from time import time
from typing import Any
from uuid import uuid4

from src.application import ObservabilityPort

try:
    from langsmith import Client
except ImportError:  # pragma: no cover
    Client = None


class LangSmithObservabilityError(Exception):
    """Raised when LangSmith instrumentation fails."""


@dataclass(frozen=True)
class LangSmithSettings:
    """LangSmith runtime configuration."""

    api_key: str
    project: str
    endpoint: str


class LangSmithObservabilityAdapter(ObservabilityPort):
    """LangSmith implementation for execution tracing."""

    def __init__(self, settings: LangSmithSettings) -> None:
        if Client is None:
            raise LangSmithObservabilityError(
                "langsmith is not installed. Install dependencies before enabling tracing."
            )
        if not settings.api_key.strip():
            raise LangSmithObservabilityError("LANGCHAIN_API_KEY cannot be empty when tracing is enabled.")

        self._client = Client(api_key=settings.api_key, api_url=settings.endpoint)
        self._project = settings.project
        self._runs: dict[str, dict[str, Any]] = {}

    def start_trace(self, name: str, tags: list[str], metadata: dict[str, Any]) -> str:
        trace_id = str(uuid4())
        self._runs[trace_id] = {
            "name": name,
            "tags": tags,
            "metadata": metadata,
            "start_time": time(),
        }
        return trace_id

    def log_event(self, trace_id: str, name: str, payload: dict[str, Any]) -> None:
        if trace_id not in self._runs:
            raise LangSmithObservabilityError(f"Unknown trace_id '{trace_id}'.")

        event_list = self._runs[trace_id].setdefault("events", [])
        event_list.append({"name": name, "payload": payload, "timestamp": time()})

    def end_trace(self, trace_id: str, status: str, payload: dict[str, Any]) -> None:
        run = self._runs.pop(trace_id, None)
        if run is None:
            raise LangSmithObservabilityError(f"Unknown trace_id '{trace_id}'.")

        end_time = time()
        inputs = {
            "metadata": run["metadata"],
            "events": run.get("events", []),
        }
        outputs = {
            "status": status,
            "summary": payload,
        }

        try:
            self._client.create_run(
                name=run["name"],
                run_type="chain",
                project_name=self._project,
                inputs=inputs,
                outputs=outputs,
                tags=run["tags"],
                start_time=run["start_time"],
                end_time=end_time,
            )
        except Exception as error:  # noqa: BLE001
            raise LangSmithObservabilityError("Failed to submit trace to LangSmith.") from error
