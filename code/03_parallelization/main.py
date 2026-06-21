"""Pattern 03: Parallelization — concurrent survey theme extraction."""

from __future__ import annotations

import asyncio

from agentic_patterns.common import get_llm


async def theme_from_comment(comment: str) -> str:
    llm = get_llm()
    return llm.complete(f"Summarize this survey comment into one theme:\n{comment}")


async def parallel_survey_themes(comments: list[str]) -> list[str]:
    return await asyncio.gather(*(theme_from_comment(c) for c in comments))


def synthesize(themes: list[str]) -> str:
    llm = get_llm()
    joined = "\n".join(f"- {t}" for t in themes)
    return llm.complete(f"Merge themes from survey responses:\n{joined}")


async def run(comments: list[str]) -> str:
    themes = await parallel_survey_themes(comments)
    return synthesize(themes)


if __name__ == "__main__":
    samples = [
        "Setup wizard skipped DNS step and I was confused.",
        "Invoice labels don't match our PO numbers.",
        "Love the dashboard, but export CSV failed once.",
    ]
    print(asyncio.run(run(samples)))
