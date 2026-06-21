"""Recipe prompt-chaining demo pipeline."""

from __future__ import annotations

from agentic_patterns.kernel import Pipeline, StageContext


def stage_extract(ctx: StageContext, llm) -> str:
    recipe = ctx.get("recipe_text", "")
    return llm.complete(
        f"Extract ingredient lines from this recipe text:\n\n{recipe}",
        system="Return comma-separated ingredients only.",
    )


def stage_normalize(ctx: StageContext, llm) -> str:
    raw = ctx.get("extract", "")
    return llm.complete(
        f"Normalize to canonical units:\n{raw}",
        system="Use metric weights/volumes.",
    )


def stage_shopping_json(ctx: StageContext, llm) -> str:
    normalized = ctx.get("normalize", "")
    return llm.complete(
        f"Build grocery JSON shopping list from:\n{normalized}",
        system="Return valid JSON with an items array.",
    )


def build_recipe_pipeline() -> Pipeline:
    return Pipeline(
        stages=[
            ("extract", stage_extract),
            ("normalize", stage_normalize),
            ("shopping_json", stage_shopping_json),
        ]
    )
