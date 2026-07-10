"""Persistent vector store for RAG retrieval with optional Redis cache."""

from __future__ import annotations

import json
import logging
import math
import os
import sqlite3
import threading
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from chat import redis_cache

logger = logging.getLogger(__name__)

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
        self._conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._init_schema()
        self._index_lock = threading.Lock()
        self._chunk_index: list[tuple[str, str, dict[str, Any], list[float]]] | None = None

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
        redis_cache.clear_cache()
        with self._index_lock:
            self._chunk_index = None

    def set_meta(self, key: str, value: str) -> None:
        self._conn.execute(
            "INSERT OR REPLACE INTO meta (key, value) VALUES (?, ?)",
            (key, value),
        )
        self._conn.commit()
        redis_cache.set_meta(key, value)

    def get_meta(self, key: str) -> str | None:
        cached = redis_cache.get_meta(key)
        if cached is not None:
            return cached
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
        redis_cache.write_chunk(chunk_id, text, metadata, embedding)
        with self._index_lock:
            if self._chunk_index is not None:
                self._chunk_index = [
                    (cid, ctext, meta, vec)
                    for cid, ctext, meta, vec in self._chunk_index
                    if cid != chunk_id
                ]
                self._chunk_index.append((chunk_id, text, metadata, embedding))

    def commit(self) -> None:
        self._conn.commit()

    def count(self) -> int:
        redis_count = redis_cache.count_chunks()
        if redis_count is not None and redis_count > 0:
            return redis_count
        row = self._conn.execute("SELECT COUNT(*) AS c FROM chunks").fetchone()
        return int(row["c"])

    def sync_redis_from_sqlite(self) -> int:
        """Populate Redis from SQLite when the cache is empty."""
        if redis_cache.get_redis() is None:
            return 0
        if (redis_cache.count_chunks() or 0) > 0:
            return redis_cache.count_chunks() or 0

        rows = self._conn.execute("SELECT id, text, metadata, embedding FROM chunks").fetchall()
        if not rows:
            return 0

        for row in rows:
            redis_cache.write_chunk(
                row["id"],
                row["text"],
                json.loads(row["metadata"]),
                json.loads(row["embedding"]),
            )
        for key in ("embedding_model", "chunk_count"):
            value = self.get_meta_from_sqlite(key)
            if value is not None:
                redis_cache.set_meta(key, value)

        logger.info("Synced %d chunks from SQLite to Redis", len(rows))
        with self._index_lock:
            self._chunk_index = None
        return len(rows)

    def get_meta_from_sqlite(self, key: str) -> str | None:
        row = self._conn.execute("SELECT value FROM meta WHERE key = ?", (key,)).fetchone()
        return row["value"] if row else None

    def _load_index(self) -> list[tuple[str, str, dict[str, Any], list[float]]]:
        with self._index_lock:
            if self._chunk_index is not None:
                return self._chunk_index

            redis_chunks = redis_cache.load_all_chunks()
            if redis_chunks is not None and redis_chunks:
                self._chunk_index = redis_chunks
                return self._chunk_index

            rows = self._conn.execute("SELECT id, text, metadata, embedding FROM chunks").fetchall()
            self._chunk_index = [
                (row["id"], row["text"], json.loads(row["metadata"]), json.loads(row["embedding"]))
                for row in rows
            ]
            return self._chunk_index

    def query(self, embedding: list[float], *, top_k: int = 6, pattern_number: int | None = None) -> list[Chunk]:
        index = self._load_index()
        scored: list[Chunk] = []
        for chunk_id, text, meta, vec in index:
            if pattern_number is not None and meta.get("pattern_number") != pattern_number:
                continue
            score = _cosine_similarity(embedding, vec)
            scored.append(Chunk(id=chunk_id, text=text, metadata=meta, score=score))
        scored.sort(key=lambda c: c.score, reverse=True)
        return scored[:top_k]

    def query_by_ids(self, chunk_ids: list[str]) -> list[Chunk]:
        index = self._load_index()
        by_id = {chunk_id: (text, meta) for chunk_id, text, meta, _ in index}
        chunks: list[Chunk] = []
        for chunk_id in chunk_ids:
            item = by_id.get(chunk_id)
            if item is None:
                continue
            text, meta = item
            chunks.append(Chunk(id=chunk_id, text=text, metadata=meta, score=0.0))
        return chunks

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
