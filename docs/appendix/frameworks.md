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
