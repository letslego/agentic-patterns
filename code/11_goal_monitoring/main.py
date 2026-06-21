"""Pattern 11: Goal Setting and Monitoring — track progress against targets."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Goal:
    name: str
    target: float
    current: float = 0.0
    unit: str = ""

    @property
    def progress(self) -> float:
        if self.target == 0:
            return 1.0
        return min(self.current / self.target, 1.0)

    @property
    def met(self) -> bool:
        return self.current >= self.target


@dataclass
class GoalMonitor:
    goals: list[Goal] = field(default_factory=list)

    def add_goal(self, goal: Goal) -> None:
        self.goals.append(goal)

    def update(self, name: str, value: float) -> None:
        for goal in self.goals:
            if goal.name == name:
                goal.current = value
                return
        raise KeyError(name)

    def status_report(self) -> str:
        lines = ["Goal Status"]
        for goal in self.goals:
            pct = round(goal.progress * 100, 1)
            flag = "OK" if goal.met else "IN_PROGRESS"
            lines.append(
                f"- {goal.name}: {goal.current}/{goal.target}{goal.unit} ({pct}%) [{flag}]"
            )
        return "\n".join(lines)


if __name__ == "__main__":
    monitor = GoalMonitor()
    monitor.add_goal(Goal("resolved_tickets", target=50, unit=" tickets"))
    monitor.add_goal(Goal("avg_latency_ms", target=800, unit=" ms"))
    monitor.update("resolved_tickets", 37)
    monitor.update("avg_latency_ms", 640)
    print(monitor.status_report())
