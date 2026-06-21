# Agentic Patterns

Reference implementations and companion guide for **21 agentic design patterns** inspired by [*Agentic Design Patterns: A Hands-On Guide to Building Intelligent Systems*](https://www.google.com/books/edition/Agentic_Design_Patterns/) by Antonio Gulli.

This repository provides:

- **Runnable Python examples** for every pattern (works offline with a mock LLM)
- **Original diagrams** and a markdown companion guide in [`docs/`](docs/)
- **Cross-links** from each guide section to the matching code module

> **Note:** This is an independent companion project. It does not reproduce the original book text. For the full treatment, diagrams, and extended appendices, please refer to the official publication.

## Quick start

```bash
git clone https://github.com/letslego/agentic-patterns.git
cd agentic-patterns
python -m venv .venv && source .venv/bin/activate
pip install -e .
python code/01_prompt_chaining/main.py
```

Use a real model provider:

```bash
export AGENTIC_LLM_PROVIDER=openai
export OPENAI_API_KEY=sk-...
pip install -e ".[openai]"
python code/02_routing/main.py
```

## Pattern index

| # | Pattern | Code | Guide |
|---|---------|------|-------|
| 01 | Prompt Chaining | [`code/01_prompt_chaining/`](code/01_prompt_chaining/) | [Chapter 1](docs/part-1-foundational/01-prompt-chaining.md) |
| 02 | Routing | [`code/02_routing/`](code/02_routing/) | [Chapter 2](docs/part-1-foundational/02-routing.md) |
| 03 | Parallelization | [`code/03_parallelization/`](code/03_parallelization/) | [Chapter 3](docs/part-1-foundational/03-parallelization.md) |
| 04 | Reflection | [`code/04_reflection/`](code/04_reflection/) | [Chapter 4](docs/part-1-foundational/04-reflection.md) |
| 05 | Tool Use | [`code/05_tool_use/`](code/05_tool_use/) | [Chapter 5](docs/part-1-foundational/05-tool-use.md) |
| 06 | Planning | [`code/06_planning/`](code/06_planning/) | [Chapter 6](docs/part-1-foundational/06-planning.md) |
| 07 | Multi-Agent | [`code/07_multi_agent/`](code/07_multi_agent/) | [Chapter 7](docs/part-1-foundational/07-multi-agent.md) |
| 08 | Memory Management | [`code/08_memory_management/`](code/08_memory_management/) | [Chapter 8](docs/part-2-advanced/08-memory-management.md) |
| 09 | Learning & Adaptation | [`code/09_learning_adaptation/`](code/09_learning_adaptation/) | [Chapter 9](docs/part-2-advanced/09-learning-adaptation.md) |
| 10 | MCP | [`code/10_mcp/`](code/10_mcp/) | [Chapter 10](docs/part-2-advanced/10-mcp.md) |
| 11 | Goal Setting & Monitoring | [`code/11_goal_monitoring/`](code/11_goal_monitoring/) | [Chapter 11](docs/part-2-advanced/11-goal-monitoring.md) |
| 12 | Exception Handling | [`code/12_exception_handling/`](code/12_exception_handling/) | [Chapter 12](docs/part-3-production/12-exception-handling.md) |
| 13 | Human-in-the-Loop | [`code/13_human_in_the_loop/`](code/13_human_in_the_loop/) | [Chapter 13](docs/part-3-production/13-human-in-the-loop.md) |
| 14 | RAG | [`code/14_rag/`](code/14_rag/) | [Chapter 14](docs/part-3-production/14-rag.md) |
| 15 | Inter-Agent Communication | [`code/15_inter_agent_communication/`](code/15_inter_agent_communication/) | [Chapter 15](docs/part-4-multi-agent/15-inter-agent-communication.md) |
| 16 | Resource-Aware Optimization | [`code/16_resource_optimization/`](code/16_resource_optimization/) | [Chapter 16](docs/part-4-multi-agent/16-resource-optimization.md) |
| 17 | Reasoning Techniques | [`code/17_reasoning/`](code/17_reasoning/) | [Chapter 17](docs/part-4-multi-agent/17-reasoning.md) |
| 18 | Guardrails & Safety | [`code/18_guardrails/`](code/18_guardrails/) | [Chapter 18](docs/part-4-multi-agent/18-guardrails.md) |
| 19 | Evaluation & Monitoring | [`code/19_evaluation/`](code/19_evaluation/) | [Chapter 19](docs/part-4-multi-agent/19-evaluation.md) |
| 20 | Prioritization | [`code/20_prioritization/`](code/20_prioritization/) | [Chapter 20](docs/part-4-multi-agent/20-prioritization.md) |
| 21 | Exploration & Discovery | [`code/21_exploration/`](code/21_exploration/) | [Chapter 21](docs/part-4-multi-agent/21-exploration.md) |

## Documentation

Read the full companion guide starting at [`docs/index.md`](docs/index.md).

## License

MIT — see [LICENSE](LICENSE). Pattern names and conceptual structure acknowledge Antonio Gulli's *Agentic Design Patterns*.

## Contributing

Issues and PRs welcome. Keep examples minimal, runnable without API keys by default, and link each doc section to its code module.
