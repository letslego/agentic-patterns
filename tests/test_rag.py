"""Tests for RAG ingestion and vector store."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_ingest_creates_chunks(tmp_path, monkeypatch):
    monkeypatch.setenv("CHAT_DATA_DIR", str(tmp_path))
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    from chat.embeddings import HashEmbedder
    from chat.ingest import ingest
    from chat.rag import get_store

    monkeypatch.setattr("chat.ingest.get_embedder", lambda: HashEmbedder())

    count = ingest(root=ROOT)
    store = get_store()
    assert count > 20
    assert store.count() == count
    assert store.get_meta("embedding_model")
