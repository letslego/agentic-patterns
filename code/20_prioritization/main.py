"""Pattern 20: Prioritization — WSJF-style backlog ordering."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(order=True)
class BacklogItem:
    score: float
    title: str
    cost_of_delay: int
    job_size: int


def wsjf(cost_of_delay: int, job_size: int) -> float:
    return cost_of_delay / max(job_size, 1)


def rank_backlog(items: list[tuple[str, int, int]]) -> list[BacklogItem]:
    ranked = [BacklogItem(wsjf(cod, size), title, cod, size) for title, cod, size in items]
    return sorted(ranked, reverse=True)


if __name__ == "__main__":
    backlog = [
        ("Patch auth bypass", 13, 2),
        ("Refresh marketing site copy", 3, 1),
        ("Migrate logging pipeline", 8, 5),
    ]
    for item in rank_backlog(backlog):
        print(f"{item.score:4.2f} | {item.title} (cod={item.cost_of_delay}, size={item.job_size})")
