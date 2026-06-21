#!/usr/bin/env python3
"""Run helpdesk routing through a LangGraph state machine."""

from __future__ import annotations

from agentic_patterns.adapters.langgraph_bridge import compile_router_graph
from agentic_patterns.demos.helpdesk import build_helpdesk_router


def main() -> None:
    graph = compile_router_graph(build_helpdesk_router())
    for ticket in (
        "I'm locked out after password expiry.",
        "Please install Figma on my laptop.",
    ):
        state = graph.invoke({"message": ticket})
        print(state.get("response"))


if __name__ == "__main__":
    main()
