# Chapter 17: Reasoning Techniques

## Pattern overview

Apply ReAct-style thought/action/observation loops for multi-step reasoning.

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
