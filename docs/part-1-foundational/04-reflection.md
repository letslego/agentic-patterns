# Chapter 04: Reflection

## Pattern overview

Generate a draft, critique it, and revise in a loop until quality thresholds are met.

![Reflection diagram](../images/reflection.svg)


## Reference implementation

**Source:** [`code/04_reflection/main.py`](https://github.com/letslego/agentic-patterns/blob/main/code/04_reflection/main.py)

Three functions—`draft_explanation`, `critique_draft`, `revise_draft`—form a self-improvement loop for refining explanations.

### Run locally

```bash
python code/04_reflection/main.py
```

## Key takeaways

- Cap reflection rounds to control cost.
- Make critique rubric explicit.
- Store diffs for monitoring.
