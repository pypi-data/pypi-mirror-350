import asyncio
import functools
import random
from typing import Callable, TypeVar, ParamSpec, Awaitable, cast, Optional

P = ParamSpec('P')
R = TypeVar('R')


def exponential_retry(
        max_retries: int = 3,
        base_delay: float = 1.0,
        max_delay: float = 60.0,
        jitter: bool = True,
        retryable_exceptions: tuple = (Exception,),
        logger=None
):
    """
    Decorator for exponential backoff retry mechanism for async functions.

    Args:
        max_retries: Maximum number of retry attempts
        base_delay: Initial delay between retries in seconds
        max_delay: Maximum delay between retries in seconds
        jitter: Whether to add random jitter to the delay
        retryable_exceptions: Tuple of exceptions that should trigger a retry
        logger: Logger object to use, if None no logging will be performed

    Returns:
        Decorator function
    """

    def decorator(func: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[R]]:
        @functools.wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            retries = 0

            while True:
                try:
                    return await func(*args, **kwargs)
                except retryable_exceptions as exc:
                    retries += 1
                    if retries > max_retries:
                        if logger:
                            logger.error(f"Maximum retries ({max_retries}) reached for {func.__name__}, giving up")
                        raise

                    # Calculate delay with exponential backoff
                    delay = min(base_delay * (2 ** (retries - 1)), max_delay)

                    # Add jitter if enabled (helps prevent thundering herd problem)
                    if jitter:
                        delay = delay * (0.5 + random.random())

                    if logger:
                        logger.warning(
                            f"Retry {retries}/{max_retries} for {func.__name__} after {delay:.2f}s "
                            f"due to: {exc.__class__.__name__}: {exc}"
                        )

                    await asyncio.sleep(delay)

        return cast(Callable[P, Awaitable[R]], wrapper)

    return decorator
