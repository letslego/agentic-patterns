"""Pattern 12: Exception Handling — circuit-aware retries."""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Callable, TypeVar

T = TypeVar("T")


@dataclass
class RetryPolicy:
    attempts: int = 3
    base_delay_s: float = 0.15


def resilient_call(
    operation: Callable[[], T],
    policy: RetryPolicy,
    *,
    on_error: Callable[[Exception, int], None] | None = None,
) -> T:
    last: Exception | None = None
    for attempt in range(1, policy.attempts + 1):
        try:
            return operation()
        except Exception as exc:  # noqa: BLE001 - teaching example
            last = exc
            if on_error:
                on_error(exc, attempt)
            if attempt < policy.attempts:
                time.sleep(policy.base_delay_s * attempt)
    assert last is not None
    raise last


if __name__ == "__main__":
    calls = {"count": 0}

    def flaky_export() -> str:
        calls["count"] += 1
        if calls["count"] < 3:
            raise TimeoutError("object store timeout")
        return "export-complete"

    result = resilient_call(flaky_export, RetryPolicy())
    print(result, "after", calls["count"], "attempts")
