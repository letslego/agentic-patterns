"""Pattern 19: Evaluation and Monitoring — rolling quality ledger."""

from __future__ import annotations

from dataclasses import dataclass, field
from statistics import mean

from agentic_patterns.common import get_llm


@dataclass
class QualitySample:
    prompt: str
    answer: str
    score: float


@dataclass
class QualityLedger:
    samples: list[QualitySample] = field(default_factory=list)

    def record(self, prompt: str, answer: str) -> float:
        llm = get_llm()
        raw = llm.complete(
            f"Rate answer quality 0..1.\nPrompt:{prompt}\nAnswer:{answer}\nNumber only."
        )
        try:
            score = float(raw.strip().split()[0])
        except ValueError:
            score = 0.5
        score = max(0.0, min(score, 1.0))
        self.samples.append(QualitySample(prompt, answer, score))
        return score

    def snapshot(self) -> dict[str, float]:
        if not self.samples:
            return {"count": 0.0, "mean_score": 0.0}
        return {"count": float(len(self.samples)), "mean_score": mean(s.score for s in self.samples)}


if __name__ == "__main__":
    ledger = QualityLedger()
    ledger.record("Define routing.", "Routing picks a specialist handler.")
    ledger.record("Define RAG.", "RAG grounds answers in retrieved docs.")
    print(ledger.snapshot())
