"""Pattern 06: Planning — database migration milestone tracker."""

from __future__ import annotations

from dataclasses import dataclass

from agentic_patterns.common import get_llm


@dataclass
class Milestone:
    order: int
    title: str
    done: bool = False


def build_migration_plan(scope: str) -> list[Milestone]:
    llm = get_llm()
    raw = llm.complete(
        f"Create a numbered migration plan for: {scope}",
        system="Return numbered milestones only.",
    )
    milestones: list[Milestone] = []
    for line in raw.splitlines():
        line = line.strip()
        if not line or not line[0].isdigit():
            continue
        title = line.split(maxsplit=1)[-1].lstrip(".) ")
        milestones.append(Milestone(order=len(milestones) + 1, title=title))
    return milestones or [Milestone(1, raw)]


def execute_milestones(steps: list[Milestone]) -> list[Milestone]:
    llm = get_llm()
    for step in steps:
        llm.complete(f"Describe validation checks for migration step: {step.title}")
        step.done = True
    return steps


if __name__ == "__main__":
    plan = build_migration_plan("Move orders DB from Postgres 12 to 16")
    for step in execute_milestones(plan):
        print(f"[{'x' if step.done else ' '}] {step.order}. {step.title}")
