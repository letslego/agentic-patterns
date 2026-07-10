"""Pattern 14: RAG — simple retrieve-then-generate pipeline."""

from __future__ import annotations

import math
import re
from dataclasses import dataclass

from agentic_patterns.common import get_llm

# corpus -> embed -> retrieve top-k -> prompt LLM with context -> answer

CORPUS = [
    "RAG (retrieval-augmented generation) grounds LLM answers in external documents.",
    "Chunk source documents, embed each chunk and the user query, then rank by cosine similarity.",
    "Pass the top-k retrieved chunks into the prompt as context before calling the LLM.",
    "Cite chunk ids in answers so users can verify which sources were used.",
]


@dataclass(frozen=True)
class Chunk:
    chunk_id: str
    text: str


def _tokenize(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


def _build_vocab(texts: list[str]) -> dict[str, int]:
    vocab: dict[str, int] = {}
    for text in texts:
        for token in _tokenize(text):
            if token not in vocab:
                vocab[token] = len(vocab)
    return vocab


def _embed(text: str, vocab: dict[str, int]) -> list[float]:
    vec = [0.0] * len(vocab)
    for token in _tokenize(text):
        idx = vocab.get(token)
        if idx is not None:
            vec[idx] += 1.0
    norm = math.sqrt(sum(x * x for x in vec))
    return [x / norm for x in vec] if norm else vec


def _cosine(a: list[float], b: list[float]) -> float:
    return sum(x * y for x, y in zip(a, b))


def index_corpus(texts: list[str]) -> tuple[list[Chunk], dict[str, int]]:
    chunks = [Chunk(f"C-{i:02d}", text) for i, text in enumerate(texts, start=1)]
    vocab = _build_vocab(texts)
    return chunks, vocab


def retrieve(query: str, chunks: list[Chunk], vocab: dict[str, int], k: int = 2) -> list[Chunk]:
    query_vec = _embed(query, vocab)
    ranked = sorted(
        chunks,
        key=lambda c: _cosine(query_vec, _embed(c.text, vocab)),
        reverse=True,
    )
    return ranked[:k]


def rag_answer(question: str, chunks: list[Chunk], vocab: dict[str, int]) -> str:
    hits = retrieve(question, chunks, vocab)
    context = "\n".join(f"[{c.chunk_id}] {c.text}" for c in hits)
    llm = get_llm()
    return llm.complete(
        f"Answer using the retrieved documents only.\n\nContext:\n{context}\n\nQuestion: {question}"
    )


if __name__ == "__main__":
    chunks, vocab = index_corpus(CORPUS)
    print(rag_answer("How does RAG ground an LLM answer?", chunks, vocab))
