"""Pattern 02: Routing — classify requests and dispatch to specialists."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from agentic_patterns.common import get_llm


@dataclass
class Route:
    name: str
    handler: Callable[[str], str]


ROUTES: dict[str, Route] = {
    "billing": Route("billing", lambda q: f"[Billing] Process refund for: {q}"),
    "engineering": Route("engineering", lambda q: f"[Engineering] Triage bug: {q}"),
    "general": Route("general", lambda q: f"[General] Answer: {q}"),
}


def classify(query: str) -> str:
    llm = get_llm()
    label = llm.complete(
        f"Classify this customer message into billing, engineering, or general:\n\n{query}",
        system="Reply with a single route label only.",
    ).strip().lower()
    for key in ROUTES:
        if key in label:
            return key
    return "general"


def route(query: str) -> str:
    route_name = classify(query)
    return ROUTES[route_name].handler(query)


if __name__ == "__main__":
    print(route("I was charged twice and need a refund."))
    print(route("The app crashes when I export a PDF."))
