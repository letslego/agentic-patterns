"""FastAPI backend for the pattern chat app."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Iterator

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from chat.embeddings import get_embedder
from chat.llm import get_chat_llm
from chat.patterns import patterns_payload
from chat.rag import get_store

STATIC_DIR = Path(__file__).parent / "static"

SYSTEM_PROMPT_HEAD = """You are an expert on the 21 agentic design patterns from the agentic-patterns repository.

Rules:
- Always cite pattern numbers and names when relevant (e.g. "Pattern 03: Parallelization").
- Include runnable Python code recipes adapted from the repository when the user asks how to implement something.
- Reference actual repo paths: code lives in `code/NN_name/main.py`, shared primitives in `agentic_patterns/`, guides in `docs/`.
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


def create_app() -> FastAPI:
    app = FastAPI(title="Agentic Patterns Chat", version="0.1.0")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/api/health")
    def health() -> dict[str, Any]:
        store = get_store()
        llm = get_chat_llm()
        return {
            "status": "ok",
            "chunks": store.count(),
            "llm_provider": llm.provider,
            "llm_model": llm.model_name,
            "embedding_model": store.get_meta("embedding_model"),
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
        context, sources = _retrieve_context(query, pattern_number=req.pattern_number, top_k=req.top_k)
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
                    for token in result:
                        payload = json.dumps({"token": token})
                        yield f"data: {payload}\n\n"
                    yield f"data: {json.dumps({'done': True, 'sources': sources})}\n\n"

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
    embedder = get_embedder()
    query_vec = embedder.embed([query])[0]
    chunks = store.query(query_vec, top_k=top_k, pattern_number=pattern_number)
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
