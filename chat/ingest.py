"""Ingest docs and code into the RAG vector store."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path

from chat.embeddings import get_embedder
from chat.patterns import pattern_for_path
from chat.rag import VectorStore, get_store

ROOT = Path(__file__).resolve().parents[1]
CHUNK_SIZE = 1200
CHUNK_OVERLAP = 200
BATCH_SIZE = 32


def _chunk_text(text: str, *, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    text = text.strip()
    if not text:
        return []
    if len(text) <= chunk_size:
        return [text]

    chunks: list[str] = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        if end < len(text):
            break_at = max(chunk.rfind("\n\n"), chunk.rfind("\n"), chunk.rfind(". "))
            if break_at > chunk_size // 2:
                chunk = chunk[: break_at + 1]
                end = start + len(chunk)
        chunks.append(chunk.strip())
        if end >= len(text):
            break
        start = max(end - overlap, start + 1)
    return [c for c in chunks if c]


def _content_type(path: Path) -> str:
    rel = str(path.relative_to(ROOT)).replace("\\", "/")
    if rel.startswith("docs/"):
        return "doc"
    if rel.startswith("code/"):
        return "code"
    if rel.startswith("agentic_patterns/"):
        return "kernel"
    return "other"


def _metadata_for(path: Path) -> dict:
    rel = str(path.relative_to(ROOT)).replace("\\", "/")
    pattern = pattern_for_path(rel)
    meta: dict = {
        "source_file": rel,
        "content_type": _content_type(path),
        "pattern_number": pattern.number if pattern else None,
        "pattern_name": pattern.name if pattern else None,
        "pattern_slug": pattern.slug if pattern else None,
    }
    if rel == "code/14_rag/main.py":
        meta["demo_rag_corpus"] = True
    return meta


def _chunk_id(source: str, index: int) -> str:
    digest = hashlib.sha256(f"{source}:{index}".encode()).hexdigest()[:16]
    return f"{digest}"


def collect_sources() -> list[Path]:
    sources: list[Path] = []
    for pattern in sorted(ROOT.glob("docs/**/*.md")):
        if ".vitepress" in pattern.parts:
            continue
        sources.append(pattern)
    sources.extend(sorted(ROOT.glob("code/**/main.py")))
    for kernel_file in sorted((ROOT / "agentic_patterns").glob("*.py")):
        if kernel_file.name != "__init__.py":
            sources.append(kernel_file)
    return sources


def ingest(*, store: VectorStore | None = None, root: Path | None = None) -> int:
    _ = root  # reserved for tests; sources are always resolved from repo ROOT
    vector_store = store or get_store()
    embedder = get_embedder()

    vector_store.clear()
    vector_store.set_meta("embedding_model", embedder.model_name)

    pending_texts: list[str] = []
    pending_meta: list[dict] = []
    pending_ids: list[str] = []
    total = 0

    def flush() -> None:
        nonlocal total
        if not pending_texts:
            return
        vectors = embedder.embed(pending_texts)
        for chunk_id, text, meta, vector in zip(pending_ids, pending_texts, pending_meta, vectors):
            vector_store.upsert(chunk_id, text, meta, vector)
            total += 1
        pending_texts.clear()
        pending_meta.clear()
        pending_ids.clear()
        vector_store.commit()

    for source in collect_sources():
        try:
            text = source.read_text(encoding="utf-8")
        except OSError:
            continue
        rel = str(source.relative_to(ROOT)).replace("\\", "/")
        base_meta = _metadata_for(source)
        for idx, chunk in enumerate(_chunk_text(text)):
            pending_ids.append(_chunk_id(rel, idx))
            pending_texts.append(chunk)
            pending_meta.append({**base_meta, "chunk_index": idx})
            if len(pending_texts) >= BATCH_SIZE:
                flush()

    flush()
    vector_store.set_meta("chunk_count", str(total))
    vector_store.commit()
    return total


def main() -> None:
    count = ingest()
    store = get_store()
    print(f"Ingested {count} chunks into {store.db_path}")
    print(f"Embedding model: {store.get_meta('embedding_model')}")


if __name__ == "__main__":
    main()
