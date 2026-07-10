"""FastAPI backend for the pattern chat app."""

from __future__ import annotations

import json
import logging
import os
import threading
from pathlib import Path
from typing import Any, Iterator

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from chat import redis_cache
from chat.embeddings import embedder_status, get_embedder, start_embedder_warmup
from chat.llm import get_chat_llm
from chat.patterns import patterns_payload
from chat.rag import corpus_version, get_store

logger = logging.getLogger(__name__)

STATIC_DIR = Path(__file__).parent / "static"

SYSTEM_PROMPT_HEAD = """You are an expert on the 21 agentic design patterns from the agentic-patterns repository.

Rules:
- Answer ONLY from the retrieved context below. Do not invent facts from outside knowledge.
- Always cite pattern numbers and names when relevant (e.g. "Pattern 03: Parallelization").
- When the user asks for code or a recipe, synthesize a SIMPLE minimal example inspired by the retrieved context — do not copy-paste large raw repo chunks verbatim.
- Prefer clean, educational code (~30–80 lines) over dumping full source files. Use `agentic_patterns.common.get_llm()` and note that mock mode works without API keys.
- Reference actual repo paths: code lives in `code/NN_name/main.py`, shared primitives in `agentic_patterns/kernel.py`, guides in `docs/`.
- Never reproduce fictional demo domains (handbooks, expense reports, IT tickets, press releases) as if they were real — teach the pattern structure instead.
- Pattern recipe shapes: chaining (stages), routing (classify→dispatch), parallelization (gather→merge), reflection (draft→critique→revise), RAG (embed→retrieve→generate), multi-agent (sequential specialists).
- Keep answers practical and concise. Use markdown with fenced Python code blocks.
- If retrieved context is insufficient, say so and suggest which pattern chapter to read.

Retrieved context from the repository:
"""

SYSTEM_PROMPT_TAIL = ""


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: list[ChatMessage]
    pattern_number: int | None = Field(default=None, ge=1, le=21)
    stream: bool = False
    top_k: int = Field(default=6, ge=1, le=12)


def _background_warmup() -> None:
    try:
        redis_cache.purge_legacy_keys()
        store = get_store()
        synced = store.sync_redis_from_sqlite()
        if synced:
            logger.info("Redis cache warmed with %d chunks", synced)
    except Exception as exc:
        logger.warning("Background Redis sync failed: %s", exc)
    start_embedder_warmup()


def create_app() -> FastAPI:
    app = FastAPI(title="Agentic Patterns Chat", version="0.1.0")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.on_event("startup")
    def on_startup() -> None:
        threading.Thread(target=_background_warmup, name="rag-warmup", daemon=True).start()

    @app.get("/api/health")
    def health() -> dict[str, Any]:
        llm = get_chat_llm()
        embedder = embedder_status()
        chunks: int | None = None
        embedding_model: str | None = None
        try:
            store = get_store()
            chunks = store.count()
            embedding_model = store.get_meta("embedding_model")
        except Exception as exc:
            logger.warning("Health chunk lookup failed: %s", exc)

        return {
            "status": "ok",
            "ready": embedder["ready"] and (chunks or 0) > 0,
            "embedder_ready": embedder["ready"],
            "embedder_model": embedder["model"],
            "embedder_error": embedder["error"],
            "chunks": chunks or 0,
            "redis_enabled": redis_cache.redis_url() is not None,
            "llm_provider": llm.provider,
            "llm_model": llm.model_name,
            "embedding_model": embedding_model,
            "mock_mode": llm.provider == "mock",
        }

    @app.get("/api/patterns")
    def list_patterns() -> list[dict]:
        return patterns_payload()

    @app.post("/api/chat")
    def chat(req: ChatRequest) -> Any:
        if not req.messages:
            raise HTTPException(status_code=400, detail="messages required")

        user_messages = [m for m in req.messages if m.role == "user"]
        if not user_messages:
            raise HTTPException(status_code=400, detail="at least one user message required")

        query = user_messages[-1].content
        try:
            context, sources = _retrieve_context(
                query, pattern_number=req.pattern_number, top_k=req.top_k
            )
        except RuntimeError as exc:
            raise HTTPException(status_code=503, detail=str(exc)) from exc

        system = _build_system_prompt(context)

        llm_messages: list[dict[str, str]] = [{"role": "system", "content": system}]
        for msg in req.messages:
            if msg.role in ("user", "assistant"):
                llm_messages.append({"role": msg.role, "content": msg.content})

        llm = get_chat_llm()

        try:
            if req.stream:
                result = llm.chat(llm_messages, stream=True)
                if isinstance(result, str):
                    return {"message": result, "sources": sources}

                def event_stream() -> Iterator[str]:
                    try:
                        for token in result:
                            payload = json.dumps({"token": token})
                            yield f"data: {payload}\n\n"
                        yield f"data: {json.dumps({'done': True, 'sources': sources})}\n\n"
                    except Exception as exc:
                        payload = json.dumps(
                            {
                                "error": f"LLM request failed ({llm.provider}/{llm.model_name}): {exc}"
                            }
                        )
                        yield f"data: {payload}\n\n"

                return StreamingResponse(event_stream(), media_type="text/event-stream")

            answer = llm.chat(llm_messages, stream=False)
            if not isinstance(answer, str):
                answer = "".join(answer)
            return {"message": answer, "sources": sources}
        except Exception as exc:
            raise HTTPException(
                status_code=502,
                detail=f"LLM request failed ({llm.provider}/{llm.model_name}): {exc}",
            ) from exc

    if STATIC_DIR.is_dir():
        app.mount("/assets", StaticFiles(directory=STATIC_DIR), name="assets")

        @app.get("/")
        def index() -> FileResponse:
            return FileResponse(STATIC_DIR / "index.html")

    return app


def _build_system_prompt(context: str) -> str:
    """Join prompt parts without str.format so code chunks can contain braces."""
    return SYSTEM_PROMPT_HEAD + (context or "_No chunks retrieved._") + SYSTEM_PROMPT_TAIL


def _retrieve_context(
    query: str, *, pattern_number: int | None, top_k: int
) -> tuple[str, list[dict[str, str]]]:
    store = get_store()
    if store.count() == 0:
        return "", []

    version = corpus_version(store)
    normalized = redis_cache.normalize_query(query)
    cached_ids = redis_cache.get_cached_query_results(
        normalized, pattern_number=pattern_number, top_k=top_k, corpus_version=version
    )
    if cached_ids is not None:
        chunks = store.query_by_ids(cached_ids)
        for chunk in chunks:
            chunk.score = 1.0
    else:
        query_vec = redis_cache.get_cached_query_embedding(normalized)
        if query_vec is None:
            embedder = get_embedder()
            query_vec = embedder.embed([query])[0]
            redis_cache.cache_query_embedding(normalized, query_vec)
        chunks = store.query(query_vec, top_k=top_k, pattern_number=pattern_number)
        redis_cache.cache_query_results(
            normalized,
            pattern_number=pattern_number,
            top_k=top_k,
            chunk_ids=[chunk.id for chunk in chunks],
            corpus_version=version,
        )

    parts: list[str] = []
    sources: list[dict[str, str]] = []
    seen: set[str] = set()
    for chunk in chunks:
        meta = chunk.metadata
        source_file = meta.get("source_file", "?")
        if source_file not in seen:
            seen.add(source_file)
            sources.append(
                {
                    "source_file": source_file,
                    "pattern_number": meta.get("pattern_number"),
                    "pattern_name": meta.get("pattern_name"),
                    "content_type": meta.get("content_type"),
                }
            )
        header = f"[{meta.get('content_type', '?')} | {source_file}"
        if meta.get("pattern_number"):
            header += f" | Pattern {meta['pattern_number']:02d}: {meta.get('pattern_name', '')}"
        header += f" | score={chunk.score:.3f}]"
        parts.append(f"{header}\n{chunk.text}")
    return "\n\n---\n\n".join(parts), sources


app = create_app()


def main() -> None:
    import uvicorn

    port = int(os.getenv("PORT", "8080"))
    uvicorn.run("chat.main:app", host="0.0.0.0", port=port, reload=False)


if __name__ == "__main__":
    main()
