"""Pattern 02: Routing — IT helpdesk intent dispatch."""

from __future__ import annotations

from agentic_patterns.common import get_llm
from agentic_patterns.kernel import Router


def handle_password_reset(ticket: str) -> str:
    return f"[PasswordReset] Sent MFA reset link for: {ticket}"


def handle_software_install(ticket: str) -> str:
    return f"[SoftwareInstall] Queued package deployment for: {ticket}"


def handle_general_support(ticket: str) -> str:
    return f"[GeneralSupport] Created follow-up task for: {ticket}"


helpdesk_router = Router(
    routes={
        "password_reset": handle_password_reset,
        "software_install": handle_software_install,
        "general_support": handle_general_support,
    },
    default="general_support",
    system="Reply with exactly one route label.",
)


if __name__ == "__main__":
    print(helpdesk_router.dispatch("I'm locked out after password expiry."))
    print(helpdesk_router.dispatch("Please install Figma on my laptop."))
