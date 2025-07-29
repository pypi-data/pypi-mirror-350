"""
Rate limiting implementation for the aiopythonik library.

This module provides a rate limiting implementation that handles the iconik API
rate limits using an exponential backoff strategy.
"""

from __future__ import annotations

import asyncio
import random
import time
from dataclasses import dataclass
from typing import Any, Callable, Coroutine, Optional, TypeVar, cast

from ._pythonik_patches._logger import logger


T = TypeVar("T")


@dataclass
class RateLimitConfig:
    """
    Configuration for rate limiting behavior.

    Args:
        max_retries: Maximum number of retries for rate-limited requests
        initial_backoff: Initial backoff time in seconds
        max_backoff: Maximum backoff time in seconds
        backoff_factor: Exponential factor for backoff calculation
        jitter: Whether to add randomness to backoff times
    """

    max_retries: int = 3
    initial_backoff: float = 1.0
    max_backoff: float = 30.0
    backoff_factor: float = 2.0
    jitter: bool = True


class RateLimitError(Exception):
    """
    Exception raised for API rate limit errors.

    This custom exception class includes a response attribute to allow
    access to the original response object that triggered the rate limit.
    """

    def __init__(self, message: str = "Rate limit exceeded", response=None):
        """
        Initialize the RateLimitError.

        Args:
            message: Error message
            response: Optional response object that triggered the rate limit
        """
        self.response = response
        super().__init__(message)


class ResponseLike:
    """
    A wrapper class for objects that may have response-like attributes.

    This class is used to safely check for the existence of status_code
    and other attributes without raising attribute errors.
    """

    def __init__(self, obj: Any):
        """
        Initialize with any object that might have response-like attributes.

        Args:
            obj: The object to wrap
        """
        self._obj = obj

    @property
    def status_code(self) -> Optional[int]:
        """
        Get the status code if it exists.

        Returns:
            The status code or None
        """
        return getattr(self._obj, "status_code", None)

    @property
    def headers(self) -> Optional[dict]:
        """
        Get the headers if they exist.

        Returns:
            The headers or None
        """
        return getattr(self._obj, "headers", None)


class RateLimitHandler:
    """
    Handler for API rate limiting.

    Implements retry logic with exponential backoff for rate-limited requests.
    """

    def __init__(self, config: Optional[RateLimitConfig] = None):
        """
        Initialize the rate limit handler.

        Args:
            config: Optional configuration for rate limiting behavior
        """
        self.config = config or RateLimitConfig()
        self._remaining_requests: Optional[int] = None
        self._last_response_time = 0.0

    def update_limits(self, headers: dict) -> None:
        """
        Update rate limit information from response headers.

        Args:
            headers: Response headers containing rate limit information
        """
        self._last_response_time = time.time()
        if "RateLimit-Remaining" in headers:
            try:
                self._remaining_requests = int(headers["RateLimit-Remaining"])
                logger.debug(
                    "Rate limit remaining: {}", self._remaining_requests
                )
            except (ValueError, TypeError):
                logger.warning("Failed to parse RateLimit-Remaining header")

    def get_backoff_time(self, retry_count: int) -> float:
        """
        Calculate backoff time for a retry attempt.

        Args:
            retry_count: The current retry attempt (0-based)

        Returns:
            float: The backoff time in seconds
        """
        backoff = min(
            self.config.max_backoff,
            self.config.initial_backoff *
            (self.config.backoff_factor**retry_count),
        )
        if self.config.jitter:
            jitter_factor = 1.0 + random.uniform(-0.15, 0.15)
            backoff *= jitter_factor
        return backoff

    async def execute_with_retry(
        self,
        func: Callable[..., Coroutine[Any, Any, T]],
        *args: Any,
        **kwargs: Any,
    ) -> T:
        """
        Execute a function with retry logic for rate limiting.

        Args:
            func: The async function to execute
            *args: Positional arguments to pass to the function
            **kwargs: Keyword arguments to pass to the function

        Returns:
            The result of the function call

        Raises:
            Exception: If all retries are exhausted
        """
        retries = 0
        last_exception: Optional[Exception] = None
        while retries <= self.config.max_retries:
            try:
                result = await func(*args, **kwargs)

                if hasattr(result, "response"):
                    response_wrapper = ResponseLike(getattr(result, "response"))
                    if response_wrapper.headers:
                        self.update_limits(response_wrapper.headers)
                return cast(T, result)
            except Exception as e:
                last_exception = e

                is_rate_limit_error = False

                if isinstance(e, RateLimitError):
                    is_rate_limit_error = True

                elif hasattr(e, "response"):
                    response_wrapper = ResponseLike(getattr(e, "response"))
                    if response_wrapper.status_code == 429:
                        is_rate_limit_error = True
                if not is_rate_limit_error:
                    raise
                if retries >= self.config.max_retries:
                    logger.error(
                        "Rate limit exceeded and max retries ({}) reached",
                        self.config.max_retries,
                    )
                    raise
                backoff_time = self.get_backoff_time(retries)
                logger.warning(
                    "Rate limit exceeded. Retrying in {} seconds", backoff_time
                )
                await asyncio.sleep(backoff_time)
                retries += 1

        if last_exception:
            raise last_exception

        raise RuntimeError("Unexpected error in rate limit retry logic")
