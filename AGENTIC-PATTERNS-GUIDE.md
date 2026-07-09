<!-- source: docs/index.md -->
# Agentic Patterns Guide

A code-linked guide to **21 agentic design patterns** for building intelligent systems.

![Agent capability levels](./images/agent-levels.svg)

## How to use this guide

Each chapter explains one pattern in plain language, includes an **original diagram** (22 total across the guide), and links to a **runnable reference implementation** in this repository.

```bash
# Example: run Pattern 01 without API keys
python code/01_prompt_chaining/main.py
```

## Table of contents

### Introduction

- [Introduction & agent levels](./introduction.md)

### Part 1 — Foundational patterns

1. [Prompt Chaining](./part-1-foundational/01-prompt-chaining.md)
2. [Routing](./part-1-foundational/02-routing.md)
3. [Parallelization](./part-1-foundational/03-parallelization.md)
4. [Reflection](./part-1-foundational/04-reflection.md)
5. [Tool Use](./part-1-foundational/05-tool-use.md)
6. [Planning](./part-1-foundational/06-planning.md)
7. [Multi-Agent Collaboration](./part-1-foundational/07-multi-agent.md)

### Part 2 — Advanced systems

8. [Memory Management](./part-2-advanced/08-memory-management.md)
9. [Learning and Adaptation](./part-2-advanced/09-learning-adaptation.md)
10. [Model Context Protocol (MCP)](./part-2-advanced/10-mcp.md)
11. [Goal Setting and Monitoring](./part-2-advanced/11-goal-monitoring.md)

### Part 3 — Production concerns

12. [Exception Handling and Recovery](./part-3-production/12-exception-handling.md)
13. [Human-in-the-Loop](./part-3-production/13-human-in-the-loop.md)
14. [Knowledge Retrieval (RAG)](./part-3-production/14-rag.md)

### Part 4 — Multi-agent architectures

15. [Inter-Agent Communication (A2A)](./part-4-multi-agent/15-inter-agent-communication.md)
16. [Resource-Aware Optimization](./part-4-multi-agent/16-resource-optimization.md)
17. [Reasoning Techniques](./part-4-multi-agent/17-reasoning.md)
18. [Guardrails and Safety](./part-4-multi-agent/18-guardrails.md)
19. [Evaluation and Monitoring](./part-4-multi-agent/19-evaluation.md)
20. [Prioritization](./part-4-multi-agent/20-prioritization.md)
21. [Exploration and Discovery](./part-4-multi-agent/21-exploration.md)

### Appendix

- [Framework notes](./appendix/frameworks.md)
- [Framework adapters (LangChain / LangGraph)](./appendix/framework-adapters.md)

## Repository

All code lives at [github.com/letslego/agentic-patterns](https://github.com/letslego/agentic-patterns).

**Live site:** [letslego.github.io/agentic-patterns](https://letslego.github.io/agentic-patterns/)


---

<!-- source: docs/introduction.md -->
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

## Architecture

Pattern logic lives in `agentic_patterns/kernel.py` with optional adapters for LangChain and LangGraph. See the [framework adapters appendix](./appendix/framework-adapters.md).


---

<!-- source: docs/part-1-foundational/01-prompt-chaining.md -->
# Chapter 01: Prompt Chaining

## Pattern overview

Break complex tasks into a linear sequence of focused LLM calls. Each step consumes the previous output as context.

![Prompt Chaining diagram](../images/prompt-chaining.svg)

## Reference implementation

**Source:** [`code/01_prompt_chaining/main.py`](https://github.com/letslego/agentic-patterns/blob/main/code/01_prompt_chaining/main.py)

Split ingredient extraction, unit normalization, and shopping-list JSON into three pipeline stages using `Pipeline` + `StageContext` (not LangChain LCEL).

### Run locally

```bash
python code/01_prompt_chaining/main.py
```

## Key takeaways

- Decompose before you prompt.
- Keep each step single-purpose.
- Validate intermediate outputs.

## Related patterns

See the [pattern index](../index.md).

## Further reading

- [`agentic_patterns/kernel.py`](https://github.com/letslego/agentic-patterns/blob/main/agentic_patterns/kernel.py) — pipeline primitives
- [`agentic_patterns/common.py`](https://github.com/letslego/agentic-patterns/blob/main/agentic_patterns/common.py) — shared LLM client utilities


---

<!-- source: docs/part-1-foundational/02-routing.md -->
# Chapter 02: Routing

## Pattern overview

Classify incoming requests and dispatch them to specialized handlers or sub-agents.

![Routing diagram](../images/routing.svg)

## Reference implementation

**Source:** [`code/02_routing/main.py`](https://github.com/letslego/agentic-patterns/blob/main/code/02_routing/main.py)

IT helpdesk router maps tickets to `password_reset`, `software_install`, or `general_support` handlers via `agentic_patterns.kernel.Router`.

### Run locally

```bash
python code/02_routing/main.py
```

## Key takeaways

- Separate classification from execution.
- Keep route labels stable.
- Log routing decisions for evaluation.

## Related patterns

See the [pattern index](../index.md).


---

<!-- source: docs/part-1-foundational/03-parallelization.md -->
# Chapter 03: Parallelization

## Pattern overview

Execute independent subtasks concurrently, then merge results.

![Parallelization diagram](../images/parallelization.svg)


## Reference implementation

**Source:** [`code/03_parallelization/main.py`](https://github.com/letslego/agentic-patterns/blob/main/code/03_parallelization/main.py)

Uses a thread pool to summarize chunks in parallel before a merge step.

### Run locally

```bash
python code/03_parallelization/main.py
```

## Key takeaways

- Parallelize only truly independent work.
- Merge with a final synthesis prompt.
- Watch token and cost budgets.


---

<!-- source: docs/part-1-foundational/04-reflection.md -->
# Chapter 04: Reflection

## Pattern overview

Generate a draft, critique it, and revise in a loop until quality thresholds are met.

![Reflection diagram](../images/reflection.svg)


## Reference implementation

**Source:** [`code/04_reflection/main.py`](https://github.com/letslego/agentic-patterns/blob/main/code/04_reflection/main.py)

Three functions—`draft`, `critique`, `revise`—form a self-improvement loop.

### Run locally

```bash
python code/04_reflection/main.py
```

## Key takeaways

- Cap reflection rounds to control cost.
- Make critique rubric explicit.
- Store diffs for monitoring.


---

<!-- source: docs/part-1-foundational/05-tool-use.md -->
# Chapter 05: Tool Use (Function Calling)

## Pattern overview

Let the model choose external tools (APIs, calculators, search) and incorporate results.

![Tool use diagram](../images/tool-use.svg)


## Reference implementation

**Source:** [`code/05_tool_use/main.py`](https://github.com/letslego/agentic-patterns/blob/main/code/05_tool_use/main.py)

Tool registry with JSON selection payload and post-tool synthesis.

### Run locally

```bash
python code/05_tool_use/main.py
```

## Key takeaways

- Tools need crisp schemas.
- Validate arguments before execution.
- Never eval untrusted code in production.


---

<!-- source: docs/part-1-foundational/06-planning.md -->
# Chapter 06: Planning

## Pattern overview

Decompose goals into ordered steps and track execution status.

![Planning diagram](../images/planning.svg)


## Reference implementation

**Source:** [`code/06_planning/main.py`](https://github.com/letslego/agentic-patterns/blob/main/code/06_planning/main.py)

`PlanStep` dataclass tracks pending/done states across a generated plan.

### Run locally

```bash
python code/06_planning/main.py
```

## Key takeaways

- Plans should be revisitable.
- Re-plan when tools fail.
- Keep steps observable.


---

<!-- source: docs/part-1-foundational/07-multi-agent.md -->
# Chapter 07: Multi-Agent Collaboration

## Pattern overview

Coordinate specialist agents through a coordinator role and shared context.

![Multi-agent diagram](../images/multi-agent.svg)

## Reference implementation

**Source:** [`code/07_multi_agent/main.py`](https://github.com/letslego/agentic-patterns/blob/main/code/07_multi_agent/main.py)

Researcher → PM outline → Writer draft → PM review pipeline.

### Run locally

```bash
python code/07_multi_agent/main.py
```

## Key takeaways

- Define roles and interfaces.
- Pass structured context between agents.
- Avoid duplicate responsibilities.


---

<!-- source: docs/part-2-advanced/08-memory-management.md -->
# Chapter 08: Memory Management

## Pattern overview

Combine short-term conversation buffer with persistent long-term store.

![Memory management diagram](../images/memory-management.svg)


## Reference implementation

**Source:** [`code/08_memory_management/main.py`](https://github.com/letslego/agentic-patterns/blob/main/code/08_memory_management/main.py)

`MemoryStore` uses a deque for short-term memory and a dict for long-term recall.

### Run locally

```bash
python code/08_memory_management/main.py
```

## Key takeaways

- Bound short-term memory.
- Persist only vetted facts.
- Retrieve before answering.


---

<!-- source: docs/part-2-advanced/09-learning-adaptation.md -->
# Chapter 09: Learning and Adaptation

## Pattern overview

Update system behavior from user or evaluator feedback over time.

![Learning and adaptation diagram](../images/learning-adaptation.svg)


## Reference implementation

**Source:** [`code/09_learning_adaptation/main.py`](https://github.com/letslego/agentic-patterns/blob/main/code/09_learning_adaptation/main.py)

`AdaptiveAgent.learn_from_feedback()` rewrites its system prompt from accumulated feedback.

### Run locally

```bash
python code/09_learning_adaptation/main.py
```

## Key takeaways

- Version prompts after updates.
- Require human approval for policy changes.
- Measure before/after quality.


---

<!-- source: docs/part-2-advanced/10-mcp.md -->
# Chapter 10: Model Context Protocol (MCP)

## Pattern overview

Standardize how agents discover resources and invoke tools via a protocol server.

![MCP diagram](../images/mcp.svg)


## Reference implementation

**Source:** [`code/10_mcp/main.py`](https://github.com/letslego/agentic-patterns/blob/main/code/10_mcp/main.py)

Minimal MCP server/client with `resources/read` and `tools/call` methods.

### Run locally

```bash
python code/10_mcp/main.py
```

## Key takeaways

- Treat MCP as an integration boundary.
- Authenticate tool hosts.
- Keep handlers idempotent.


---

<!-- source: docs/part-2-advanced/11-goal-monitoring.md -->
# Chapter 11: Goal Setting and Monitoring

## Pattern overview

Define measurable targets and track progress during agent execution.

![Goal monitoring diagram](../images/goal-monitoring.svg)


## Reference implementation

**Source:** [`code/11_goal_monitoring/main.py`](https://github.com/letslego/agentic-patterns/blob/main/code/11_goal_monitoring/main.py)

`GoalMonitor` reports percent complete against numeric targets.

### Run locally

```bash
python code/11_goal_monitoring/main.py
```

## Key takeaways

- Goals must be measurable.
- Alert when progress stalls.
- Separate leading vs lagging metrics.


---

<!-- source: docs/part-3-production/12-exception-handling.md -->
# Chapter 12: Exception Handling and Recovery

## Pattern overview

Retry transient failures and provide graceful fallbacks.

![Exception handling diagram](../images/exception-handling.svg)


## Reference implementation

**Source:** [`code/12_exception_handling/main.py`](https://github.com/letslego/agentic-patterns/blob/main/code/12_exception_handling/main.py)

`with_retry()` wraps flaky calls with backoff and optional fallback.

### Run locally

```bash
python code/12_exception_handling/main.py
```

## Key takeaways

- Classify retryable vs fatal errors.
- Surface final failure reasons.
- Use circuit breakers at scale.


---

<!-- source: docs/part-3-production/13-human-in-the-loop.md -->
# Chapter 13: Human-in-the-Loop

## Pattern overview

Require human approval before high-impact or irreversible actions.

![Human-in-the-loop diagram](../images/human-in-the-loop.svg)


## Reference implementation

**Source:** [`code/13_human_in_the_loop/main.py`](https://github.com/letslego/agentic-patterns/blob/main/code/13_human_in_the_loop/main.py)

Approval gate wraps risky actions such as bulk email sends.

### Run locally

```bash
python code/13_human_in_the_loop/main.py
```

## Key takeaways

- Default deny for destructive operations.
- Show diffs to reviewers.
- Audit all decisions.


---

<!-- source: docs/part-3-production/14-rag.md -->
# Chapter 14: Knowledge Retrieval (RAG)

## Pattern overview

Retrieve relevant documents, inject them into context, then generate grounded answers.

![RAG diagram](../images/rag.svg)

## Reference implementation

**Source:** [`code/14_rag/main.py`](https://github.com/letslego/agentic-patterns/blob/main/code/14_rag/main.py)

Keyword retriever over an in-memory corpus plus grounded generation.

### Run locally

```bash
python code/14_rag/main.py
```

## Key takeaways

- Chunk and embed thoughtfully.
- Cite sources in answers.
- Monitor retrieval precision.


---

<!-- source: docs/part-4-multi-agent/15-inter-agent-communication.md -->
# Chapter 15: Inter-Agent Communication (A2A)

## Pattern overview

Exchange structured messages between agents through a pub/sub bus.

![Inter-agent communication diagram](../images/inter-agent-communication.svg)


## Reference implementation

**Source:** [`code/15_inter_agent_communication/main.py`](https://github.com/letslego/agentic-patterns/blob/main/code/15_inter_agent_communication/main.py)

`MessageBus` delivers `AgentMessage` objects to subscribed handlers.

### Run locally

```bash
python code/15_inter_agent_communication/main.py
```

## Key takeaways

- Use typed message schemas.
- Avoid circular message storms.
- Include correlation IDs.


---

<!-- source: docs/part-4-multi-agent/16-resource-optimization.md -->
# Chapter 16: Resource-Aware Optimization

## Pattern overview

Select models and strategies based on token, latency, and cost budgets.

![Resource optimization diagram](../images/resource-optimization.svg)


## Reference implementation

**Source:** [`code/16_resource_optimization/main.py`](https://github.com/letslego/agentic-patterns/blob/main/code/16_resource_optimization/main.py)

`ResourceBudget` gates model choice between large and small models.

### Run locally

```bash
python code/16_resource_optimization/main.py
```

## Key takeaways

- Track spend per task.
- Downshift models when possible.
- Cache deterministic sub-results.


---

<!-- source: docs/part-4-multi-agent/17-reasoning.md -->
# Chapter 17: Reasoning Techniques

## Pattern overview

Apply ReAct-style thought/action/observation loops for multi-step reasoning.

![Reasoning diagram](../images/reasoning.svg)


## Reference implementation

**Source:** [`code/17_reasoning/main.py`](https://github.com/letslego/agentic-patterns/blob/main/code/17_reasoning/main.py)

`react_loop()` iterates until a final answer appears in the trace.

### Run locally

```bash
python code/17_reasoning/main.py
```

## Key takeaways

- Cap reasoning steps.
- Log traces for debugging.
- Combine with tool use for grounding.


---

<!-- source: docs/part-4-multi-agent/18-guardrails.md -->
# Chapter 18: Guardrails and Safety Patterns

## Pattern overview

Validate inputs and outputs against policy before and after generation.

![Guardrails diagram](../images/guardrails.svg)


## Reference implementation

**Source:** [`code/18_guardrails/main.py`](https://github.com/letslego/agentic-patterns/blob/main/code/18_guardrails/main.py)

`safe_generate()` runs regex and secret-leak checks on both sides.

### Run locally

```bash
python code/18_guardrails/main.py
```

## Key takeaways

- Defense in depth.
- Block prompt injection patterns.
- Redact secrets automatically.


---

<!-- source: docs/part-4-multi-agent/19-evaluation.md -->
# Chapter 19: Evaluation and Monitoring

## Pattern overview

Score agent outputs and aggregate quality metrics over time.

![Evaluation diagram](../images/evaluation.svg)


## Reference implementation

**Source:** [`code/19_evaluation/main.py`](https://github.com/letslego/agentic-patterns/blob/main/code/19_evaluation/main.py)

`EvalMonitor` stores scored records and reports rolling averages.

### Run locally

```bash
python code/19_evaluation/main.py
```

## Key takeaways

- Evaluate continuously.
- Use human labels where possible.
- Track regressions by pattern.


---

<!-- source: docs/part-4-multi-agent/20-prioritization.md -->
# Chapter 20: Prioritization

## Pattern overview

Rank backlog items by urgency and impact to sequence agent work.

![Prioritization diagram](../images/prioritization.svg)


## Reference implementation

**Source:** [`code/20_prioritization/main.py`](https://github.com/letslego/agentic-patterns/blob/main/code/20_prioritization/main.py)

Weighted score `0.6*urgency + 0.4*impact` sorts the task queue.

### Run locally

```bash
python code/20_prioritization/main.py
```

## Key takeaways

- Make tradeoffs explicit.
- Re-prioritize as context changes.
- Keep humans in the loop for edge cases.


---

<!-- source: docs/part-4-multi-agent/21-exploration.md -->
# Chapter 21: Exploration and Discovery

## Pattern overview

Generate hypotheses, gather evidence, and select the best explanation.

![Exploration diagram](../images/exploration.svg)


## Reference implementation

**Source:** [`code/21_exploration/main.py`](https://github.com/letslego/agentic-patterns/blob/main/code/21_exploration/main.py)

`explore()` scores candidate hypotheses and returns the highest-confidence winner.

### Run locally

```bash
python code/21_exploration/main.py
```

## Key takeaways

- Treat exploration as experiments.
- Record negative results.
- Stop when confidence saturates.


---

<!-- source: docs/appendix/frameworks.md -->
# Appendix: Framework Notes

Many production agent stacks use **LangChain**, **LangGraph**, **CrewAI**, or **Google ADK**. This repository keeps core examples framework-agnostic so you can port them quickly.

| Framework | Strength | Map to patterns |
|-----------|----------|-----------------|
| LangChain / LCEL | Linear chains | [Prompt Chaining](../part-1-foundational/01-prompt-chaining.md) |
| LangGraph | Stateful graphs | [Routing](../part-1-foundational/02-routing.md), [Reflection](../part-1-foundational/04-reflection.md) |
| CrewAI | Role-based crews | [Multi-Agent](../part-1-foundational/07-multi-agent.md) |
| Google ADK | Deployment + eval | [Evaluation](../part-4-multi-agent/19-evaluation.md) |
| MCP SDK | Tool/resource hosts | [MCP](../part-2-advanced/10-mcp.md) |

Porting tip: use [`framework adapters`](./framework-adapters.md) to run kernel workflows through LangChain or LangGraph without rewriting pattern logic.


---

<!-- source: docs/appendix/framework-adapters.md -->
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


---

