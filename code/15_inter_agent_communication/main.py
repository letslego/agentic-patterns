"""Pattern 15: Inter-Agent Communication — typed event envelope."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable


@dataclass(frozen=True)
class AgentEvent:
    topic: str
    sender: str
    payload: str
    correlation_id: str


@dataclass
class EventBroker:
    _handlers: dict[str, list[Callable[[AgentEvent], None]]] = field(default_factory=dict)

    def on(self, topic: str, handler: Callable[[AgentEvent], None]) -> None:
        self._handlers.setdefault(topic, []).append(handler)

    def emit(self, event: AgentEvent) -> None:
        for handler in self._handlers.get(event.topic, []):
            handler(event)


if __name__ == "__main__":
    broker = EventBroker()
    audit: list[str] = []

    broker.on("security.alert", lambda e: audit.append(f"{e.sender}: {e.payload}"))

    broker.emit(
        AgentEvent(
            topic="security.alert",
            sender="detector-7",
            payload="Suspicious login from new region",
            correlation_id="c-8842",
        )
    )
    print("\n".join(audit))
