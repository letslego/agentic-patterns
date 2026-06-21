"""Pattern 14: Knowledge Retrieval (RAG) — retrieve then generate."""

from __future__ import annotations

from dataclasses import dataclass

from agentic_patterns.common import get_llm


@dataclass
class Document:
    id: str
    text: str


CORPUS = [
    Document("d1", "Prompt chaining splits complex tasks into sequential LLM steps."),
    Document("d2", "Routing sends user requests to specialized handlers."),
    Document("d3", "RAG combines retrieval with generation for grounded answers."),
]


def retrieve(query: str, k: int = 2) -> list[Document]:
    terms = set(query.lower().split())
    scored = sorted(
        CORPUS,
        key=lambda doc: len(terms.intersection(doc.text.lower().split())),
        reverse=True,
    )
    return scored[:k]


def rag_answer(query: str) -> str:
    docs = retrieve(query)
    context = "\n".join(f"[{d.id}] {d.text}" for d in docs)
    llm = get_llm()
    return llm.complete(
        f"Answer using only this context.\n\nContext:\n{context}\n\nQuestion: {query}"
    )


if __name__ == "__main__":
    print(rag_answer("How does RAG help agents stay grounded?"))
