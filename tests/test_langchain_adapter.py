import pytest

pytest.importorskip("langchain_core")

from agentic_patterns.adapters.langchain_bridge import (
    pipeline_to_runnable,
    router_to_runnable,
)
from agentic_patterns.demos.helpdesk import build_helpdesk_router
from agentic_patterns.demos.recipe_pipeline import build_recipe_pipeline


def test_pipeline_runnable_invokes_stages():
    chain = pipeline_to_runnable(build_recipe_pipeline())
    out = chain.invoke({"recipe_text": "2 cups flour and 1 tsp yeast"})
    assert "extract" in out
    assert "shopping_json" in out


def test_router_runnable_dispatches_ticket():
    runnable = router_to_runnable(build_helpdesk_router())
    response = runnable.invoke("Please install Figma on my laptop.")
    assert "SoftwareInstall" in response
