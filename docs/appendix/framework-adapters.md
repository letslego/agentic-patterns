# Framework Adapters (LangChain & LangGraph)

The kernel in `agentic_patterns/kernel.py` stays framework-agnostic. Adapter modules expose the same workflows through LangChain `Runnable` objects and compiled LangGraph state machines.

## Install

```bash
pip install -e ".[frameworks]"
```

## LangChain bridge

| Kernel type | Adapter | Example |
|-------------|---------|---------|
| `Pipeline` | `pipeline_to_runnable()` | `examples/langchain_recipe_pipeline.py` |
| `Router` | `router_to_runnable()` | — |
| `LLMClient` | `llm_prompt_to_runnable()` | — |

```python
from agentic_patterns.adapters.langchain_bridge import recipe_chain_runnable

chain = recipe_chain_runnable()
result = chain.invoke({"recipe_text": "2 cups flour, 1 tsp yeast"})
print(result["shopping_json"])
```

## LangGraph bridge

| Pattern | Adapter | Example |
|---------|---------|---------|
| Prompt chaining | `compile_pipeline_graph()` | uses recipe pipeline |
| Routing | `compile_router_graph()` | `examples/langgraph_helpdesk_router.py` |
| Reflection | `compile_reflection_graph()` | `examples/langgraph_reflection_loop.py` |
| Multi-agent crew | `compile_crew_graph()` | `examples/langgraph_incident_crew.py` |

```python
from agentic_patterns.adapters.langgraph_bridge import compile_router_graph
from agentic_patterns.demos.helpdesk import build_helpdesk_router

graph = compile_router_graph(build_helpdesk_router())
print(graph.invoke({"message": "Install VS Code on my laptop."}))
```

## Shared demos

Reusable workflows live in `agentic_patterns/demos/` so pattern examples and adapters stay in sync:

- `recipe_pipeline.py` — prompt chaining
- `helpdesk.py` — routing
- `press_release.py` — reflection

## Design note

Adapters are thin glue: they translate kernel state (`StageContext`, `Router`, `Crew`) into framework-native constructs. Swap `get_llm()` for a real provider or replace runnables with vendor chat models in your own integration layer.
