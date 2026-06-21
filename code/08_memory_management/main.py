"""Pattern 08: Memory Management — short-term buffer plus long-term store."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field

from agentic_patterns.common import get_llm


@dataclass
class MemoryStore:
    short_term: deque[str] = field(default_factory=lambda: deque(maxlen=8))
    long_term: dict[str, str] = field(default_factory=dict)

    def remember(self, key: str, value: str, *, persistent: bool = False) -> None:
        self.short_term.append(f"{key}: {value}")
        if persistent:
            self.long_term[key] = value

    def recall(self, query: str) -> str:
        context = "\n".join(self.short_term)
        if query in self.long_term:
            context += f"\nlong_term[{query}]={self.long_term[query]}"
        llm = get_llm()
        return llm.complete(f"Using memory context:\n{context}\n\nAnswer: {query}")


if __name__ == "__main__":
    mem = MemoryStore()
    mem.remember("user_name", "Alex", persistent=True)
    mem.remember("topic", "agent memory patterns")
    print(mem.recall("What topic are we discussing and who is the user?"))
