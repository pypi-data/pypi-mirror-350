"""
Performance-related utility functions for Taskinity.

This module contains utilities for timing execution, caching results, and retrying operations.
"""
import time
import functools
from typing import Any, Callable, Dict, Optional, TypeVar, cast

T = TypeVar('T')

def timed_execution(func: Callable[..., T]) -> Callable[..., T]:
    """
    Decorator to measure and log the execution time of a function.
    
    Args:
        func: The function to time.
        
    Returns:
        The wrapped function that logs execution time.
    """
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> T:
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Function {func.__name__} executed in {end_time - start_time:.4f} seconds")
        return result
    return wrapper

def retry(max_attempts: int = 3, delay: float = 1.0, backoff: float = 2.0, 
          exceptions: tuple = (Exception,)) -> Callable:
    """
    Decorator to retry a function on failure.
    
    Args:
        max_attempts: Maximum number of retry attempts.
        delay: Initial delay between retries in seconds.
        backoff: Backoff multiplier for delay between retries.
        exceptions: Tuple of exceptions to catch and retry on.
        
    Returns:
        Decorator function.
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            attempt = 0
            current_delay = delay
            
            while attempt < max_attempts:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    attempt += 1
                    if attempt >= max_attempts:
                        raise
                    
                    print(f"Retry attempt {attempt}/{max_attempts} for {func.__name__} after error: {str(e)}")
                    time.sleep(current_delay)
                    current_delay *= backoff
            
            # This should never be reached due to the raise in the except block
            return cast(T, None)
        return wrapper
    return decorator

_cache: Dict[str, Dict[str, Any]] = {}

def cache_result(ttl: Optional[float] = None) -> Callable:
    """
    Decorator to cache function results.
    
    Args:
        ttl: Time-to-live for cached results in seconds. None means no expiration.
        
    Returns:
        Decorator function.
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        cache_key = f"{func.__module__}.{func.__qualname__}"
        if cache_key not in _cache:
            _cache[cache_key] = {}
            
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            # Create a key from the function arguments
            arg_key = str(args) + str(sorted(kwargs.items()))
            cache = _cache[cache_key]
            
            # Check if result is in cache and not expired
            if arg_key in cache:
                result, timestamp = cache[arg_key]
                if ttl is None or time.time() - timestamp < ttl:
                    return result
            
            # Call the function and cache the result
            result = func(*args, **kwargs)
            cache[arg_key] = (result, time.time())
            return result
        
        return wrapper
    return decorator
