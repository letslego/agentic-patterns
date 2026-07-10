"""Pattern 01: Prompt Chaining — topic to structured summary via staged LLM calls."""

from __future__ import annotations

from agentic_patterns.common import get_llm
from agentic_patterns.kernel import Pipeline, StageContext


def stage_outline(ctx: StageContext, llm) -> str:
    topic = ctx.get("topic", "")
    return llm.complete(
        f"List 3 key points for explaining: {topic}",
        system="Return a short numbered list.",
    )


def stage_expand(ctx: StageContext, llm) -> str:
    outline = ctx.get("outline", "")
    return llm.complete(
        f"Expand each point into one sentence:\n{outline}",
        system="Keep each point on its own line.",
    )


def stage_json(ctx: StageContext, llm) -> str:
    expanded = ctx.get("expand", "")
    return llm.complete(
        f"Convert to JSON with topic and points array:\n{expanded}",
        system="Return valid JSON only.",
    )


def explain_topic(topic: str) -> str:
    pipeline = Pipeline(
        stages=[
            ("outline", stage_outline),
            ("expand", stage_expand),
            ("json", stage_json),
        ]
    )
    result = pipeline.run({"topic": topic}, get_llm())
    return result.get("json", "")


if __name__ == "__main__":
    print(explain_topic("prompt chaining in agentic systems"))
