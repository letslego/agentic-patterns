#!/usr/bin/env python3
"""Run the recipe pipeline through LangChain Runnable adapter."""

from __future__ import annotations

from agentic_patterns.adapters.langchain_bridge import recipe_chain_runnable


def main() -> None:
    chain = recipe_chain_runnable()
    sample = (
        "Rustic loaf: mix 2 cups flour, 1 tsp yeast, 1 cup warm water, "
        "and 1 tbsp olive oil."
    )
    result = chain.invoke({"recipe_text": sample})
    print(result.get("shopping_json", result))


if __name__ == "__main__":
    main()
