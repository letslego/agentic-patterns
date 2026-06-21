"""Pattern 21: Exploration and Discovery — generate and test hypotheses."""

from __future__ import annotations

from dataclasses import dataclass

from agentic_patterns.common import get_llm


@dataclass
class Hypothesis:
    statement: str
    evidence: str
    confidence: float


def propose_hypotheses(problem: str, *, n: int = 3) -> list[Hypothesis]:
    llm = get_llm()
    raw = llm.complete(
        f"Propose {n} hypotheses for: {problem}. Number each hypothesis.",
        system="Be concise.",
    )
    lines = [line.strip(" 1234567890.)") for line in raw.splitlines() if line.strip()]
    return [Hypothesis(statement=line, evidence="", confidence=0.5) for line in lines[:n]]


def explore(problem: str) -> Hypothesis | None:
    candidates = propose_hypotheses(problem)
    llm = get_llm()
    best: Hypothesis | None = None
    for candidate in candidates:
        evidence = llm.complete(
            f"Gather supporting/contradicting evidence for hypothesis: {candidate.statement}"
        )
        score_raw = llm.complete(
            f"Score confidence 0-1 for hypothesis given evidence.\n"
            f"Hypothesis: {candidate.statement}\nEvidence: {evidence}\nNumber only."
        )
        try:
            confidence = float(score_raw.strip().split()[0])
        except ValueError:
            confidence = 0.5
        candidate.evidence = evidence
        candidate.confidence = max(0.0, min(confidence, 1.0))
        if best is None or candidate.confidence > best.confidence:
            best = candidate
    return best


if __name__ == "__main__":
    winner = explore("Why did support ticket volume spike last week?")
    if winner:
        print(winner.statement)
        print(f"confidence={winner.confidence}")
        print(winner.evidence[:200])
