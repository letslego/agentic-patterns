"""Original runtime primitives for agentic pattern examples."""

from __future__ import annotations

import asyncio
from collections.abc import Awaitable, Callable, Iterable
from dataclasses import dataclass, field
from typing import Any, Generic, TypeVar

from agentic_patterns.common import LLMClient, get_llm

T = TypeVar("T")
R = TypeVar("R")


@dataclass
class StageContext:
    """Mutable bag passed between pipeline stages."""

    data: dict[str, Any] = field(default_factory=dict)

    def put(self, key: str, value: Any) -> None:
        self.data[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        return self.data.get(key, default)


StageFn = Callable[[StageContext, LLMClient], str]


@dataclass
class Pipeline:
    """Linear composition of LLM stages (alternative to LCEL-style chaining)."""

    stages: list[tuple[str, StageFn]]

    def run(self, seed: dict[str, Any], llm: LLMClient | None = None) -> StageContext:
        client = llm or get_llm()
        ctx = StageContext(data=dict(seed))
        for name, stage in self.stages:
            output = stage(ctx, client)
            ctx.put(name, output)
        return ctx


RouteHandler = Callable[[str], str]


@dataclass
class Router:
    """Intent router with keyword fallback when LLM labels are ambiguous."""

    routes: dict[str, RouteHandler]
    default: str
    system: str

    def decide(self, message: str, llm: LLMClient | None = None) -> str:
        client = llm or get_llm()
        labels = ", ".join(self.routes)
        raw = client.complete(
            f"Message:\n{message}\n\nChoose one route label: {labels}",
            system=self.system,
        ).lower()
        for label in self.routes:
            if label in raw:
                return label
        return self.default

    def dispatch(self, message: str, llm: LLMClient | None = None) -> str:
        label = self.decide(message, llm)
        return self.routes[label](message)


async def map_async(
    items: Iterable[T],
    worker: Callable[[T], Awaitable[R]],
    *,
    concurrency: int = 4,
) -> list[R]:
    sem = asyncio.Semaphore(concurrency)
    results: list[R | None] = [None] * len(list(items))  # placeholder
    items_list = list(items)

    async def run(idx: int, item: T) -> None:
        async with sem:
            results[idx] = await worker(item)

    await asyncio.gather(*(run(i, item) for i, item in enumerate(items_list)))
    return [r for r in results if r is not None]


@dataclass
class Specialist:
    name: str
    brief: str

    def run(self, task: str, prior: str, llm: LLMClient | None = None) -> str:
        client = llm or get_llm()
        return client.complete(
            f"Role: {self.brief}\nPrior work:\n{prior}\n\nCurrent task:\n{task}",
            system=f"You are {self.name}.",
        )


@dataclass
class Crew:
    """Sequential multi-specialist workflow."""

    members: list[Specialist]

    def execute(self, mission: str, llm: LLMClient | None = None) -> list[tuple[str, str]]:
        transcript: list[tuple[str, str]] = []
        prior = ""
        for member in self.members:
            result = member.run(mission, prior, llm)
            transcript.append((member.name, result))
            prior = result
        return transcript
