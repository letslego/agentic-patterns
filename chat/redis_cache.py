"""Optional Redis KV cache for RAG chunks and query results."""

from __future__ import annotations

import hashlib
import json
import logging
import os
from typing import Any

logger = logging.getLogger(__name__)

PREFIX = "rag:"
CHUNK_IDS_KEY = f"{PREFIX}chunks:ids"
QUERY_CACHE_TTL = int(os.getenv("RAG_QUERY_CACHE_TTL", "3600"))

_client: Any | None = None
_client_failed = False


def redis_url() -> str | None:
    url = os.getenv("REDIS_URL", "").strip()
    return url or None


def get_redis() -> Any | None:
    """Return a Redis client or None when unavailable."""
    global _client, _client_failed
    if _client_failed or not redis_url():
        return None
    if _client is not None:
        return _client
    try:
        import redis

        _client = redis.from_url(
            redis_url(),
            decode_responses=True,
            socket_connect_timeout=5,
            socket_timeout=5,
            retry_on_timeout=True,
        )
        _client.ping()
        return _client
    except Exception as exc:
        logger.warning("Redis unavailable, falling back to SQLite: %s", exc)
        _client_failed = True
        return None


def _chunk_key(chunk_id: str) -> str:
    return f"{PREFIX}chunk:{chunk_id}"


def _meta_key(key: str) -> str:
    return f"{PREFIX}meta:{key}"


def _query_emb_key(normalized_query: str) -> str:
    digest = hashlib.sha256(normalized_query.encode()).hexdigest()[:32]
    return f"{PREFIX}query:emb:{digest}"


def _query_results_key(normalized_query: str, pattern_number: int | None, top_k: int) -> str:
    scope = pattern_number if pattern_number is not None else "all"
    digest = hashlib.sha256(f"{normalized_query}|{scope}|{top_k}".encode()).hexdigest()[:32]
    return f"{PREFIX}query:results:{digest}"


def normalize_query(query: str) -> str:
    return " ".join(query.lower().split())


def clear_cache() -> None:
    client = get_redis()
    if client is None:
        return
    try:
        keys = list(client.scan_iter(match=f"{PREFIX}*"))
        if keys:
            client.delete(*keys)
    except Exception as exc:
        logger.warning("Redis clear failed: %s", exc)


def set_meta(key: str, value: str) -> None:
    client = get_redis()
    if client is None:
        return
    try:
        client.set(_meta_key(key), value)
    except Exception as exc:
        logger.warning("Redis set_meta failed: %s", exc)


def get_meta(key: str) -> str | None:
    client = get_redis()
    if client is None:
        return None
    try:
        return client.get(_meta_key(key))
    except Exception as exc:
        logger.warning("Redis get_meta failed: %s", exc)
        return None


def write_chunk(chunk_id: str, text: str, metadata: dict[str, Any], embedding: list[float]) -> None:
    client = get_redis()
    if client is None:
        return
    try:
        payload = json.dumps(
            {"id": chunk_id, "text": text, "metadata": metadata, "embedding": embedding},
            separators=(",", ":"),
        )
        pipe = client.pipeline()
        pipe.set(_chunk_key(chunk_id), payload)
        pipe.sadd(CHUNK_IDS_KEY, chunk_id)
        pipe.execute()
    except Exception as exc:
        logger.warning("Redis write_chunk failed: %s", exc)


def count_chunks() -> int | None:
    client = get_redis()
    if client is None:
        return None
    try:
        return int(client.scard(CHUNK_IDS_KEY))
    except Exception as exc:
        logger.warning("Redis count_chunks failed: %s", exc)
        return None


def load_all_chunks() -> list[tuple[str, str, dict[str, Any], list[float]]] | None:
    client = get_redis()
    if client is None:
        return None
    try:
        chunk_ids = client.smembers(CHUNK_IDS_KEY)
        if not chunk_ids:
            return []
        pipe = client.pipeline()
        for chunk_id in chunk_ids:
            pipe.get(_chunk_key(chunk_id))
        rows = pipe.execute()
        chunks: list[tuple[str, str, dict[str, Any], list[float]]] = []
        for raw in rows:
            if not raw:
                continue
            data = json.loads(raw)
            chunks.append((data["id"], data["text"], data["metadata"], data["embedding"]))
        return chunks
    except Exception as exc:
        logger.warning("Redis load_all_chunks failed: %s", exc)
        return None


def cache_query_embedding(normalized_query: str, embedding: list[float]) -> None:
    client = get_redis()
    if client is None:
        return
    try:
        client.setex(
            _query_emb_key(normalized_query),
            QUERY_CACHE_TTL,
            json.dumps(embedding, separators=(",", ":")),
        )
    except Exception as exc:
        logger.warning("Redis cache_query_embedding failed: %s", exc)


def get_cached_query_embedding(normalized_query: str) -> list[float] | None:
    client = get_redis()
    if client is None:
        return None
    try:
        raw = client.get(_query_emb_key(normalized_query))
        if not raw:
            return None
        return json.loads(raw)
    except Exception as exc:
        logger.warning("Redis get_cached_query_embedding failed: %s", exc)
        return None


def cache_query_results(
    normalized_query: str,
    *,
    pattern_number: int | None,
    top_k: int,
    chunk_ids: list[str],
) -> None:
    client = get_redis()
    if client is None:
        return
    try:
        client.setex(
            _query_results_key(normalized_query, pattern_number, top_k),
            QUERY_CACHE_TTL,
            json.dumps(chunk_ids, separators=(",", ":")),
        )
    except Exception as exc:
        logger.warning("Redis cache_query_results failed: %s", exc)


def get_cached_query_results(
    normalized_query: str,
    *,
    pattern_number: int | None,
    top_k: int,
) -> list[str] | None:
    client = get_redis()
    if client is None:
        return None
    try:
        raw = client.get(_query_results_key(normalized_query, pattern_number, top_k))
        if not raw:
            return None
        return json.loads(raw)
    except Exception as exc:
        logger.warning("Redis get_cached_query_results failed: %s", exc)
        return None
