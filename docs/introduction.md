# Introduction: What Makes a System Agentic?

Large language models can answer questions, but **agents** pursue goals over multiple steps. They perceive context, decide actions, invoke tools, retain memory, and sometimes collaborate with other software entities.

## Agent capability levels

![Agent levels diagram](./images/agent-levels.svg)

| Level | Capabilities | Patterns in this guide |
|-------|--------------|------------------------|
| **0** | Reasoning only | Prompt design foundations |
| **1** | Tools + retrieval | [Tool Use](./part-1-foundational/05-tool-use.md), [RAG](./part-3-production/14-rag.md) |
| **2** | Planning + memory | [Planning](./part-1-foundational/06-planning.md), [Memory](./part-2-advanced/08-memory-management.md) |
| **3** | Multi-agent teams | [Multi-Agent](./part-1-foundational/07-multi-agent.md), [A2A](./part-4-multi-agent/15-inter-agent-communication.md) |

## Why patterns?

Agent systems fail in predictable ways: context overflow, runaway tool loops, brittle routing, missing guardrails. Design patterns give reusable structure—much like MVC for web apps or MapReduce for data pipelines.

## Code map

Shared utilities live in [`agentic_patterns/common.py`](https://github.com/letslego/agentic-patterns/blob/main/agentic_patterns/common.py). Every chapter example imports `get_llm()` which defaults to a deterministic mock client so you can explore patterns without API spend.

Set `AGENTIC_LLM_PROVIDER=openai` to swap in a real provider—see [`agentic_patterns/providers.py`](https://github.com/letslego/agentic-patterns/blob/main/agentic_patterns/providers.py).

## Attribution

Conceptual pattern names and taxonomy follow Antonio Gulli's *Agentic Design Patterns* (Springer, 2025). This guide's prose, diagrams, and code are original companion material.
