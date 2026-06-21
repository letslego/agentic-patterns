# Implementation Notes

This repository provides **original reference implementations** for 21 agentic design patterns.

## Design choices

| Area | Approach in this repo |
|------|------------------------|
| Chaining | Custom `Pipeline` + `StageContext` in `agentic_patterns/kernel.py` |
| Routing | IT helpdesk routes (`password_reset`, `software_install`, `general_support`) |
| Extraction demo | Recipe ingredients → normalized units → shopping list JSON |
| Tool use demo | Travel toolkit (`timezone_lookup`, `currency_convert`) |
| Multi-agent | Framework-agnostic `Router`, `Crew`, `CapabilityHost` |
| Framework glue | `agentic_patterns/adapters/langchain_bridge.py` and `langgraph_bridge.py` |

## Principles

1. **Clear pattern boundaries** — each module demonstrates one architectural idea (chain, route, reflect, etc.).
2. **Original docs and diagrams** — all prose and SVG assets are authored for this repository.
3. **Runnable without vendor SDKs** — mock LLM by default; optional OpenAI adapter.

## Mapping

Each folder under `code/NN_*` maps to one pattern chapter. See `docs/index.md` for walkthroughs and GitHub links.

## License

MIT for this repository's code and documentation.
