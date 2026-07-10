"""Pattern 07: Multi-Agent Collaboration — sequential specialist crew."""

from __future__ import annotations

from agentic_patterns.kernel import Crew, Specialist


def run_pattern_crew(task: str) -> list[tuple[str, str]]:
    crew = Crew(
        members=[
            Specialist("Researcher", "gather facts and references for the task"),
            Specialist("Writer", "draft a clear explanation from prior research"),
            Specialist("Reviewer", "check accuracy and suggest final edits"),
        ]
    )
    return crew.execute(task)


if __name__ == "__main__":
    transcript = run_pattern_crew("Explain Pattern 03: Parallelization with a code sketch")
    for role, output in transcript:
        print(f"\n[{role}]\n{output}")
