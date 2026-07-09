"""Persistent vector store for RAG retrieval."""

from __future__ import annotations

import json
import math
import os
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Any


DEFAULT_STORE_DIR = Path(os.getenv("CHAT_DATA_DIR", "data/chat"))
DEFAULT_DB_PATH = DEFAULT_STORE_DIR / "rag.sqlite"


@dataclass
class Chunk:
    id: str
    text: str
    metadata: dict[str, Any]
    score: float = 0.0


class VectorStore:
    def __init__(self, db_path: Path | None = None) -> None:
        self.db_path = db_path or DEFAULT_DB_PATH
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(self.db_path)
        self._conn.row_factory = sqlite3.Row
        self._init_schema()

    def _init_schema(self) -> None:
        self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS chunks (
                id TEXT PRIMARY KEY,
                text TEXT NOT NULL,
                metadata TEXT NOT NULL,
                embedding TEXT NOT NULL
            )
            """
        )
        self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS meta (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            )
            """
        )
        self._conn.commit()

    def clear(self) -> None:
        self._conn.execute("DELETE FROM chunks")
        self._conn.execute("DELETE FROM meta")
        self._conn.commit()

    def set_meta(self, key: str, value: str) -> None:
        self._conn.execute(
            "INSERT OR REPLACE INTO meta (key, value) VALUES (?, ?)",
            (key, value),
        )
        self._conn.commit()

    def get_meta(self, key: str) -> str | None:
        row = self._conn.execute("SELECT value FROM meta WHERE key = ?", (key,)).fetchone()
        return row["value"] if row else None

    def upsert(self, chunk_id: str, text: str, metadata: dict[str, Any], embedding: list[float]) -> None:
        self._conn.execute(
            """
            INSERT OR REPLACE INTO chunks (id, text, metadata, embedding)
            VALUES (?, ?, ?, ?)
            """,
            (chunk_id, text, json.dumps(metadata), json.dumps(embedding)),
        )

    def commit(self) -> None:
        self._conn.commit()

    def count(self) -> int:
        row = self._conn.execute("SELECT COUNT(*) AS c FROM chunks").fetchone()
        return int(row["c"])

    def query(self, embedding: list[float], *, top_k: int = 6, pattern_number: int | None = None) -> list[Chunk]:
        rows = self._conn.execute("SELECT id, text, metadata, embedding FROM chunks").fetchall()
        scored: list[Chunk] = []
        for row in rows:
            meta = json.loads(row["metadata"])
            if pattern_number is not None and meta.get("pattern_number") != pattern_number:
                continue
            vec = json.loads(row["embedding"])
            score = _cosine_similarity(embedding, vec)
            scored.append(Chunk(id=row["id"], text=row["text"], metadata=meta, score=score))
        scored.sort(key=lambda c: c.score, reverse=True)
        return scored[:top_k]

    def close(self) -> None:
        self._conn.close()


def _cosine_similarity(a: list[float], b: list[float]) -> float:
    if not a or not b or len(a) != len(b):
        return 0.0
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


_store: VectorStore | None = None


def get_store() -> VectorStore:
    global _store
    if _store is None:
        _store = VectorStore()
    return _store
