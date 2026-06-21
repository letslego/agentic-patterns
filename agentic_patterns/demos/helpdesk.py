"""IT helpdesk routing demo."""

from __future__ import annotations

from agentic_patterns.kernel import Router


def handle_password_reset(ticket: str) -> str:
    return f"[PasswordReset] Sent MFA reset link for: {ticket}"


def handle_software_install(ticket: str) -> str:
    return f"[SoftwareInstall] Queued package deployment for: {ticket}"


def handle_general_support(ticket: str) -> str:
    return f"[GeneralSupport] Created follow-up task for: {ticket}"


def build_helpdesk_router() -> Router:
    return Router(
        routes={
            "password_reset": handle_password_reset,
            "software_install": handle_software_install,
            "general_support": handle_general_support,
        },
        default="general_support",
        system="Reply with exactly one route label.",
    )
