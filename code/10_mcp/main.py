"""Pattern 10: Model Context Protocol (MCP) — tool/resource server sketch."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Callable


@dataclass
class MCPResource:
    uri: str
    reader: Callable[[], str]


@dataclass
class MCPTool:
    name: str
    handler: Callable[[dict[str, Any]], str]


class MCPServer:
    def __init__(self) -> None:
        self.resources: dict[str, MCPResource] = {}
        self.tools: dict[str, MCPTool] = {}

    def register_resource(self, resource: MCPResource) -> None:
        self.resources[resource.uri] = resource

    def register_tool(self, tool: MCPTool) -> None:
        self.tools[tool.name] = tool

    def handle(self, request: dict[str, Any]) -> dict[str, Any]:
        kind = request.get("method")
        if kind == "resources/read":
            uri = request["params"]["uri"]
            return {"content": self.resources[uri].reader()}
        if kind == "tools/call":
            name = request["params"]["name"]
            args = request["params"].get("arguments", {})
            return {"result": self.tools[name].handler(args)}
        return {"error": f"unsupported method: {kind}"}


class MCPClient:
    def __init__(self, server: MCPServer) -> None:
        self.server = server

    def read_resource(self, uri: str) -> str:
        payload = self.server.handle({"method": "resources/read", "params": {"uri": uri}})
        return payload["content"]

    def call_tool(self, name: str, arguments: dict[str, Any] | None = None) -> str:
        payload = self.server.handle(
            {"method": "tools/call", "params": {"name": name, "arguments": arguments or {}}}
        )
        return payload["result"]


if __name__ == "__main__":
    server = MCPServer()
    server.register_resource(MCPResource("file:///docs/agentic.md", lambda: "Agentic patterns guide"))
    server.register_tool(MCPTool("grep_docs", lambda args: f"matches for {args.get('query')}"))
    client = MCPClient(server)
    print(client.read_resource("file:///docs/agentic.md"))
    print(client.call_tool("grep_docs", {"query": "routing"}))
