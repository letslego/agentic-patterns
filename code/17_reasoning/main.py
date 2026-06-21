"""Pattern 17: Reasoning Techniques — structured trace until final answer."""

from __future__ import annotations

from agentic_patterns.common import get_llm


def traced_reasoning(question: str, *, max_steps: int = 4) -> str:
    llm = get_llm()
    scratchpad = question
    for _ in range(max_steps):
        trace = llm.complete(
            f"Produce a reasoning trace for:\n{scratchpad}",
            system="Use Thought/Action/Observation lines; end with Final Answer.",
        )
        if "final answer" in trace.lower():
            return trace
        scratchpad += "\n" + trace
    return llm.complete(f"Final Answer for: {question}\nNotes:\n{scratchpad}")


if __name__ == "__main__":
    print(traced_reasoning("Should we use embedding routing or rule routing for FAQs?"))
