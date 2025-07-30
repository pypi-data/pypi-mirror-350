import random
import time
from functools import wraps
from splore_sdk.core.logger import sdk_logger


def retry_with_backoff(
    max_retries: int = 3,
    backoff_factor: float = 0.5,
    max_timeout: float = 300,
):
    """
    Retry a function with exponential backoff.

    Args:
        max_retries: The maximum number of retries.
        backoff_factor: The factor to multiply the sleep time by.
        max_timeout: The maximum time to wait before raising a timeout error.
        timeout_exception: The exception to catch and retry.

    Returns:
        A decorator that retries the function with exponential backoff.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            func_name = func.__name__
            retries_left = max_retries
            start_time = time.time()
            sleep_time = backoff_factor
            attempt = 0

            sdk_logger.debug(
                f"Starting retry operation for {func_name}, max retries: {max_retries}"
            )

            while retries_left > 0:
                attempt += 1
                try:
                    result = func(*args, **kwargs)
                    elapsed = time.time() - start_time
                    sdk_logger.debug(
                        f"Operation {func_name} succeeded on attempt {attempt} after {elapsed:.2f}s"
                    )
                    return result
                except Exception as e:
                    retries_left -= 1
                    elapsed = time.time() - start_time
                    jitter = random.uniform(-0.1, 0.1) * sleep_time  # Add ±10% jitter
                    sleep_time = min(
                        (sleep_time * 2) + jitter, 10
                    )  # Exponential backoff with jitter

                    if retries_left > 0:
                        sdk_logger.warning(
                            f"Retry attempt {attempt} for {func_name} failed after {elapsed:.2f}s: {str(e)}. Retrying in {sleep_time:.2f}s. Attempts left: {retries_left}"
                        )
                        time.sleep(sleep_time)
                    else:
                        sdk_logger.error(
                            f"All retry attempts ({max_retries}) exhausted for {func_name} after {elapsed:.2f}s. Last error: {str(e)}"
                        )

                    if time.time() - start_time > max_timeout:
                        sdk_logger.error(
                            f"Timeout exceeded for {func_name} after {elapsed:.2f}s"
                        )
                        raise TimeoutError(
                            f"Timeout exceeded after {max_timeout} seconds for {func_name}"
                        )

            raise RuntimeError(f"All {max_retries} retries exhausted for {func_name}")

        return wrapper

    return decorator
