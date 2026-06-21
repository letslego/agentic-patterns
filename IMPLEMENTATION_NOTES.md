# Clean-Room Implementation Notes

This repository implements the **agentic design pattern taxonomy** described in Antonio Gulli's *Agentic Design Patterns* using **original code**.

## What we deliberately changed

| Book reference style | This repository |
|---------------------|-----------------|
| LangChain LCEL (`prompt \| llm \| parser`) | Custom `Pipeline` + `StageContext` in `agentic_patterns/kernel.py` |
| `booking_handler` / `info_handler` travel routing | IT helpdesk routes (`password_reset`, `software_install`) |
| Laptop specs → JSON extraction demo | Recipe ingredients → normalized units → shopping list JSON |
| CrewAI `get_stock_price` tool demo | Travel toolkit (`timezone_lookup`, `currency_convert`) |
| Google ADK coordinator samples | Framework-agnostic `Router`, `Crew`, `CapabilityHost` |
| LangChain/LCEL book snippets | `agentic_patterns/adapters/langchain_bridge.py` wrapping kernel |
| LangGraph book graphs | `agentic_patterns/adapters/langgraph_bridge.py` compiling kernel workflows |

## Principles

1. **Pattern fidelity, not code parity** — each module demonstrates the same architectural idea (chain, route, reflect, etc.) with different APIs and domains.
2. **No copied prose or diagrams** — docs and SVG assets are authored for this repo.
3. **Runnable without vendor SDKs** — mock LLM by default; optional OpenAI adapter only.

## Mapping

Each folder under `code/NN_*` maps to one chapter pattern. See `docs/index.md` for narrative walkthroughs and GitHub links.

## License

MIT for this repository's code and docs. The original book remains the authoritative reference for full explanations and extended appendices.
