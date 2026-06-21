"""Pattern 07: Multi-Agent Collaboration — specialized roles coordinate on a task."""

from __future__ import annotations

from dataclasses import dataclass

from agentic_patterns.common import get_llm


@dataclass
class Agent:
    name: str
    role: str

    def act(self, task: str, context: str = "") -> str:
        llm = get_llm()
        return llm.complete(
            f"You are {self.name}, a {self.role}.\nContext:\n{context}\nTask:\n{task}",
            system=f"Stay in role: {self.role}",
        )


def run_multi_agent(brief: str) -> dict[str, str]:
    pm = Agent("ProjectManager", "coordinator")
    researcher = Agent("Researcher", "market analyst")
    writer = Agent("Writer", "technical writer")

    research = researcher.act(f"Research requirements for: {brief}")
    outline = pm.act("Create an outline from research", context=research)
    draft = writer.act("Draft deliverable from outline", context=outline)
    review = pm.act("Review draft and list gaps", context=draft)
    return {
        "research": research,
        "outline": outline,
        "draft": draft,
        "review": review,
    }


if __name__ == "__main__":
    outputs = run_multi_agent("Launch an internal AI assistant for engineers")
    for role, text in outputs.items():
        print(f"\n=== {role} ===\n{text[:200]}...")
