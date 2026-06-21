"""Pattern 01: Prompt Chaining — recipe text to structured shopping list."""

from __future__ import annotations

from agentic_patterns.common import get_llm
from agentic_patterns.demos.recipe_pipeline import build_recipe_pipeline


def recipe_to_shopping_list(recipe_text: str) -> str:
    pipeline = build_recipe_pipeline()
    result = pipeline.run({"recipe_text": recipe_text}, get_llm())
    return result.get("shopping_json", "")


if __name__ == "__main__":
    sample = (
        "Rustic loaf: mix 2 cups flour, 1 tsp yeast, 1 cup warm water, "
        "and 1 tbsp olive oil. Rest 90 minutes, then bake."
    )
    print(recipe_to_shopping_list(sample))
