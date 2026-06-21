"""Pattern 15: Inter-Agent Communication (A2A) — message bus between agents."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable


@dataclass
class AgentMessage:
    sender: str
    recipient: str
    topic: str
    body: str


@dataclass
class MessageBus:
    subscribers: dict[str, list[Callable[[AgentMessage], None]]] = field(default_factory=dict)

    def subscribe(self, agent_name: str, handler: Callable[[AgentMessage], None]) -> None:
        self.subscribers.setdefault(agent_name, []).append(handler)

    def publish(self, message: AgentMessage) -> None:
        for handler in self.subscribers.get(message.recipient, []):
            handler(message)


if __name__ == "__main__":
    bus = MessageBus()
    inbox: list[str] = []

    def on_message(msg: AgentMessage) -> None:
        inbox.append(f"{msg.sender}->{msg.recipient}: {msg.body}")

    bus.subscribe("planner", on_message)
    bus.publish(
        AgentMessage(
            sender="researcher",
            recipient="planner",
            topic="requirements",
            body="Users need SSO and audit logs.",
        )
    )
    print("\n".join(inbox))
