# Chapter 19: Evaluation and Monitoring

## Pattern overview

Score agent outputs and aggregate quality metrics over time.

## Reference implementation

**Source:** [`code/19_evaluation/main.py`](https://github.com/letslego/agentic-patterns/blob/main/code/19_evaluation/main.py)

`EvalMonitor` stores scored records and reports rolling averages.

### Run locally

```bash
python code/19_evaluation/main.py
```

## Key takeaways

- Evaluate continuously.
- Use human labels where possible.
- Track regressions by pattern.
