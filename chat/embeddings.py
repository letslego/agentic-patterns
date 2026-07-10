"""Embedding providers for RAG ingestion and retrieval."""

from __future__ import annotations

import os
import threading
from abc import ABC, abstractmethod


class Embedder(ABC):
    @abstractmethod
    def embed(self, texts: list[str]) -> list[list[float]]:
        raise NotImplementedError

    @property
    @abstractmethod
    def model_name(self) -> str:
        raise NotImplementedError


class OpenAIEmbedder(Embedder):
    def __init__(self, model: str | None = None) -> None:
        try:
            from openai import OpenAI
        except ImportError as exc:
            raise RuntimeError("Install openai: pip install openai") from exc

        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("Set OPENAI_API_KEY for OpenAI embeddings")
        self._client = OpenAI(api_key=api_key)
        self._model = model or os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")

    @property
    def model_name(self) -> str:
        return self._model

    def embed(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []
        response = self._client.embeddings.create(model=self._model, input=texts)
        return [item.embedding for item in response.data]


class LocalEmbedder(Embedder):
    """Sentence-transformers fallback when no OpenAI key is available."""

    def __init__(self, model: str | None = None) -> None:
        try:
            from sentence_transformers import SentenceTransformer
        except ImportError as exc:
            raise RuntimeError(
                "Install sentence-transformers: pip install sentence-transformers"
            ) from exc

        self._model_name = model or os.getenv(
            "LOCAL_EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2"
        )
        self._model = SentenceTransformer(self._model_name)

    @property
    def model_name(self) -> str:
        return self._model_name

    def embed(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []
        vectors = self._model.encode(texts, normalize_embeddings=True)
        return [vector.tolist() for vector in vectors]


class HashEmbedder(Embedder):
    """Deterministic lightweight embedder when no API or ML deps are available."""

    def __init__(self, dims: int = 256) -> None:
        self._dims = dims

    @property
    def model_name(self) -> str:
        return f"hash-{self._dims}"

    def embed(self, texts: list[str]) -> list[list[float]]:
        import hashlib
        import math

        vectors: list[list[float]] = []
        for text in texts:
            vec = [0.0] * self._dims
            for token in text.lower().split():
                digest = hashlib.sha256(token.encode()).digest()
                for i in range(self._dims):
                    vec[i] += (digest[i % len(digest)] - 128) / 128.0
            norm = math.sqrt(sum(v * v for v in vec)) or 1.0
            vectors.append([v / norm for v in vec])
        return vectors


_embedder: Embedder | None = None
_embedder_error: BaseException | None = None
_embedder_ready = threading.Event()
_embedder_lock = threading.Lock()
_warmup_started = False


def _create_embedder() -> Embedder:
    if os.environ.get("OPENAI_API_KEY"):
        return OpenAIEmbedder()
    try:
        return LocalEmbedder()
    except RuntimeError:
        return HashEmbedder()


def _load_embedder() -> None:
    global _embedder, _embedder_error
    try:
        _embedder = _create_embedder()
    except BaseException as exc:
        _embedder_error = exc
    finally:
        _embedder_ready.set()


def start_embedder_warmup() -> None:
    global _warmup_started
    with _embedder_lock:
        if _warmup_started:
            return
        _warmup_started = True
        thread = threading.Thread(target=_load_embedder, name="embedder-warmup", daemon=True)
        thread.start()


def embedder_status() -> dict[str, str | bool | None]:
    if _embedder is not None:
        return {"ready": True, "model": _embedder.model_name, "error": None}
    if _embedder_error is not None:
        return {"ready": False, "model": None, "error": str(_embedder_error)}
    if _warmup_started:
        return {"ready": False, "model": None, "error": None}
    return {"ready": False, "model": None, "error": None}


def get_embedder(*, timeout: float | None = None) -> Embedder:
    start_embedder_warmup()
    if timeout is None:
        timeout = float(os.getenv("EMBEDDER_WARMUP_TIMEOUT", "120"))
    if not _embedder_ready.wait(timeout=timeout):
        raise RuntimeError("Embedding model is still warming up; try again shortly.")
    if _embedder_error is not None:
        raise RuntimeError(f"Embedding model failed to load: {_embedder_error}") from _embedder_error
    assert _embedder is not None
    return _embedder
