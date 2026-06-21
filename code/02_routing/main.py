"""Pattern 02: Routing — IT helpdesk intent dispatch."""

from __future__ import annotations

from agentic_patterns.demos.helpdesk import build_helpdesk_router

helpdesk_router = build_helpdesk_router()


if __name__ == "__main__":
    print(helpdesk_router.dispatch("I'm locked out after password expiry."))
    print(helpdesk_router.dispatch("Please install Figma on my laptop."))
