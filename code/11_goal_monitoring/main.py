"""Pattern 11: Goal Setting and Monitoring — SLA dashboard."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class SLA:
    metric: str
    target: float
    observed: float = 0.0
    comparator: str = "lte"  # lte => observed must be <= target

    @property
    def satisfied(self) -> bool:
        if self.comparator == "lte":
            return self.observed <= self.target
        return self.observed >= self.target


@dataclass
class SLADashboard:
    slas: list[SLA] = field(default_factory=list)

    def track(self, metric: str, value: float) -> None:
        for sla in self.slas:
            if sla.metric == metric:
                sla.observed = value
                return
        raise KeyError(metric)

    def report(self) -> str:
        lines = ["SLA dashboard"]
        for sla in self.slas:
            status = "PASS" if sla.satisfied else "FAIL"
            lines.append(
                f"- {sla.metric}: observed={sla.observed} target={sla.target} [{status}]"
            )
        return "\n".join(lines)


if __name__ == "__main__":
    board = SLADashboard(
        slas=[
            SLA("p95_latency_ms", target=500),
            SLA("successful_rollouts", target=3, comparator="gte"),
        ]
    )
    board.track("p95_latency_ms", 430)
    board.track("successful_rollouts", 4)
    print(board.report())
