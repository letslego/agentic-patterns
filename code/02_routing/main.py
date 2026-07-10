"""Pattern 02: Routing — classify questions and dispatch to handlers."""

from __future__ import annotations

from agentic_patterns.kernel import Router


def handle_code_request(question: str) -> str:
    return f"[Code] Runnable example for: {question}"


def handle_concept_request(question: str) -> str:
    return f"[Concept] Definition and when to use: {question}"


def handle_compare_request(question: str) -> str:
    return f"[Compare] Trade-offs for: {question}"


pattern_router = Router(
    routes={
        "code_example": handle_code_request,
        "concept_explanation": handle_concept_request,
        "pattern_comparison": handle_compare_request,
    },
    default="concept_explanation",
    system="Reply with exactly one route label.",
)


if __name__ == "__main__":
    print(pattern_router.dispatch("Show me code for parallel LLM calls."))
    print(pattern_router.dispatch("What is routing in agentic design?"))
    print(pattern_router.dispatch("Routing vs prompt chaining — when to use each?"))
