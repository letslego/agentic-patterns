# Chapter 16: Resource-Aware Optimization

## Pattern overview

Select models and strategies based on token, latency, and cost budgets.

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
