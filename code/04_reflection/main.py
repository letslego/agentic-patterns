"""Pattern 04: Reflection — generate, critique, and revise."""

from __future__ import annotations

from agentic_patterns.common import get_llm


def draft(task: str) -> str:
    llm = get_llm()
    return llm.complete(f"Write a short plan for: {task}")


def critique(text: str) -> str:
    llm = get_llm()
    return llm.complete(
        f"Critique this draft and list concrete improvements:\n\n{text}",
        system="Be specific and actionable.",
    )


def revise(text: str, feedback: str) -> str:
    llm = get_llm()
    return llm.complete(
        f"Revise the draft using this feedback.\n\nDraft:\n{text}\n\nFeedback:\n{feedback}"
    )


def reflect_loop(task: str, *, rounds: int = 2) -> str:
    current = draft(task)
    for _ in range(rounds):
        feedback = critique(current)
        current = revise(current, feedback)
    return current


if __name__ == "__main__":
    print(reflect_loop("Launch a beta program for a developer tool"))
