"""Pattern 03: Parallelization — run independent subtasks concurrently."""

from __future__ import annotations

from concurrent.futures import Future, ThreadPoolExecutor, as_completed
from typing import Iterable

from agentic_patterns.common import get_llm


def analyze_chunk(chunk: str) -> str:
    llm = get_llm()
    return llm.complete(f"Summarize this section in one sentence:\n\n{chunk}")


def parallel_summarize(chunks: Iterable[str], *, max_workers: int = 4) -> list[str]:
    chunks = list(chunks)
    results: list[str | None] = [None] * len(chunks)
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        future_map: dict[Future[str], int] = {
            pool.submit(analyze_chunk, chunk): idx for idx, chunk in enumerate(chunks)
        }
        for future in as_completed(future_map):
            idx = future_map[future]
            results[idx] = future.result()
    return [r or "" for r in results]


def merge_summaries(parts: list[str]) -> str:
    llm = get_llm()
    joined = "\n".join(f"- {p}" for p in parts)
    return llm.complete(f"Merge these bullet summaries into a cohesive paragraph:\n{joined}")


if __name__ == "__main__":
    sections = [
        "Section A discusses onboarding flows.",
        "Section B covers billing integrations.",
        "Section C explains observability dashboards.",
    ]
    partial = parallel_summarize(sections)
    print(merge_summaries(partial))
