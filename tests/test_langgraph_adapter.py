import pytest

pytest.importorskip("langgraph")

from agentic_patterns.adapters.langgraph_bridge import (
    compile_crew_graph,
    compile_pipeline_graph,
    compile_reflection_graph,
    compile_router_graph,
)
from agentic_patterns.demos.helpdesk import build_helpdesk_router
from agentic_patterns.demos.press_release import (
    draft_release,
    editorial_review,
    revise_release,
)
from agentic_patterns.demos.recipe_pipeline import build_recipe_pipeline
from agentic_patterns.kernel import Crew, Specialist


def test_pipeline_graph_runs_linear_stages():
    graph = compile_pipeline_graph(build_recipe_pipeline())
    state = graph.invoke({"recipe_text": "1 cup water, 2 cups flour"})
    assert state.get("shopping_json")


def test_router_graph_routes_ticket():
    graph = compile_router_graph(build_helpdesk_router())
    state = graph.invoke({"message": "I'm locked out after password expiry."})
    assert "PasswordReset" in state.get("response", "")


def test_reflection_graph_produces_draft():
    graph = compile_reflection_graph(
        draft_fn=draft_release,
        critique_fn=editorial_review,
        revise_fn=revise_release,
        max_rounds=1,
    )
    state = graph.invoke({"topic": "Orion SDK", "max_rounds": 1})
    assert state.get("draft")


def test_crew_graph_runs_specialists():
    crew = Crew(
        members=[
            Specialist("SRE", "triage alerts"),
            Specialist("Fix", "propose remediation"),
        ]
    )
    graph = compile_crew_graph(crew)
    state = graph.invoke({"mission": "latency spike", "prior": "", "transcript": []})
    assert len(state.get("transcript", [])) == 2
