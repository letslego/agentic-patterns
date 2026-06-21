"""Pattern 04: Reflection — press release draft/review loop."""

from __future__ import annotations

from agentic_patterns.common import get_llm


def draft_release(topic: str) -> str:
    llm = get_llm()
    return llm.complete(
        f"Draft a one-sentence press release about: {topic}",
        system="Be factual.",
    )


def editorial_review(draft: str) -> str:
    llm = get_llm()
    return llm.complete(
        f"Provide editorial review for this release:\n{draft}",
        system="List concrete fixes only.",
    )


def revise_release(draft: str, feedback: str) -> str:
    llm = get_llm()
    return llm.complete(
        f"Revise release using feedback.\nDraft:\n{draft}\nFeedback:\n{feedback}",
        system="Return final release sentence.",
    )


def reflective_release(topic: str, *, rounds: int = 2) -> str:
    current = draft_release(topic)
    for _ in range(rounds):
        notes = editorial_review(current)
        current = revise_release(current, notes)
    return current


if __name__ == "__main__":
    print(reflective_release("Orion SDK for edge inference"))
