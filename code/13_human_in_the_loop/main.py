"""Pattern 13: Human-in-the-Loop — policy gate for destructive ops."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Callable


class Risk(str, Enum):
    LOW = "low"
    HIGH = "high"


@dataclass
class ActionProposal:
    name: str
    detail: str
    risk: Risk


def gated_execute(
    proposal: ActionProposal,
    reviewer: Callable[[ActionProposal], bool],
    effect: Callable[[ActionProposal], str],
) -> str:
    if proposal.risk is Risk.HIGH and not reviewer(proposal):
        return f"Denied by reviewer: {proposal.name}"
    return effect(proposal)


if __name__ == "__main__":
    wipe = ActionProposal("drop_staging_db", "DROP DATABASE staging;", Risk.HIGH)

    def strict_reviewer(p: ActionProposal) -> bool:
        return p.name != "drop_staging_db"

    print(
        gated_execute(
            wipe,
            strict_reviewer,
            lambda p: f"Executed {p.name}",
        )
    )
