# Chapter 21: Exploration and Discovery

## Pattern overview

Generate hypotheses, gather evidence, and select the best explanation.

![Exploration diagram](../images/exploration.svg)


## Reference implementation

**Source:** [`code/21_exploration/main.py`](https://github.com/letslego/agentic-patterns/blob/main/code/21_exploration/main.py)

`explore()` scores candidate hypotheses and returns the highest-confidence winner.

### Run locally

```bash
python code/21_exploration/main.py
```

## Key takeaways

- Treat exploration as experiments.
- Record negative results.
- Stop when confidence saturates.
