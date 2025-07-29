from __future__ import annotations

import asyncio
from typing import Callable

from hamcrest import assert_that
from hamcrest.core.matcher import Matcher
from tenacity import AsyncRetrying, stop_after_delay, wait_fixed


class RetryAssert:
    """
    A class to perform asynchronous retries on a condition, with configurable timeout and polling interval before the first attempt.
    Use await_at_most() to create this class.

    """

    def __init__(self, timeout=10, interval=1.0) -> None:
        """
        Initializes the RetryAssert instance.

        :param timeout: The maximum duration to wait before giving up, in seconds.
        :param interval: The interval between retries, in seconds.
        :param initial_hold: The delay before the first attempt, in seconds.
        """
        self.timeout = timeout
        self._interval = interval
        self.attempts = 0

    async def until(self, func: Callable, matcher: Matcher) -> None:
        """
        Waits until the result of the given function matches the provided matcher, retrying until timeout.

        :param func: A callable that returns the result to be tested.
        :param matcher: A matcher from hamcrest to evaluate the result against.

        :raises TypeError: If func is not a callable.
        """
        if not callable(func):
            raise TypeError(f"Arguments used in .until(Callable) must be of type Callable, was {type(func)}")

        retrying = AsyncRetrying(stop=stop_after_delay(self.timeout), wait=wait_fixed(self._interval))
        async for attempt in retrying:
            with attempt:
                if asyncio.iscoroutinefunction(func):
                    result = await asyncio.wait_for(func(), self.timeout)
                elif hasattr(func, "__call__") and asyncio.iscoroutinefunction(func.__call__):
                    result = await asyncio.wait_for(func(), self.timeout)
                else:
                    result = func()

                assert_that(result, matcher)

    def with_poll_interval(self, seconds: float) -> RetryAssert:
        """
        Sets the interval between retries.

        :param seconds: The interval between retries, in seconds.
        :return: self, to allow method chaining.
        """
        self._interval = seconds
        return self


def await_at_most(seconds: float) -> RetryAssert:
    """
    Factory function to create a RetryAssert instance with a specified timeout.

    :param seconds: The maximum duration to wait before giving up, in seconds.
    :return: A configured instance of RetryAssert.
    """
    return RetryAssert(timeout=seconds)
