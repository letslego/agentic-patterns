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
