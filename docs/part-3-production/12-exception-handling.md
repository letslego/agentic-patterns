# Chapter 12: Exception Handling and Recovery

## Pattern overview

Retry transient failures and provide graceful fallbacks.

## Reference implementation

**Source:** [`code/12_exception_handling/main.py`](https://github.com/letslego/agentic-patterns/blob/main/code/12_exception_handling/main.py)

`with_retry()` wraps flaky calls with backoff and optional fallback.

### Run locally

```bash
python code/12_exception_handling/main.py
```

## Key takeaways

- Classify retryable vs fatal errors.
- Surface final failure reasons.
- Use circuit breakers at scale.
