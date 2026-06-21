"""Pattern 06: Planning — decompose goals into executable steps."""

from __future__ import annotations

from dataclasses import dataclass

from agentic_patterns.common import get_llm


@dataclass
class PlanStep:
    id: int
    description: str
    status: str = "pending"


def create_plan(goal: str) -> list[PlanStep]:
    llm = get_llm()
    raw = llm.complete(
        f"Break this goal into 3-5 numbered steps:\n{goal}",
        system="Return numbered steps only.",
    )
    steps: list[PlanStep] = []
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        if line[0].isdigit():
            desc = line.split(maxsplit=1)[-1].lstrip(".) ")
            steps.append(PlanStep(id=len(steps) + 1, description=desc))
    return steps or [PlanStep(1, raw)]


def execute_plan(steps: list[PlanStep]) -> list[PlanStep]:
    llm = get_llm()
    for step in steps:
        llm.complete(f"Execute plan step: {step.description}")
        step.status = "done"
    return steps


if __name__ == "__main__":
    plan = create_plan("Ship a RAG-powered support bot in two weeks")
    for step in execute_plan(plan):
        print(f"[{step.status}] {step.id}. {step.description}")
