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


def test_pattern_14_chunk_ingested(tmp_path, monkeypatch):
    monkeypatch.setenv("CHAT_DATA_DIR", str(tmp_path))
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    from chat.embeddings import HashEmbedder
    from chat.ingest import ingest
    from chat.rag import get_store

    monkeypatch.setattr("chat.ingest.get_embedder", lambda: HashEmbedder())
    ingest(root=ROOT)
    store = get_store()
    rows = store._conn.execute("SELECT metadata FROM chunks").fetchall()
    rag_rows = [row for row in rows if "code/14_rag/main.py" in row[0]]
    assert rag_rows, "Pattern 14 example should be indexed"
    assert all("HandbookSection" not in row[0] for row in rag_rows)


def test_rag_query_retrieves_pattern_14(tmp_path, monkeypatch):
    monkeypatch.setenv("CHAT_DATA_DIR", str(tmp_path))
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    from chat.embeddings import HashEmbedder
    from chat.ingest import ingest
    from chat.rag import get_store

    monkeypatch.setattr("chat.ingest.get_embedder", lambda: HashEmbedder())
    ingest(root=ROOT)
    store = get_store()
    embedder = HashEmbedder()
    vec = embedder.embed(["Show me a simple RAG pipeline with cosine similarity"])[0]
    chunks = store.query(vec, top_k=6, pattern_number=14)
    sources = [c.metadata.get("source_file") for c in chunks]
    assert "code/14_rag/main.py" in sources


def test_redis_key_prefix_default():
    from chat import redis_cache

    assert redis_cache.key_prefix() == "agentic-patterns:"
    assert redis_cache.PREFIX == "agentic-patterns:"
    assert redis_cache._chunk_key("abc").startswith("agentic-patterns:")
