"""Pattern 08: Memory Management — episodic buffer + fact vault."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field

from agentic_patterns.common import get_llm


@dataclass
class EpisodicMemory:
    window: deque[str] = field(default_factory=lambda: deque(maxlen=6))
    fact_vault: dict[str, str] = field(default_factory=dict)

    def observe(self, event: str) -> None:
        self.window.append(event)

    def store_fact(self, key: str, value: str) -> None:
        self.fact_vault[key] = value

    def answer(self, question: str) -> str:
        llm = get_llm()
        episodic = "\n".join(self.window)
        facts = "\n".join(f"{k}={v}" for k, v in self.fact_vault.items())
        return llm.complete(
            f"Episodic log:\n{episodic}\n\nFacts:\n{facts}\n\nQuestion: {question}"
        )


if __name__ == "__main__":
    memory = EpisodicMemory()
    memory.store_fact("session_id", "demo-42")
    memory.store_fact("focus_pattern", "08_memory_management")
    memory.observe("User asked how episodic memory differs from long-term facts.")
    memory.observe("User wants a minimal runnable example.")
    print(memory.answer("What pattern are we discussing and what did I ask?"))
