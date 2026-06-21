"""Press-release reflection demo functions."""

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
