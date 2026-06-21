"""Pattern 05: Tool Use — travel assistant with explicit tool manifest."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Callable

from agentic_patterns.common import extract_json, get_llm


@dataclass(frozen=True)
class TravelTool:
    name: str
    description: str
    invoke: Callable[[dict[str, Any]], str]


MANIFEST: dict[str, TravelTool] = {
    "timezone_lookup": TravelTool(
        "timezone_lookup",
        "Return local time for a city",
        lambda args: f"{args.get('city', 'Unknown')}: 09:30 JST",
    ),
    "currency_convert": TravelTool(
        "currency_convert",
        "Convert currency amounts",
        lambda args: f"{args['amount']} {args['from']} -> {float(args['amount']) * 150:.0f} {args['to']}",
    ),
}


def pick_tool(question: str) -> tuple[str, dict[str, Any]]:
    llm = get_llm()
    catalog = [{"name": t.name, "description": t.description} for t in MANIFEST.values()]
    raw = llm.complete(
        f"Question: {question}\nSelect tool from manifest: {json.dumps(catalog)}",
        system='Return JSON {"tool":"...","args":{...}}',
    )
    payload = extract_json(raw)
    return payload.get("tool", "timezone_lookup"), payload.get("args", {})


def answer_with_tools(question: str) -> str:
    tool_name, args = pick_tool(question)
    tool = MANIFEST.get(tool_name, MANIFEST["timezone_lookup"])
    observation = tool.invoke(args)
    llm = get_llm()
    return llm.complete(
        f"Question: {question}\nTool output: {observation}\nWrite a concise answer."
    )


if __name__ == "__main__":
    print(answer_with_tools("What time is it in Tokyo right now?"))
    print(answer_with_tools("Convert 100 USD to JPY for my trip."))
