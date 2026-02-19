from __future__ import annotations

from datetime import datetime, timezone
import unittest

from src.domain import Answer, Chunk, Document, Query


class DomainEntitiesTests(unittest.TestCase):
    def test_document_requires_traceability_fields(self) -> None:
        document = Document.create(
            id="doc-1",
            source_path="knowledge/example.txt",
            metadata={"source": "user-upload"},
        )

        self.assertEqual(document.id, "doc-1")
        self.assertEqual(document.source_path, "knowledge/example.txt")
        self.assertIsNotNone(document.created_at.tzinfo)
        self.assertEqual(document.metadata["source"], "user-upload")

    def test_document_rejects_empty_source_path(self) -> None:
        with self.assertRaises(ValueError):
            Document(
                id="doc-1",
                source_path="",
                created_at=datetime.now(timezone.utc),
                metadata={},
            )

    def test_chunk_validation(self) -> None:
        chunk = Chunk(
            id="chunk-1",
            document_id="doc-1",
            content="content",
            sequence_number=0,
            metadata={"token_count": 2},
        )

        self.assertEqual(chunk.document_id, "doc-1")
        self.assertEqual(chunk.metadata["token_count"], 2)

    def test_query_validation(self) -> None:
        query = Query.create(text="What is Atlas?", metadata={"channel": "api"})

        self.assertEqual(query.text, "What is Atlas?")
        self.assertEqual(query.metadata["channel"], "api")

    def test_answer_requires_sources(self) -> None:
        with self.assertRaises(ValueError):
            Answer.create(text="answer", source_chunk_ids=[])

        answer = Answer.create(text="answer", source_chunk_ids=["chunk-1", "  "])
        self.assertEqual(answer.source_chunk_ids, ["chunk-1"])


if __name__ == "__main__":
    unittest.main()
