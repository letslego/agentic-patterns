#!/usr/bin/env python3
"""Run press-release reflection as a LangGraph cycle."""

from __future__ import annotations

from agentic_patterns.adapters.langgraph_bridge import compile_reflection_graph
from agentic_patterns.demos.press_release import (
    draft_release,
    editorial_review,
    revise_release,
)


def main() -> None:
    graph = compile_reflection_graph(
        draft_fn=draft_release,
        critique_fn=editorial_review,
        revise_fn=revise_release,
        max_rounds=2,
    )
    state = graph.invoke({"topic": "Orion SDK for edge inference", "max_rounds": 2})
    print(state.get("draft"))


if __name__ == "__main__":
    main()
