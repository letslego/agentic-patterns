# Appendix: Framework Notes

The original book demonstrates patterns with **LangChain**, **LangGraph**, **CrewAI**, and **Google ADK**. This repository keeps examples framework-agnostic so you can port them quickly.

| Framework | Strength | Map to patterns |
|-----------|----------|-----------------|
| LangChain / LCEL | Linear chains | [Prompt Chaining](../part-1-foundational/01-prompt-chaining.md) |
| LangGraph | Stateful graphs | [Routing](../part-1-foundational/02-routing.md), [Reflection](../part-1-foundational/04-reflection.md) |
| CrewAI | Role-based crews | [Multi-Agent](../part-1-foundational/07-multi-agent.md) |
| Google ADK | Deployment + eval | [Evaluation](../part-4-multi-agent/19-evaluation.md) |
| MCP SDK | Tool/resource hosts | [MCP](../part-2-advanced/10-mcp.md) |

Porting tip: replace `get_llm()` calls with your framework's model node and wrap side effects as tools.
