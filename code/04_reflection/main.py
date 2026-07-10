"""Pattern 04: Reflection — draft, critique, and revise in a loop."""

from __future__ import annotations

from agentic_patterns.common import get_llm


def draft_explanation(topic: str) -> str:
    llm = get_llm()
    return llm.complete(
        f"Draft a one-paragraph explanation of: {topic}",
        system="Be concise and accurate.",
    )


def critique_draft(draft: str) -> str:
    llm = get_llm()
    return llm.complete(
        f"Critique this explanation for clarity and completeness:\n{draft}",
        system="List concrete improvements only.",
    )


def revise_draft(draft: str, feedback: str) -> str:
    llm = get_llm()
    return llm.complete(
        f"Revise using feedback.\nDraft:\n{draft}\nFeedback:\n{feedback}",
        system="Return the improved paragraph.",
    )


def reflective_explain(topic: str, *, rounds: int = 2) -> str:
    current = draft_explanation(topic)
    for _ in range(rounds):
        notes = critique_draft(current)
        current = revise_draft(current, notes)
    return current


if __name__ == "__main__":
    print(reflective_explain("reflection pattern for self-correcting agents"))
