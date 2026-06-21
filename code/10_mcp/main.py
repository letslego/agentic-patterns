"""Pattern 10: MCP — capability host with typed request envelope."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable


@dataclass(frozen=True)
class Capability:
    kind: str
    name: str
    handler: Callable[[dict[str, Any]], str]


class CapabilityHost:
    def __init__(self) -> None:
        self._caps: dict[tuple[str, str], Capability] = {}

    def register(self, cap: Capability) -> None:
        self._caps[(cap.kind, cap.name)] = cap

    def invoke(self, kind: str, name: str, params: dict[str, Any]) -> str:
        cap = self._caps[(kind, name)]
        return cap.handler(params)


class CapabilityClient:
    def __init__(self, host: CapabilityHost) -> None:
        self.host = host

    def read(self, uri: str) -> str:
        return self.host.invoke("resource", uri, {})

    def tool(self, name: str, **params: Any) -> str:
        return self.host.invoke("tool", name, params)


if __name__ == "__main__":
    host = CapabilityHost()
    host.register(
        Capability("resource", "policy/handbook", lambda _: "Handbook section 4.2: travel policy")
    )
    host.register(
        Capability("tool", "expense_lookup", lambda p: f"Trip {p['trip_id']} total $842")
    )
    client = CapabilityClient(host)
    print(client.read("policy/handbook"))
    print(client.tool("expense_lookup", trip_id="T-991"))
