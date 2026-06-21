"""Pattern 01: Prompt Chaining — recipe text to structured shopping list."""

from __future__ import annotations

from agentic_patterns.common import get_llm
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


def recipe_to_shopping_list(recipe_text: str) -> str:
    pipeline = Pipeline(
        stages=[
            ("extract", stage_extract),
            ("normalize", stage_normalize),
            ("shopping_json", stage_shopping_json),
        ]
    )
    result = pipeline.run({"recipe_text": recipe_text}, get_llm())
    return result.get("shopping_json", "")


if __name__ == "__main__":
    sample = (
        "Rustic loaf: mix 2 cups flour, 1 tsp yeast, 1 cup warm water, "
        "and 1 tbsp olive oil. Rest 90 minutes, then bake."
    )
    print(recipe_to_shopping_list(sample))
