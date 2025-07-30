import math
import random
import time
from typing import Callable, Any
from functools import wraps
from splore_sdk.core.logger import sdk_logger


def generate_intervals(min_poll_interval, max_poll_interval, poll_interval_change_rate):
    # Calculate number of steps
    n_steps = (
        int(math.log(max_poll_interval / min_poll_interval, poll_interval_change_rate))
        + 1
    )

    # Increasing sequence
    inc = [min_poll_interval * (poll_interval_change_rate**i) for i in range(n_steps)]
    # Ensure max is included (in case of floating point error)
    if inc[-1] < max_poll_interval:
        inc.append(max_poll_interval)

    # Decreasing sequence
    dec = [max_poll_interval / (poll_interval_change_rate**i) for i in range(n_steps)]
    if dec[-1] > min_poll_interval:
        dec.append(min_poll_interval)

    return inc, dec


def poll_with_timeout(
    condition: Callable[[Any], bool] = lambda x: x is not None,
    max_timeout: float = 30,
    min_poll_interval: float = 1,
    max_poll_interval: float = 5,
    poll_interval_change_rate: float = 2,
):
    """
    A decorator that polls a function and assigns the result to a variable
    until the result satisfies the condition or the max timeout is reached.

    The poll interval starts at min_poll_interval and increases up to
    max_poll_interval, then decreases back down to min_poll_interval in a
    sawtooth pattern.

    Args:
        condition (Callable[[Any], bool]): The condition to check on the result.
        max_timeout (float): The maximum time to wait for the result.
        min_poll_interval (float): The minimum poll interval.
        max_poll_interval (float): The maximum poll interval.
        poll_interval_change_rate (float): The rate at which the poll interval
            changes.
    Returns:
        A decorator that polls the function and assigns the result to a variable.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = None
            poll_interval = min_poll_interval
            func_name = func.__name__
            inc, dec = generate_intervals(
                min_poll_interval, max_poll_interval, poll_interval_change_rate
            )
            intervals = [interval for pair in zip(inc, dec) for interval in pair]
            jitter = 0.2
            sdk_logger.debug(f"Starting polling operation for {func_name}")
            attempt_count = 0

            while time.time() - start_time < max_timeout:
                attempt_count += 1
                result = func(*args, **kwargs)

                if not condition(result):
                    elapsed = time.time() - start_time
                    sdk_logger.debug(
                        f"Poll attempt {attempt_count} for {func_name}: condition not met after {elapsed:.2f}s, waiting {poll_interval:.2f}s"
                    )

                    sleep_time = intervals[attempt_count - 1] + random.uniform(
                        -jitter, jitter
                    )
                    time.sleep(sleep_time)
                else:
                    elapsed = time.time() - start_time
                    sdk_logger.debug(
                        f"Poll operation for {func_name} completed successfully after {attempt_count} attempts, total time: {elapsed:.2f}s"
                    )
                    break

            if time.time() - start_time > max_timeout:
                elapsed = time.time() - start_time
                sdk_logger.warning(
                    f"Poll operation for {func_name} timed out after {elapsed:.2f}s and {attempt_count} attempts"
                )
                raise TimeoutError(
                    f"Timeout exceeded after {max_timeout} seconds for {func_name}"
                )

            return result

        return wrapper

    return decorator
