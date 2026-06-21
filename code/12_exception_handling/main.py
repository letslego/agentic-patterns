"""Pattern 12: Exception Handling and Recovery — retries and fallbacks."""

from __future__ import annotations

import time
from typing import Callable, TypeVar

T = TypeVar("T")


def with_retry(
    fn: Callable[[], T],
    *,
    retries: int = 3,
    delay_s: float = 0.2,
    fallback: Callable[[Exception], T] | None = None,
) -> T:
    last_error: Exception | None = None
    for attempt in range(1, retries + 1):
        try:
            return fn()
        except Exception as exc:  # noqa: BLE001 - demo pattern
            last_error = exc
            if attempt < retries:
                time.sleep(delay_s * attempt)
    if fallback and last_error:
        return fallback(last_error)
    raise last_error if last_error else RuntimeError("retry failed")


def flaky_service(should_fail: bool) -> str:
    if should_fail:
        raise ConnectionError("upstream unavailable")
    return "success"


if __name__ == "__main__":
    attempts = {"n": 0}

    def unstable() -> str:
        attempts["n"] += 1
        return flaky_service(attempts["n"] < 2)

    result = with_retry(unstable, fallback=lambda e: f"recovered after error: {e}")
    print(result)
