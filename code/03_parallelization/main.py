"""Pattern 03: Parallelization — concurrent LLM calls, then merge."""

from __future__ import annotations

import asyncio

from agentic_patterns.common import get_llm


async def summarize_chunk(chunk: str) -> str:
    llm = get_llm()
    return llm.complete(f"Summarize this text in one line:\n{chunk}")


async def parallel_summaries(chunks: list[str]) -> list[str]:
    return await asyncio.gather(*(summarize_chunk(c) for c in chunks))


def merge_summaries(summaries: list[str]) -> str:
    llm = get_llm()
    joined = "\n".join(f"- {s}" for s in summaries)
    return llm.complete(f"Merge these summaries into one paragraph:\n{joined}")


async def run(chunks: list[str]) -> str:
    summaries = await parallel_summaries(chunks)
    return merge_summaries(summaries)


if __name__ == "__main__":
    samples = [
        "Prompt chaining breaks tasks into sequential LLM stages.",
        "Routing classifies input and dispatches to specialized handlers.",
        "RAG retrieves documents before generating grounded answers.",
    ]
    print(asyncio.run(run(samples)))
