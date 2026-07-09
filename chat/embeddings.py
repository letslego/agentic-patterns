"""Embedding providers for RAG ingestion and retrieval."""

from __future__ import annotations

import os
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


def get_embedder() -> Embedder:
    if os.environ.get("OPENAI_API_KEY"):
        return OpenAIEmbedder()
    try:
        return LocalEmbedder()
    except RuntimeError:
        return HashEmbedder()
