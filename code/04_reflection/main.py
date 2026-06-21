"""Pattern 04: Reflection — press release draft/review loop."""

from __future__ import annotations

from agentic_patterns.demos.press_release import (
    draft_release,
    editorial_review,
    revise_release,
)


def reflective_release(topic: str, *, rounds: int = 2) -> str:
    current = draft_release(topic)
    for _ in range(rounds):
        notes = editorial_review(current)
        current = revise_release(current, notes)
    return current


if __name__ == "__main__":
    print(reflective_release("Orion SDK for edge inference"))
