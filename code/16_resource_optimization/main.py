"""Pattern 16: Resource-Aware Optimization — budget tokens, time, and cost."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ResourceBudget:
    max_tokens: int
    max_latency_ms: int
    max_cost_usd: float

    tokens_used: int = 0
    latency_ms: int = 0
    cost_usd: float = 0.0

    def can_spend(self, *, tokens: int, latency_ms: int, cost_usd: float) -> bool:
        return (
            self.tokens_used + tokens <= self.max_tokens
            and self.latency_ms + latency_ms <= self.max_latency_ms
            and self.cost_usd + cost_usd <= self.max_cost_usd
        )

    def spend(self, *, tokens: int, latency_ms: int, cost_usd: float) -> None:
        if not self.can_spend(tokens=tokens, latency_ms=latency_ms, cost_usd=cost_usd):
            raise RuntimeError("budget exceeded")
        self.tokens_used += tokens
        self.latency_ms += latency_ms
        self.cost_usd += cost_usd


def choose_model(task_complexity: str, budget: ResourceBudget) -> str:
    if task_complexity == "high" and budget.can_spend(tokens=4000, latency_ms=3000, cost_usd=0.08):
        return "large-model"
    if budget.can_spend(tokens=1200, latency_ms=900, cost_usd=0.01):
        return "small-model"
    return "cached-response"


if __name__ == "__main__":
    budget = ResourceBudget(max_tokens=5000, max_latency_ms=4000, max_cost_usd=0.10)
    print(choose_model("high", budget))
    budget.spend(tokens=4000, latency_ms=2500, cost_usd=0.07)
    print(choose_model("low", budget))
