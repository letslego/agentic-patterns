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
        Capability(
            "resource",
            "patterns/03-parallelization",
            lambda _: "Parallelization runs independent LLM calls concurrently, then merges results.",
        )
    )
    host.register(
        Capability(
            "tool",
            "lookup_pattern",
            lambda p: f"Pattern {p['number']:02d}: see code/{p['number']:02d}_*/main.py",
        )
    )
    client = CapabilityClient(host)
    print(client.read("patterns/03-parallelization"))
    print(client.tool("lookup_pattern", number=14))
