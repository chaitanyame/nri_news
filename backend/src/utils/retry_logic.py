"""
Exponential backoff retry logic for API calls.

This module provides a decorator and utility functions for implementing
retry logic with exponential backoff for handling transient failures.
"""

import time
import logging
from functools import wraps
from typing import TypeVar, Callable, Type, Tuple

logger = logging.getLogger(__name__)

T = TypeVar('T')


class MaxRetriesExceeded(Exception):
    """Raised when maximum retry attempts are exhausted."""
    pass


def exponential_backoff_retry(
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    exceptions: Tuple[Type[Exception], ...] = (Exception,)
):
    """
    Decorator for retrying functions with exponential backoff.
    
    Args:
        max_retries: Maximum number of retry attempts (default: 3)
        base_delay: Initial delay in seconds (default: 1.0)
        max_delay: Maximum delay between retries in seconds (default: 60.0)
        exceptions: Tuple of exception types to catch and retry
        
    Returns:
        Decorated function with retry logic
        
    Example:
        @exponential_backoff_retry(max_retries=3, base_delay=1.0)
        def fetch_data():
            return api.get('/data')
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> T:
            attempt = 0
            while attempt < max_retries:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    attempt += 1
                    if attempt >= max_retries:
                        logger.error(
                            f"Max retries ({max_retries}) exceeded for {func.__name__}",
                            extra={
                                "function": func.__name__,
                                "attempts": attempt,
                                "error": str(e)
                            }
                        )
                        raise MaxRetriesExceeded(
                            f"Failed after {max_retries} attempts: {str(e)}"
                        ) from e
                    
                    # Calculate delay with exponential backoff
                    delay = min(base_delay * (2 ** (attempt - 1)), max_delay)
                    
                    logger.warning(
                        f"Attempt {attempt}/{max_retries} failed for {func.__name__}, "
                        f"retrying in {delay}s",
                        extra={
                            "function": func.__name__,
                            "attempt": attempt,
                            "max_retries": max_retries,
                            "delay_seconds": delay,
                            "error": str(e)
                        }
                    )
                    
                    time.sleep(delay)
            
            # This should never be reached, but included for type checking
            raise MaxRetriesExceeded(f"Failed after {max_retries} attempts")
        
        return wrapper
    return decorator


def retry_with_backoff(
    func: Callable[..., T],
    max_retries: int = 3,
    base_delay: float = 1.0,
    exceptions: Tuple[Type[Exception], ...] = (Exception,)
) -> T:
    """
    Execute a function with exponential backoff retry logic.
    
    This is a non-decorator version for cases where you can't use decorators.
    
    Args:
        func: Function to execute
        max_retries: Maximum number of retry attempts
        base_delay: Initial delay in seconds (doubles each retry)
        exceptions: Tuple of exception types to catch and retry
        
    Returns:
        Return value from successful function execution
        
    Raises:
        MaxRetriesExceeded: If all retries are exhausted
        
    Example:
        result = retry_with_backoff(
            lambda: api.get('/data'),
            max_retries=3,
            base_delay=1.0
        )
    """
    attempt = 0
    while attempt < max_retries:
        try:
            return func()
        except exceptions as e:
            attempt += 1
            if attempt >= max_retries:
                raise MaxRetriesExceeded(
                    f"Failed after {max_retries} attempts: {str(e)}"
                ) from e
            
            delay = base_delay * (2 ** (attempt - 1))
            logger.warning(
                f"Attempt {attempt}/{max_retries} failed, retrying in {delay}s: {str(e)}"
            )
            time.sleep(delay)
    
    raise MaxRetriesExceeded(f"Failed after {max_retries} attempts")
