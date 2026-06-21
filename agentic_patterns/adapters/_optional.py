"""Optional dependency helpers for framework adapters."""

from __future__ import annotations

import importlib


def require_runnable_lambda():
    return importlib.import_module("langchain_core.runnables").RunnableLambda


def require_state_graph():
    graph = importlib.import_module("langgraph.graph")
    return graph.StateGraph, graph.END
