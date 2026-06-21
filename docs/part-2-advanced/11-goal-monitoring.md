# Chapter 11: Goal Setting and Monitoring

## Pattern overview

Define measurable targets and track progress during agent execution.

## Reference implementation

**Source:** [`code/11_goal_monitoring/main.py`](https://github.com/letslego/agentic-patterns/blob/main/code/11_goal_monitoring/main.py)

`GoalMonitor` reports percent complete against numeric targets.

### Run locally

```bash
python code/11_goal_monitoring/main.py
```

## Key takeaways

- Goals must be measurable.
- Alert when progress stalls.
- Separate leading vs lagging metrics.
