"""Pattern 20: Prioritization — rank tasks by urgency and impact."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(order=True)
class Task:
    priority: float
    title: str
    urgency: int
    impact: int


def priority_score(urgency: int, impact: int) -> float:
    return urgency * 0.6 + impact * 0.4


def prioritize(tasks: list[tuple[str, int, int]]) -> list[Task]:
    ranked = [
        Task(priority_score(u, i), title, u, i)
        for title, u, i in tasks
    ]
    return sorted(ranked, reverse=True)


if __name__ == "__main__":
    backlog = [
        ("Fix checkout outage", 10, 10),
        ("Update FAQ copy", 3, 4),
        ("Add dark mode", 5, 6),
        ("Patch SQL injection", 9, 9),
    ]
    for task in prioritize(backlog):
        print(f"{task.priority:.1f} | {task.title} (u={task.urgency}, i={task.impact})")
