"""Pattern 14: RAG — policy handbook retrieval."""

from __future__ import annotations

from dataclasses import dataclass

from agentic_patterns.common import get_llm


@dataclass(frozen=True)
class HandbookSection:
    section_id: str
    body: str


HANDBOOK = [
    HandbookSection("P-01", "Expense reports require itemized receipts over $25."),
    HandbookSection("P-02", "Remote work is allowed up to two days per week."),
    HandbookSection("P-03", "Customer data must be redacted in support tickets."),
]


def retrieve_sections(query: str, k: int = 2) -> list[HandbookSection]:
    tokens = set(query.lower().split())
    ranked = sorted(
        HANDBOOK,
        key=lambda s: len(tokens.intersection(s.body.lower().split())),
        reverse=True,
    )
    return ranked[:k]


def grounded_policy_answer(question: str) -> str:
    sections = retrieve_sections(question)
    context = "\n".join(f"[{s.section_id}] {s.body}" for s in sections)
    llm = get_llm()
    return llm.complete(
        f"Answer using handbook excerpts only.\n\n{context}\n\nQuestion: {question}"
    )


if __name__ == "__main__":
    print(grounded_policy_answer("How many remote days are allowed?"))
