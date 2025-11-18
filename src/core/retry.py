import time
import random
import functools
from typing import Iterable, Callable, Any, Tuple, Type

from src.core.config import load_config
from src.core.logger import get_logger

cfg = load_config()
log = get_logger("retry")


def retry(
    attempts: int | None = None,
    delay_ms: int | None = None,
    backoff_multiplier: float | None = None,
    retry_on_status: Iterable[int] | None = None,
    retry_on_exceptions: Tuple[Type[BaseException], ...] = (Exception,),
    jitter_ms: int = 100,
):
    """
    Universal retry decorator with support for:
    - retrying on specific HTTP statuses,
    - retrying on exceptions,
    - exponential backoff,
    - jitter (randomized delay),
    - config-driven defaults.

    Args:
        attempts: Number of retry attempts. Falls back to config if None.
        delay_ms: Initial retry delay in milliseconds.
        backoff_multiplier: Multiplier applied after each retry (exponential backoff).
        retry_on_status: Iterable of HTTP status codes that trigger retry.
        retry_on_exceptions: Exceptions that should trigger retry.
        jitter_ms: Max random noise added to each delay to avoid thundering herd.

    Returns:
        Decorator that wraps a function with retry logic.
    """
    attempts = attempts or cfg.retry.attempts
    delay_ms = delay_ms or cfg.retry.delay_ms
    backoff_multiplier = backoff_multiplier or cfg.retry.backoff_multiplier
    retry_on_status = set(retry_on_status or cfg.retry.retry_on_status)

    def decorator(func: Callable[..., Any]):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 1
            wait = delay_ms / 1000.0
            last_exc = None

            while attempt <= attempts:
                try:
                    result = func(*args, **kwargs)

                    # If the wrapped function returns a Response (HTTP), inspect status
                    status = getattr(result, "status_code", None)
                    if status is not None and status in retry_on_status:
                        raise RuntimeError(f"retryable status {status}")

                    if attempt > 1:
                        log.info(f"[SUCCESS after {attempt} attempt(s)] {func.__name__}")

                    return result

                except retry_on_exceptions as e:
                    last_exc = e

                    if attempt == attempts:
                        log.error(f"[GIVE UP] {func.__name__}: {e}")
                        raise

                    log.warning(
                        f"[RETRY {attempt}/{attempts}] {func.__name__}: {e} | "
                        f"sleep {wait:.2f}s"
                    )

                    time.sleep(wait + random.uniform(0, jitter_ms / 1000.0))
                    wait *= backoff_multiplier
                    attempt += 1

            if last_exc:
                raise last_exc

        return wrapper

    return decorator
