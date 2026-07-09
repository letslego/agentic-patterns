"""Tests for the pattern chat app."""

from __future__ import annotations

import os
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture()
def chat_client(tmp_path, monkeypatch):
    db_path = tmp_path / "rag.sqlite"
    monkeypatch.setenv("CHAT_DATA_DIR", str(tmp_path))
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    monkeypatch.delenv("NVIDIA_API_KEY", raising=False)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    from chat.embeddings import HashEmbedder
    from chat.ingest import ingest
    from chat.main import create_app
    from chat.rag import VectorStore

    monkeypatch.setattr("chat.embeddings.get_embedder", lambda: HashEmbedder())
    monkeypatch.setattr("chat.ingest.get_embedder", lambda: HashEmbedder())
    monkeypatch.setattr("chat.main.get_embedder", lambda: HashEmbedder())

    store = VectorStore(db_path=db_path)
    count = ingest(store=store, root=ROOT)
    assert count > 0

    return TestClient(create_app())


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


def test_health_endpoint(chat_client):
    res = chat_client.get("/api/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "ok"
    assert data["chunks"] > 0
    assert data["mock_mode"] is True
    assert data["llm_provider"] == "mock"


def test_patterns_endpoint(chat_client):
    res = chat_client.get("/api/patterns")
    assert res.status_code == 200
    patterns = res.json()
    assert len(patterns) == 21
    assert patterns[0]["number"] == 1
    assert "code_path" in patterns[0]


def test_chat_mock_mode(chat_client):
    res = chat_client.post(
        "/api/chat",
        json={"messages": [{"role": "user", "content": "What is prompt chaining?"}], "stream": False},
    )
    assert res.status_code == 200
    data = res.json()
    assert "message" in data
    assert "Mock mode" in data["message"] or "pattern" in data["message"].lower()
