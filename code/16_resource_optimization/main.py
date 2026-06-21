"""Pattern 16: Resource-Aware Optimization — tiered model picker."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class SpendLedger:
    token_budget: int
    cost_budget_usd: float
    tokens_used: int = 0
    cost_used: float = 0.0

    def afford(self, tokens: int, cost: float) -> bool:
        return (
            self.tokens_used + tokens <= self.token_budget
            and self.cost_used + cost <= self.cost_budget_usd
        )

    def charge(self, tokens: int, cost: float) -> None:
        if not self.afford(tokens, cost):
            raise RuntimeError("budget exceeded")
        self.tokens_used += tokens
        self.cost_used += cost


def select_tier(task: str, ledger: SpendLedger) -> str:
    complex_task = any(word in task.lower() for word in ("architecture", "security", "migration"))
    if complex_task and ledger.afford(3500, 0.06):
        return "tier-a"
    if ledger.afford(900, 0.01):
        return "tier-b"
    return "cached"


if __name__ == "__main__":
    ledger = SpendLedger(token_budget=5000, cost_budget_usd=0.08)
    print(select_tier("Design security architecture review", ledger))
    ledger.charge(3500, 0.06)
    print(select_tier("Summarize meeting notes", ledger))
