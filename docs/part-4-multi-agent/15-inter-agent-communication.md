# Chapter 15: Inter-Agent Communication (A2A)

## Pattern overview

Exchange structured messages between agents through a pub/sub bus.

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
