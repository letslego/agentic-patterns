"""Pattern 07: Multi-Agent Collaboration — incident response crew."""

from __future__ import annotations

from agentic_patterns.kernel import Crew, Specialist


def run_incident_response(alert: str) -> list[tuple[str, str]]:
    crew = Crew(
        members=[
            Specialist("SRE", "triage production alerts and identify blast radius"),
            Specialist("Comms", "draft customer-facing incident updates"),
            Specialist("Fix", "propose and validate remediation steps"),
        ]
    )
    return crew.execute(alert)


if __name__ == "__main__":
    transcript = run_incident_response("Checkout API error rate exceeded 4% for 6 minutes")
    for role, output in transcript:
        print(f"\n[{role}]\n{output}")
