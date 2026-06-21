"""Pattern 17: Reasoning Techniques — ReAct-style thought/action loop."""

from __future__ import annotations

from agentic_patterns.common import get_llm


def react_loop(question: str, *, max_steps: int = 3) -> str:
    llm = get_llm()
    context = question
    for step in range(max_steps):
        trace = llm.complete(
            f"Use Thought/Action/Observation steps to solve:\n{context}",
            system="Stop with Final Answer when done.",
        )
        if "final answer" in trace.lower():
            return trace
        context += f"\nStep {step + 1}:\n{trace}"
    return llm.complete(f"Provide final answer for: {question}\nContext:\n{context}")


if __name__ == "__main__":
    print(react_loop("Find the best agent pattern for classifying support tickets"))
