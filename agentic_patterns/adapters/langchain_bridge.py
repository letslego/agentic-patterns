"""LangChain adapters that expose kernel primitives as Runnable chains."""

from __future__ import annotations

from typing import Any

from agentic_patterns.adapters._optional import require_runnable_lambda
from agentic_patterns.common import LLMClient, get_llm
from agentic_patterns.kernel import Pipeline, Router


def pipeline_to_runnable(pipeline: Pipeline, *, llm: LLMClient | None = None):
    """Wrap a kernel Pipeline as a LangChain Runnable returning stage outputs."""
    RunnableLambda = require_runnable_lambda()

    client = llm or get_llm()

    def _invoke(inputs: dict[str, Any]) -> dict[str, Any]:
        ctx = pipeline.run(inputs, client)
        return dict(ctx.data)

    return RunnableLambda(_invoke)


def router_to_runnable(router: Router, *, llm: LLMClient | None = None):
    """Wrap a kernel Router as a Runnable that maps a message string to a response."""
    RunnableLambda = require_runnable_lambda()

    client = llm or get_llm()

    def _invoke(message: str) -> str:
        return router.dispatch(message, client)

    return RunnableLambda(_invoke)


def llm_prompt_to_runnable(
    *,
    system: str | None = None,
    llm: LLMClient | None = None,
):
    """Wrap kernel LLMClient.complete as a Runnable over a prompt string."""
    RunnableLambda = require_runnable_lambda()

    client = llm or get_llm()

    def _invoke(prompt: str) -> str:
        return client.complete(prompt, system=system)

    return RunnableLambda(_invoke)


def recipe_chain_runnable(*, llm: LLMClient | None = None):
    """Convenience: recipe pipeline as LCEL-compatible Runnable."""
    from agentic_patterns.demos.recipe_pipeline import build_recipe_pipeline

    return pipeline_to_runnable(build_recipe_pipeline(), llm=llm)
