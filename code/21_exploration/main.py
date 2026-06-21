"""Pattern 21: Exploration and Discovery — hypothesis tournament."""

from __future__ import annotations

from dataclasses import dataclass

from agentic_patterns.common import get_llm


@dataclass
class Candidate:
    claim: str
    evidence: str = ""
    confidence: float = 0.0


def brainstorm(problem: str, n: int = 3) -> list[Candidate]:
    llm = get_llm()
    raw = llm.complete(f"List {n} hypotheses for: {problem}", system="Number each line.")
    lines = [ln.strip(" 1234567890.)") for ln in raw.splitlines() if ln.strip()]
    return [Candidate(claim=line) for line in lines[:n]]


def tournament(problem: str) -> Candidate | None:
    llm = get_llm()
    winner: Candidate | None = None
    for cand in brainstorm(problem):
        cand.evidence = llm.complete(f"Collect evidence for hypothesis: {cand.claim}")
        score_raw = llm.complete(
            f"Score confidence 0..1 for hypothesis given evidence.\n"
            f"H: {cand.claim}\nE: {cand.evidence}\nNumber only."
        )
        try:
            cand.confidence = float(score_raw.strip().split()[0])
        except ValueError:
            cand.confidence = 0.5
        if winner is None or cand.confidence > winner.confidence:
            winner = cand
    return winner


if __name__ == "__main__":
    best = tournament("Why did API latency spike after Tuesday deploy?")
    if best:
        print(best.claim)
        print(f"confidence={best.confidence:.2f}")
        print(best.evidence[:180])
