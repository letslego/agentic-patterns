#!/usr/bin/env python3
"""Run incident-response crew through LangGraph sequential nodes."""

from __future__ import annotations

from agentic_patterns.adapters.langgraph_bridge import compile_crew_graph
from agentic_patterns.kernel import Crew, Specialist


def main() -> None:
    crew = Crew(
        members=[
            Specialist("SRE", "triage production alerts and identify blast radius"),
            Specialist("Comms", "draft customer-facing incident updates"),
            Specialist("Fix", "propose and validate remediation steps"),
        ]
    )
    graph = compile_crew_graph(crew)
    state = graph.invoke(
        {
            "mission": "Checkout API error rate exceeded 4% for 6 minutes",
            "prior": "",
            "transcript": [],
        }
    )
    for role, text in state.get("transcript", []):
        print(f"\n[{role}]\n{text}")


if __name__ == "__main__":
    main()
