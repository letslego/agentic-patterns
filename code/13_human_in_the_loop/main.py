"""Pattern 13: Human-in-the-Loop — approval gate before risky actions."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable


@dataclass
class ApprovalRequest:
    action: str
    details: str


def human_in_the_loop(
    proposal: ApprovalRequest,
    approve: Callable[[ApprovalRequest], bool],
    execute: Callable[[ApprovalRequest], str],
) -> str:
    if approve(proposal):
        return execute(proposal)
    return f"Action blocked by human reviewer: {proposal.action}"


if __name__ == "__main__":
    request = ApprovalRequest(
        action="send_bulk_email",
        details="Send release notes to 12,000 users",
    )

    def auto_approve(req: ApprovalRequest) -> bool:
        return "bulk" not in req.action

    def send(req: ApprovalRequest) -> str:
        return f"Executed {req.action}: {req.details}"

    print(human_in_the_loop(request, auto_approve, send))
