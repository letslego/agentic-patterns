"""Pattern 19: Evaluation and Monitoring — score agent outputs."""

from __future__ import annotations

from dataclasses import dataclass, field
from statistics import mean

from agentic_patterns.common import get_llm


@dataclass
class EvalRecord:
    prompt: str
    output: str
    score: float


@dataclass
class EvalMonitor:
    records: list[EvalRecord] = field(default_factory=list)

    def score(self, prompt: str, output: str) -> float:
        llm = get_llm()
        raw = llm.complete(
            f"Rate answer quality from 0 to 1.\nPrompt: {prompt}\nAnswer: {output}\nReturn number only."
        )
        try:
            value = float(raw.strip().split()[0])
        except ValueError:
            value = 0.5
        record = EvalRecord(prompt, output, max(0.0, min(value, 1.0)))
        self.records.append(record)
        return record.score

    def summary(self) -> dict[str, float]:
        if not self.records:
            return {"count": 0, "avg_score": 0.0}
        return {
            "count": float(len(self.records)),
            "avg_score": mean(r.score for r in self.records),
        }


if __name__ == "__main__":
    monitor = EvalMonitor()
    monitor.score("What is prompt chaining?", "It splits tasks into sequential prompts.")
    monitor.score("What is routing?", "It classifies requests to specialists.")
    print(monitor.summary())
