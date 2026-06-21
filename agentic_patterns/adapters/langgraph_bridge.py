"""LangGraph adapters that compile kernel workflows into state graphs."""

from __future__ import annotations

from typing import Any, Callable, TypedDict

from agentic_patterns.adapters._optional import require_state_graph
from agentic_patterns.common import LLMClient, get_llm
from agentic_patterns.kernel import Crew, Pipeline, Router


class PipelineState(TypedDict, total=False):
    data: dict[str, Any]
    done: bool


class RouterState(TypedDict, total=False):
    message: str
    route: str
    response: str


class ReflectionState(TypedDict, total=False):
    topic: str
    draft: str
    feedback: str
    round: int
    max_rounds: int
    done: bool


class CrewState(TypedDict, total=False):
    mission: str
    prior: str
    index: int
    transcript: list[tuple[str, str]]
    done: bool


def compile_pipeline_graph(pipeline: Pipeline, *, llm: LLMClient | None = None):
    """Linear graph: each pipeline stage becomes one node."""
    StateGraph, END = require_state_graph()

    client = llm or get_llm()
    stage_names = [name for name, _ in pipeline.stages]

    graph = StateGraph(dict)

    def run_stage(state: dict[str, Any], stage_name: str, stage_fn) -> dict[str, Any]:
        ctx_data = {k: v for k, v in state.items() if k != "done"}
        from agentic_patterns.kernel import StageContext

        ctx = StageContext(data=ctx_data)
        output = stage_fn(ctx, client)
        ctx_data[stage_name] = output
        ctx_data["done"] = stage_name == stage_names[-1]
        return ctx_data

    for name, fn in pipeline.stages:
        graph.add_node(name, lambda s, n=name, f=fn: run_stage(s, n, f))

    graph.set_entry_point(stage_names[0])
    for i, name in enumerate(stage_names):
        if i + 1 < len(stage_names):
            graph.add_edge(name, stage_names[i + 1])
        else:
            graph.add_edge(name, END)

    return graph.compile()


def compile_router_graph(router: Router, *, llm: LLMClient | None = None):
    """Classify node + one handler node per route."""
    StateGraph, END = require_state_graph()

    client = llm or get_llm()
    route_names = list(router.routes.keys())

    graph = StateGraph(RouterState)

    def classify(state: RouterState) -> RouterState:
        label = router.decide(state["message"], client)
        return {"route": label}

    graph.add_node("classify", classify)

    for route_name, handler in router.routes.items():

        def make_handler(h: Callable[[str], str], label: str):
            def node(state: RouterState) -> RouterState:
                return {"response": h(state["message"]), "route": label}

            return node

        graph.add_node(route_name, make_handler(handler, route_name))

    graph.set_entry_point("classify")

    def pick_route(state: RouterState) -> str:
        return state.get("route", router.default)

    path_map = {name: name for name in route_names}
    graph.add_conditional_edges("classify", pick_route, path_map)
    for name in route_names:
        graph.add_edge(name, END)

    return graph.compile()


def compile_reflection_graph(
    *,
    draft_fn: Callable[[str], str],
    critique_fn: Callable[[str], str],
    revise_fn: Callable[[str, str], str],
    max_rounds: int = 2,
):
    """Cycle: draft -> critique -> revise until round budget exhausted."""
    StateGraph, END = require_state_graph()

    graph = StateGraph(ReflectionState)

    def draft_node(state: ReflectionState) -> ReflectionState:
        text = draft_fn(state["topic"])
        return {"draft": text, "round": 0}

    def critique_node(state: ReflectionState) -> ReflectionState:
        return {"feedback": critique_fn(state["draft"])}

    def revise_node(state: ReflectionState) -> ReflectionState:
        new_round = state.get("round", 0) + 1
        revised = revise_fn(state["draft"], state["feedback"])
        done = new_round >= state.get("max_rounds", max_rounds)
        return {"draft": revised, "round": new_round, "done": done}

    graph.add_node("draft", draft_node)
    graph.add_node("critique", critique_node)
    graph.add_node("revise", revise_node)
    graph.set_entry_point("draft")
    graph.add_edge("draft", "critique")
    graph.add_edge("critique", "revise")

    def continue_or_end(state: ReflectionState) -> str:
        return END if state.get("done") else "critique"

    graph.add_conditional_edges("revise", continue_or_end, {END: END, "critique": "critique"})
    return graph.compile()


def compile_crew_graph(crew: Crew, *, llm: LLMClient | None = None):
    """Sequential specialist nodes sharing prior context."""
    StateGraph, END = require_state_graph()

    client = llm or get_llm()
    member_names = [m.name for m in crew.members]

    graph = StateGraph(CrewState)

    def make_member_node(index: int):
        member = crew.members[index]

        def node(state: CrewState) -> CrewState:
            result = member.run(state["mission"], state.get("prior", ""), client)
            transcript = list(state.get("transcript", []))
            transcript.append((member.name, result))
            return {
                "prior": result,
                "index": index + 1,
                "transcript": transcript,
                "done": index + 1 >= len(crew.members),
            }

        return node

    for idx, name in enumerate(member_names):
        graph.add_node(name, make_member_node(idx))

    graph.set_entry_point(member_names[0])
    for i, name in enumerate(member_names):
        if i + 1 < len(member_names):
            graph.add_edge(name, member_names[i + 1])
        else:
            graph.add_edge(name, END)

    return graph.compile()
