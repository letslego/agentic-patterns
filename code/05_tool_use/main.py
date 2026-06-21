"""Pattern 05: Tool Use — LLM selects and invokes external tools."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Callable

from agentic_patterns.common import get_llm


@dataclass
class Tool:
    name: str
    description: str
    fn: Callable[..., Any]

    def schema(self) -> dict[str, Any]:
        return {"name": self.name, "description": self.description}


TOOLS: dict[str, Tool] = {
    "search": Tool(
        "search",
        "Search the knowledge base",
        lambda query: f"Results for '{query}': doc1, doc2",
    ),
    "calculator": Tool(
        "calculator",
        "Evaluate a math expression",
        lambda expression: str(eval(expression, {"__builtins__": {}}, {})),
    ),
}


def choose_tool(question: str) -> tuple[str, dict[str, Any]]:
    llm = get_llm()
    catalog = json.dumps([t.schema() for t in TOOLS.values()])
    raw = llm.complete(
        f"Pick a tool and JSON args for: {question}\nAvailable tools: {catalog}\n"
        "Respond as JSON: {\"tool\": \"name\", \"args\": {{}}}"
    )
    start, end = raw.find("{"), raw.rfind("}")
    if start >= 0:
        payload = json.loads(raw[start : end + 1])
        tool = payload.get("tool", "search")
        return tool, payload.get("args", {})
    if any(op in question for op in "+-*/"):
        expr = question.split("?", 1)[0]
        for prefix in ("What is ", "Calculate "):
            expr = expr.replace(prefix, "")
        return "calculator", {"expression": expr.strip()}
    return "search", {"query": question}


def run_with_tools(question: str) -> str:
    tool_name, args = choose_tool(question)
    tool = TOOLS.get(tool_name, TOOLS["search"])
    result = tool.fn(**args) if args else tool.fn(question)
    llm = get_llm()
    return llm.complete(f"Question: {question}\nTool result: {result}\nWrite the final answer.")


if __name__ == "__main__":
    print(run_with_tools("What is 12 * (4 + 3) ?"))
